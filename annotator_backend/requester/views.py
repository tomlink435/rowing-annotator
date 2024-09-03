import csv
import json
import os
import asyncio
import cv2
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST

from dataset.models import DataSet
from dataset.models import MarkResult
from tcp_network_client import TcpNetworkClient
from utils.HttpRespond import HttpRespond
from datetime import datetime
import pickle
import numpy as np
import pandas as pds

# 查看数据集
@require_GET
def get_dataset(requester):
    datasets = DataSet.objects.all()
    print('-------',datasets)
    reslist = []
    for datas in datasets:
        marks = MarkResult.objects.filter(dataset_id=datas.id)
        flag = 1
        for mark in marks:
            if mark.result == "":
                flag = 3
                break
        if flag == 1 and datas.is_mark!=1:
            DataSet.objects.filter(id=datas.id).update(is_mark=0)
            datas.is_mark = 0
        data_dict = {"id": datas.id, "name": datas.name, "quantity": datas.quantity,
                     "describe": datas.description, "create_time": datas.create_time
            , "is_mark": datas.is_mark,"user_id":datas.user_id}
        reslist.append(data_dict)
    return HttpRespond.success(data=reslist)


@require_GET
def get_dataset_task(requester):
    datasets = DataSet.objects.filter(is_mark=1)
    reslist = []
    for datas in datasets:
        data_dict = {"id": datas.id, "name": datas.name, "quantity": datas.quantity,
                     "describe": datas.description, "create_time": datas.create_time,"user_id":datas.user_id}
        reslist.append(data_dict)
    return HttpRespond.success(data=reslist)


# 添加数据集
# @require_POST
def add_dataSet(name, description, url, userId):
    if DataSet.objects.filter(name=name).exists():
        dataset = DataSet.objects.get(name=name)
        DataSet.objects.filter(name=name).update(quantity=dataset.quantity + 1)
    else:
        DataSet.objects.create(
            name=name,
            quantity=1,
            description=description,
            is_mark=3,
            user_id=userId
        )
    dataset = DataSet.objects.get(name=name)
    MarkResult.objects.create(
        url=url,
        dataset_id=dataset.id,
        is_mark=0,
    )

    encode_input = url.encode('utf-8')
    client = TcpNetworkClient("localhost", 9998, 4096)
    if url.endswith(".mp4") or url.endswith(".avi") or url.endswith(".mkv") or url.endswith("flv") or url.endswith(
            "mov") or url.endswith("wmv") or url.endswith("rmvb") or url.endswith("webm"):
        client = TcpNetworkClient("localhost", 9999, 4096)
        client.send_data(encode_input)
        data = client.recv_data()
        serialized_data = pickle.loads(data)
        print(serialized_data)
        MarkResult.objects.filter(url=url).update(result=serialized_data)
    else:
        client.send_data(encode_input)
        data = client.recv_data()
        serialized_data = pickle.loads(data)
        print(serialized_data)
        new_arr = serialized_data.tolist()
        MarkResult.objects.filter(url=url).update(result=new_arr)


def add_dataSet_Id(addId, url):
    dataset = DataSet.objects.get(id=addId)
    DataSet.objects.filter(id=addId).update(quantity=dataset.quantity + 1)
    encode_input = url.encode('GB2312')
    # encode_input = url.encode('utf-8')

    MarkResult.objects.create(
        url=url,
        dataset_id=dataset.id,
        is_mark=0
    )

    client = TcpNetworkClient("localhost", 9998, 4096)
    if url.endswith(".mp4") or url.endswith(".avi") or url.endswith(".mkv") or url.endswith("flv") or url.endswith(
            "mov") or url.endswith("wmv") or url.endswith("rmvb") or url.endswith("webm"):
        client = TcpNetworkClient("localhost", 9999, 4096)
        client.send_data(encode_input)
        data = client.recv_data()
        serialized_data = pickle.loads(data)
        print(serialized_data)
        MarkResult.objects.filter(url=url).update(result=serialized_data)
    else:
        client.send_data(encode_input)
        data = client.recv_data()
        serialized_data = pickle.loads(data)
        print(serialized_data)
        new_arr = serialized_data.tolist()
        MarkResult.objects.filter(url=url).update(result=new_arr)


async def my_async_method(url):
    await asyncio.sleep(2)
    print("Hello, World!")
    return "Hello, World!"


@require_POST
def del_dataSet(request):
    """删除数据集"""
    pd = json.loads(request.body)
    dataset = DataSet.objects.filter(id=pd.get('id'))
    if dataset is not None:
        dataset.delete()
        return HttpRespond.success()
    else:
        return HttpRespond.error(message="数据集不存在")


@require_POST
def download_results(request):
    # 解析JSON请求体

        pd = json.loads(request.body)
        obj_id = pd.get("id")

        # 根据ID查询数据
        objs =MarkResult.objects.filter(dataset_id=obj_id)
        print(objs)
        # 定义文件路径
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        head_path = BASE_DIR + "/upload/json"
        file_path = head_path+'/file.xlsx'
        # 将查询结果转换为字典列表
        data = [{
            'ID': index+1,
            # 'id2':obj.id,
            '坐标': obj.result
        } for index, obj in enumerate(objs, start=0)]

        # 转换成pandas DataFrame
        df = pds.DataFrame(data)
        # 将DataFrame写入Excel文件
        df.to_excel(file_path, index=False)

        # 返回文件路径或下载链接
        download_url = file_path
        data_dict = {"url": download_url}
        return HttpRespond.success(data=data_dict)




