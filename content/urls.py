from django.urls import path
from content import views

urlpatterns = [
    path('cbv-lc/', views.BlogListCreateView.as_view()),
    path('cbv-rud/<int:pk>', views.BlogRetrieveUpdateDestoryView.as_view()),
    path('my/', views.MyListBlogView.as_view())
]
