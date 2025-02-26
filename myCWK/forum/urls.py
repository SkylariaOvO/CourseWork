from django.urls import path
from . import views

urlpatterns = [
    path("", views.forum_home, name="forum_home"),
    path("create/", views.create_post, name="create_post"),
    path("<slug:slug>/edit/", views.edit_post, name="edit_post"),
    path("post/delete/<slug:slug>/", views.delete_post, name="delete_post"),
    path("<slug:slug>/vote/<str:vote_type>/", views.vote_post, name="vote"),
    path("<slug:slug>/reply/", views.reply_to_post, name="reply"),
    path("<slug:slug>/reply/<slug:parent_slug>/", views.reply_to_post, name="nested_reply"),
    path("<slug:slug>/reply_form/<slug:parent_slug>/", views.reply_form, name="reply_form"),
    path("reply/delete/<slug:slug>/", views.delete_reply, name="delete_reply"),
    path("<slug:slug>/", views.post_detail, name="post_detail"),
]

        
        
        
        