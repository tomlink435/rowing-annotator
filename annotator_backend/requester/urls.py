from django.urls import path
from requester import views

urlpatterns = [
    path('getDataSet', views.get_dataset, name='getDataSet'),
    path('getDataSetTask', views.get_dataset_task, name='getDataSetTask'),
    path('addDataSet/', views.add_dataSet, name="addDataSet"),
    path('delDataSet/', views.del_dataSet, name="delDataSet"),
    path('upload/', views.upload, name="upload"),
    path('getAllData/', views.get_all_data, name="getAllData"),
    path('getFirstData/', views.get_first_data, name="getAllData"),
    path('getFrame/', views.get_frame, name="getFrame"),
    path('searchName/', views.search_name, name="searchName"),
    path('changeMark/', views.change_mark, name="changeMark"),
    path('test/', views.test, name="test"),
    path('downloadResults/', views.download_results, name="downloadResults"),

]
