from django.urls import path
from .views import UserLoginView, UserRegistration, LogoutView

urlpatterns = [
    path('login/',UserLoginView.as_view()),
    path('register/',UserRegistration.as_view()),
    path('logout/', LogoutView.as_view())
]
