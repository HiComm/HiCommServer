from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = "q_and_a"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("about", views.AboutView.as_view(), name="about"),
    path("post_question", login_required(views.PostQuestionView.as_view()), name="post_question"),
]