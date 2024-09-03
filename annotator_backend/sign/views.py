# Create your views here.
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib.auth.hashers import make_password
from sign.models import UserInfo
from utils.HttpRespond import HttpRespond

# 登录
def sign_in(request):
    pd = json.loads(request.body)
    username = pd.get('userName')
    password = pd.get('password')

    # 校验用户名和密码
    user = authenticate(username=username, password=password)
    # authenticate和login是Django auth 应用中的标准函数
    # 这个函数是 Django 的 django.contrib.auth模块的一部分，它的主要目的是通过接收用户名和密码作为参数来识别并验证用户。
    # 如果提供的凭证（用户名和密码）与数据库中的某个用户匹配，该函数将返回对应的用户对象；如果没有找到匹配的用户或密码不正确，它将返回None。

    if user is not None:
        # 校验权限和是否被激活
        if user.is_active:
            login(request, user)
            # login函数用于在当前会话中登录一个用户。这意味着一旦用户通过authenticate函数认证，login函数会将用户的ID保存在会话中，
            # 从而允许用户在不重新输入用户名和密码的情况下访问网站的其他受保护部分。
            # 使用login函数时，需要传入一个HttpRequest对象和一个通过authenticate函数认证的用户对象。这样做会为该用户创建一个登录会话。
            if user.is_superuser == 1:
                user_dict = {"username": user.username, "id": user.id, "role": 1}
                user = json.dumps(user_dict)
                # 对象转换（序列化）成JSON格式的字符串。
            else:
                user_dict = {"username": user.username, "id": user.id, "role": 2}
                user = json.dumps(user_dict)
            return HttpRespond.success(message="登录成功", data=user)
        else:
            return HttpRespond.error(message="非法用户")
    else:
        return HttpRespond.error(message="请输入正确的用户名或密码")


# 登出
def sign_out(request):
    logout(request)
    return HttpRespond.success(message="注销成功")


# 注册
def add_user(request):
    pd = json.loads(request.body)
    username = pd.get('username')
    password = pd.get('password')
    password = make_password(password)

    if UserInfo.objects.filter(username=username):
        return HttpRespond.error(message='用户已存在')

    UserInfo.objects.create(
        username=username,
        password=password,)
    return HttpRespond.success()


def get_user(request):
    users = UserInfo.objects.all()
    userList = []
    for datas in users:
        if datas.last_login is None:
            data_dict = {"id": datas.id, "name": datas.username, "last_login": datas.last_login}
        else:
            data_dict = {"id": datas.id, "name": datas.username,
                         "last_login": datas.last_login.strftime("%Y-%m-%d %H:%M:%S")}
        userList.append(data_dict)
    return HttpRespond.success(data=userList)

def search_user(request):
    pd = json.loads(request.body)
    search_name = pd.get("name")
    users = UserInfo.objects.filter(username__contains=search_name)
    userList = []
    for datas in users:
        if datas.last_login is None:
            data_dict = {"id": datas.id, "name": datas.username, "last_login": datas.last_login}
        else:
            data_dict = {"id": datas.id, "name": datas.username,
                         "last_login": datas.last_login.strftime("%Y-%m-%d %H:%M:%S")}
        userList.append(data_dict)
    return HttpRespond.success(data=userList)


def change_user(request):
    pd = json.loads(request.body)
    id = pd.get("id")
    password = make_password("111111")
    UserInfo.objects.filter(id=id).update(password=password)
    return HttpRespond.success()

def del_user(request):
    pd = json.loads(request.body)
    id = pd.get("id")
    user = UserInfo.objects.filter(id=id)
    user.delete()
    return HttpRespond.success()

def index(request):
    return HttpRespond.auth_error()
