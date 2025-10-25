from django.urls import path
from content import views

urlpatterns = [
    path('', views.blogs),
    path('<int:pk>/', views.single_blog),
    path('cbv-lc/', views.BlogListCreateView.as_view()),
    path('cbv-rud/<int:pk>', views.BlogRetrieveUpdateDestoryView.as_view())
]
