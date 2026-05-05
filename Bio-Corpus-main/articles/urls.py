from django.urls import path
from . import views

app_name = "articles"

urlpatterns = [
    path("", views.article_list, name="list"),
    path("<str:article_id>/", views.article_detail, name="detail"),
]
