import os

"""该工具用来分析数据集地址"""
def get_dataset_info(root_path):
    """扫描文件路径，获取数据集信息"""
    list_img_path = []
    list_dir_path = []
    list_path = os.listdir(path=root_path)
    for volume in list_path:
        subset_url = os.path.join(root_path, volume)
        volume_dic = {
            'name': volume,
            'url': subset_url,
            'volume': volume,
            'quantity': file_cnt_in(subset_url)}
        list_dir_path.append(volume_dic)
        for root, dirs, files in os.walk(subset_url, topdown=True):
            for name in files:
                if name.endswith(".png") | name.endswith(".jpg"):
                    img_url = os.path.join(root, name)
                    page_dic = {'name': name, 'url': img_url, 'subset_url': subset_url,
                                'page': name[:-4], 'volume': volume}
                    list_img_path.append(page_dic)
    return list_img_path, list_dir_path





def file_cnt_in(currPath):
    """汇总当前目录下文件数"""
    count = 0
    for root, dirs, files in os.walk(currPath):
        for img in files:
            if img.endswith(".png") | img.endswith(".jpg") | img.endswith(".bmp") | img.endswith(".jpeg"):
                count += 1
    return count
