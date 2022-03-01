from django.urls import path
from . import views

app_name = "complaints"   


urlpatterns = [
    # path("", views.profile, name="profile"),
    path("create/", views.create, name="create"),
    path("view/", views.view, name="view"),
    path("view/all/", views.viewAll, name="viewAll")
]