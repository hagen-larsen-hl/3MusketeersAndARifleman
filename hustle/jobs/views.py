from django.shortcuts import render

from jobs.forms import NewJobForm


def create_job_request(request):
    form = NewJobForm()
    return render(request=request, template_name='jobs/job_form.html', context={"create_job_form": form})

