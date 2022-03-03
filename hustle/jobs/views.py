from django.shortcuts import render, redirect
from .forms import NewJobForm
from django.contrib import messages
from .models import Job


def create_job_request(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = NewJobForm(request.POST)
            errors = form.errors
            if form.is_valid():
                job = form.save()
                job.complete = False
                job.customer = request.user
                job.save()
                messages.success(request, "Job submitted successfully.")
                return redirect("jobs:view")
            messages.error(request, errors)
            messages.error(request, "There was invalid information in your job form. Please review and try again.")
        form = NewJobForm()
        return render(request=request, template_name='jobs/job_form.html', context={"create_job_form": form})
    else:
        return redirect("main:login")


def view(request):
    if request.user.is_authenticated:
        open_jobs = Job.objects.filter(customer=request.user, complete=False)
        completed_jobs = Job.objects.filter(customer=request.user, complete=True)
        return render(request=request, template_name="jobs/view_all.html", context={"open_jobs": open_jobs, "completed_jobs": completed_jobs})
    else:
        return redirect("main:login")


def update_job_request(request, job_id):
    if request.user.is_authenticated:
        try:
            job = Job.objects.get(pk=job_id)
        except Job.DoesNotExist:
            return redirect("jobs:view")
        if job.customer != request.user:
            return redirect("jobs:view")
        if request.method == "POST":
            form = NewJobForm(request.POST)
            errors = form.errors
            if form.is_valid():
                job = form.instance
                job.complete = False
                job.customer = request.user
                job.id = job_id
                job.save()
                messages.success(request, "Job submitted successfully.")
                return redirect("jobs:view")
            messages.error(request, errors)
            messages.error(request, "There was invalid information in your job form. Please review and try again.")
        form = NewJobForm(instance=job)
        return render(request=request, template_name='jobs/edit_job_form.html', context={"create_job_form": form})
    else:
        return redirect("main:login")


def view_job(request, job_id):
    if request.user.is_authenticated:
        try:
            job = Job.objects.get(pk=job_id)
        except Job.DoesNotExist:
            return redirect("jobs:view")
        return render(request=request, template_name='jobs/view_job.html', context={"job": job})
    else:
        return redirect("main:login")