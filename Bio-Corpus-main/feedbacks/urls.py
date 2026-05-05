from django.urls import path
from . import views

app_name = "feedbacks"

urlpatterns = [
    path("submit/<str:article_id>/", views.submit, name="submit"),
]
