"""封装JsonRespond"""
from django.http import JsonResponse


class HttpRespond(object):

    @staticmethod
    def success(message="操作成功", data=None):
        json_dict = {"code": 200, "message": message, "data": data}
        return JsonResponse(json_dict)

    # @staticmethod
    # 是一个装饰器，用于声明紧随其后的方法是一个静态方法。静态方法不需要实例化其所在的类即可调用
    # 通过使用这样的静态方法，可以避免在多个地方重复编写相同的响应生成代码，从而提高代码的可维护性和一致性。

    @staticmethod
    def error(message="操作失败", data=None):
        json_dict = {"code": 400, "message": message, "data": data}
        return JsonResponse(json_dict)

    @staticmethod
    def auth_error(message="权限不足，请重新登录", data=None):
        json_dict = {"code": 302, "message": message, "data": data}
        return JsonResponse(json_dict)