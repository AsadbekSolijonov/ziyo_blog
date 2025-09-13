from django.urls import path
from content import views

urlpatterns = [
    path('hello/', views.hello_world),
    path('welcome/', views.welcome),
    path('', views.blogs),
    path('f/', views.fblogs)
]
