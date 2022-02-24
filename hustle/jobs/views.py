from django.shortcuts import render


def post_job(request):
    return render(request, 'templates/job_form.html')
