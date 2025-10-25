from django.urls import path
from content import views

urlpatterns = [
    path('', views.blogs),
    path('<int:pk>/', views.single_blog),
]
