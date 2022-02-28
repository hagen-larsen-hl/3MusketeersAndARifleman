from django.urls import path
from . import views

app_name = "jobs"


urlpatterns = [
    path("create/", views.create_job_request, name="create"),
    path("view/", views.view, name="view"),
    path("view/<int:job_id>", views.update_job_request, name="update"),
]