@require_POST
def upload(request):
    # 获取相对路径
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        addId = request.POST.get('id')
        userId = request.POST.get('userId')
        files = request.FILES.getlist('file', None)
        for file in files:
            # 设置文件上传文件夹
            head_path = BASE_DIR + "/upload/json"
            # 判断是否存在文件夹, 如果没有就创建文件路径
            if not os.path.exists(head_path):
                os.makedirs(head_path)
            # 获取当前日期和时间
            current_datetime = datetime.now()
            # 格式化日期时间为字符串
            datetime_string = current_datetime.strftime("%Y%m%d%H%M%S")
            # file_suffix = file.name.split(".")[1]  # 获取文件后缀
            # 储存路径
            file_path = head_path + "/{}".format(datetime_string + file.name)
            file_path = file_path.replace(" ", "")
            # 上传文件
            with open(file_path, 'wb') as f:
                for chunk in file.chunks():
                    f.write(chunk)
            print(addId)
            if addId is None:
                add_dataSet(name, description, file_path, userId)
            else:
                add_dataSet_Id(addId, file_path)
    return HttpRespond.success()


@require_POST
def get_all_data(request):
    pd = json.loads(request.body)
    markResults = MarkResult.objects.filter(dataset_id=pd.get("setId"))
    results = []
    for result in markResults:
        data_dict = {"id": result.id, "result": result.result, "url": result.url,
                     "is_mark": result.is_mark}
        results.append(data_dict)
    return HttpRespond.success(data=results)


@require_POST
def get_first_data(request):
    pd = json.loads(request.body)
    result = MarkResult.objects.filter(dataset_id=pd.get("setId")).first()
    data_dict = {"id": result.id, "result": result.result, "url": result.url, "is_mark": result.is_mark}
    return HttpRespond.success(data=data_dict)


@require_POST
def get_frame(request):
    pd = json.loads(request.body)
    video_path = pd.get("video")
    print(video_path)
    video = cv2.VideoCapture(video_path)
    # 检查是否成功打开视频
    if not video.isOpened():
        print("Error opening video file")
        exit()
    # 获取帧率
    fps = video.get(cv2.CAP_PROP_FPS)
    print("Frame rate: ", fps)
    # 释放视频文件
    video.release()
    return HttpRespond.success(data=fps)


@require_POST
def search_name(request):
    pd = json.loads(request.body)
    search_name = pd.get("name")
    datasets = DataSet.objects.filter(name__contains=search_name)
    reslist = []
    for datas in datasets:
        data_dict = {"id": datas.id, "name": datas.name, "quantity": datas.quantity,
                     "describe": datas.description, "create_time": datas.create_time
            , "is_mark": datas.is_mark}
        reslist.append(data_dict)
    return HttpRespond.success(data=reslist)


@require_POST
def change_mark(request):
    pd = json.loads(request.body)
    set_id = pd.get("id")
    DataSet.objects.filter(id=set_id).update(is_mark=1)
    return HttpRespond.success()



@require_POST
def test(request):
    # data = np.loadtxt(open("C://Users/18242/Desktop/test.csv", "rb"), delimiter=",", skiprows=7,
    #                   usecols=[34, 35, 20, 21, 41, 42, 174, 175, 35, 36, 188, 189, 62, 63, 195, 196, 307, 308, 335, 336,
    #                            314, 315, 342, 343, 321, 322, 349, 350])
    # data = np.loadtxt(open("C://Users/18242/Desktop/test.csv", "rb"), delimiter=",", skiprows=7,
    #                   usecols=[34, 35, 36, 20, 21, 22, 41, 42, 43, 174, 175, 176, 35, 36, 37, 188, 189, 190, 62, 63, 64, 195, 196, 197, 307, 308, 309,
    #                            335, 336, 337,
    #                            314, 315, 316, 342, 343, 344, 321, 322, 323, 349, 350, 351])
    # 读取csv
    data = np.loadtxt(open("C://Users/18242/Desktop/test.csv", "rb"), delimiter=",", skiprows=7,
                      usecols=[36, 35, 22, 21, 43, 42, 176, 175, 57, 56, 190, 189, 64, 63, 197, 196, 309, 308,
                               337, 336,
                               316, 315, 344, 343, 323, 322, 351, 350])
    #每隔12个数据
    data = data[::4]


    # data = [[-64.16284, 211.0097, 60.40332, 153.3238, -10.16254, 194.8604, -35.40027, -232.2198, 318.3802, -154.2785, -12.13489, 195.7104, -183.6664,-109.913,
    #          338.3191, -90.69226, -3.114929, -7.767792,549.0597,-51.43744,516.3044,-168.1064,3.114929,7.767792,551.0953,21.73077,484.8453,-240.6562]]
    data_list = data.tolist()

    print(data)
    return HttpRespond.success(data=json.dumps(data_list))