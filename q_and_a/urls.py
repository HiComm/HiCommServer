from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = "q_and_a"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("about", views.AboutView.as_view(), name="about"),
    path("post_question", login_required(views.post_question), name="post_question"),
    path("post_article", login_required(views.post_diary), name="post_article"), 
    path("questions/<uuid:question_id>/", views.detail_question, name="detail_question"),
    path("article/<uuid:article_id>/", views.detail_question, name="detail_article"),
    #path("contents/<uuid:user_id>/<uuid:content_id>", ),

    path("ajax/save_draft", login_required(views.ajax_save_draft)),
    
]