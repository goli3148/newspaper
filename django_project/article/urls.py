from django.urls import path
from .views import ArticleListView, ArticleDetailView, ArticleUpdateView, ArticleDeleteView, ArticleCreateView
urlpatterns = [
    path("create/", ArticleCreateView.as_view(), name="article_create"),
    path("<slug:slug>/delete/", ArticleDeleteView.as_view(), name="article_delete"),
    path("<slug:slug>/update/", ArticleUpdateView.as_view(), name="article_update"),
    path("<slug:slug>", ArticleDetailView.as_view(), name="article_detail"),
    path("", ArticleListView.as_view(), name="home"),
]