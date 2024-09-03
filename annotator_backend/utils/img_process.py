import os
import shutil

import cv2


def get_origin_img_narrow(url, origin_image_id):
    img = cv2.imread(url)
    height, width, channel = img.shape
    # 当图片高小于宽时需要旋转90度
    if height < width:
        # mat = cv2.getRotationMatrix2D((height * 0.5, width * 0.5), 90, 1)
        # img = cv2.warpAffine(img, mat, (height, width))
        img = cv2.transpose(img)
        img = cv2.flip(img, 0)
    # 长宽分别缩小为二分之一
    img = cv2.resize(src=img, dsize=(0, 0), fx=0.5, fy=0.5, interpolation=cv2.INTER_NEAREST)
    save_path = "../imgs/" + str(origin_image_id) + ".jpg"
    cv2.imwrite(save_path, img)
    return save_path


def clean_cache_images():
    """
    删除图片缓存
    """
    filepath = "../imgs"
    print(filepath)
    if not os.path.exists(filepath):
        os.mkdir(filepath)
    else:
        shutil.rmtree(filepath)
        os.mkdir(filepath)
