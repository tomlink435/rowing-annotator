from django.urls import path
from sign import views

urlpatterns = [
    path('signIn/', views.sign_in, name='login'),
    path('signOut/', views.sign_out, name='logout'),
    path('addUser/', views.add_user, name='register'),  # 注册用户
    path('getUser/', views.get_user, name='getUser'),
    path('searchUser/', views.search_user, name='searchUser'),
    path('changeUser/', views.change_user, name='changeUser'),
    path('delUser/', views.del_user, name='delUser'),
]
