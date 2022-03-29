from django.urls import path
from . import views

app_name = "jobs"


urlpatterns = [
    path("create/", views.create_job_request, name="create"),
    path("view/", views.view_all_jobs, name="view"),
    path("view/mine/", views.view, name="view mine"),
    path("update/<int:job_id>/", views.update_job_request, name="update"),
    path("accept_bid/<int:bid_id>/", views.accept_bid, name="accept bid"),
    path("cancle_accept_bid/<int:job_id>/", views.cancel_accept_bid, name="cancel accept bid"),
    path("complete_job/<int:job_id>/", views.complete_job, name="complete job"),
    path("view/<int:job_id>/", views.view_job, name="view job"),

]
