from django.shortcuts import render, redirect, get_object_or_404

from jobs.models import Job

from .forms import SurveyForm
from .models import Survey
from django.contrib import messages
from datetime import datetime


def create(request, job_id):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = SurveyForm(request.POST)
            if form.is_valid():
                survey = form.save()
                survey.create_date = datetime.today()
                survey.job = Job.objects.get(pk=job_id)
                print(Job.objects.get(pk=job_id))
                survey.customer = Job.objects.get(pk=job_id).customer
                survey.save()
                messages.success(request, "Survey completed successfully." )
                return redirect("jobs:view")
            messages.error(request, "There was invalid information in your survey. Please review and try again.")
        form = SurveyForm()
        job = get_object_or_404(Job, pk=job_id)
        return render(request=request, template_name="surveys/create.html", context={"survey_form":form, "job": job})
    else:
        return redirect("main:login")


def viewOne(request, review_id):
    if request.user.is_authenticated:
        survey = get_object_or_404(Survey, pk=review_id)
        return render(request, 'surveys/view_one.html', {'survey': survey})
    else:
        return redirect("main:login")