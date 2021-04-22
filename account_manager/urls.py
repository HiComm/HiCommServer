from django.urls import path
from . import views

app_name = 'account_manager'

urlpatterns = [
    path('top/', views.Top, name='top'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path("register/", views.UserCreate.as_view(), name="register"),
    path("register_in_process/", views.UserCreateInProcess.as_view(), name="registerInProcess"),
    path("register_completed/<token>/", views.UserCreateComplete.as_view(), name="registerDone"),
    
]