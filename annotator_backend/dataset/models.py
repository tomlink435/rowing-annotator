from django.db import models
from config import settings


class DataSet(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=16, verbose_name="名称")
    quantity = models.IntegerField(default=0, verbose_name="数量")
    description = models.TextField(verbose_name="描述")
    create_time = models.DateField(auto_now_add=True, verbose_name="创建时间")
    is_mark = models.IntegerField(verbose_name="是否标注完成")
    user_id = models.IntegerField(default=0, verbose_name="用户id")

    class Meta:
        db_table = 'tb_dataset'
        verbose_name = '数据集表'


class MarkResult(models.Model):
    id = models.AutoField(primary_key=True)
    dataset = models.ForeignKey("DataSet", to_field='id', on_delete=models.CASCADE)
    result = models.TextField(verbose_name="标注结果")
    url = models.URLField(unique=True, verbose_name="地址")
    create_time = models.DateField(auto_now_add=True, verbose_name="创建时间")
    is_mark = models.IntegerField(verbose_name="是否标注完成")

    class Meta:
        db_table = 'tb_mark_result'
        verbose_name = '图片标注结果表'