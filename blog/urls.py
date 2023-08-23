from django.urls import path
from .views import PostListCreateView,PostDetailView

urlpatterns = [
    path('post/',PostListCreateView.as_view()),
    path('post/<int:pk>/',PostDetailView.as_view())
]