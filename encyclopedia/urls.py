from django.urls import path
from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("add",views.add,name="add"),
    path("random",views.random,name="random"),
    path("<str:title>",views.title,name="title"),
    path("search/",views.search,name="search"),
    path("edit/<str:entry>",views.edit,name="edit"),
]
