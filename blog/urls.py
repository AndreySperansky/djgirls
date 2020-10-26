from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
]

'''
<int:pk> — эта часть означает, что Django ожидает целочисленное значение и 
преобразует его в представление — переменную pk
'''