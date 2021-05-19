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
    path("article/<uuid:article_id>/", views.detail_diary, name="detail_article"),
    path("ajax/submit_good/", login_required(views.ajax_submit_good), name="ajax_submit_good"),
    path("post/answer/<uuid:question_id>/", login_required(views.ajax_post_answer), name="post_answer"),
    path("error/", views.ErrorPage.as_view(), name="error"),
    #path("contents/<uuid:user_id>/<uuid:content_id>", ),

    path("ajax/save_draft", login_required(views.ajax_save_draft), name="ajax_save_draft"),
    path("ajax/get_q_drafts", login_required(views.ajax_get_q_drafts), name="ajax_get_q_drafts"),
    path("ajax/get_d_drafts", login_required(views.ajax_get_d_drafts), name="ajax_get_d_drafts"),
    path("ajax/set_bestanswer/<uuid:question_id>/", login_required(views.ajax_set_bestanswer), name="ajax_set_bestanswer"),
    path("ajax/post_comment", login_required(views.ajax_post_comment), name="ajax_post_comment"),
    path("ajax/get_tags_json", views.ajax_get_tags_json, name="ajax_get_tags_json"),
]