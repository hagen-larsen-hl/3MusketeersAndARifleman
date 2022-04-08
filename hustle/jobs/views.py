from django.shortcuts import render, redirect
from .forms import NewJobForm, NewJobBidForm
from django.contrib import messages
from main.auth import user_passes_test, user_is_authenticated, user_in_group
from .models import Job, Bid, JobType
from django.contrib.auth.models import Group, User


@user_is_authenticated()
@user_in_group("Customer")
def create_job_request(request):
    if request.method == "POST":
        form = NewJobForm(request.POST)
        errors = form.errors
        if form.is_valid():
            job = form.save()
            job.complete = False
            job.customer = request.user
            job.save()
            messages.success(request, "Job submitted successfully.")
            return redirect("jobs:view mine")
        messages.error(request, errors)
        messages.error(request, "There was invalid information in your job form. Please review and try again.")
    form = NewJobForm()
    return render(request=request, template_name='jobs/job_form.html', context={"create_job_form": form})


@user_is_authenticated()
def view(request):
    if request.user.groups.filter(name="Worker").exists():
        open_jobs = Job.objects.filter(claimed_user=request.user, complete=False, cancelled=False)
        completed_jobs = Job.objects.filter(claimed_user=request.user, complete=True)
        cancelled_jobs = Job.objects.filter(claimed_user=request.user, cancelled=True)
        isWorker = True
    else:
        open_jobs = Job.objects.filter(customer=request.user, complete=False, cancelled=False)
        completed_jobs = Job.objects.filter(customer=request.user, complete=True)
        cancelled_jobs = Job.objects.filter(customer=request.user, cancelled=True)
        isWorker = False
    
    return render(request=request, template_name="jobs/view_all.html", context={"open_jobs": open_jobs, "completed_jobs": completed_jobs, "isWorker": isWorker, "cancelled_jobs": cancelled_jobs})


@user_is_authenticated()
@user_in_group("Customer")
def update_job_request(request, job_id):
    try:
        job = Job.objects.get(pk=job_id)
    except Job.DoesNotExist:
        return redirect("jobs:view")
    if not job.request_from_owner(request):
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
            return redirect("jobs:view job", job_id)
        messages.error(request, errors)
        messages.error(request, "There was invalid information in your job form. Please review and try again.")
    form = NewJobForm(instance=job)
    return render(request=request, template_name='jobs/edit_job_form.html', context={"create_job_form": form})

@user_is_authenticated()
def view_job(request, job_id):
    try:
        job = Job.objects.get(pk=job_id)
    except Job.DoesNotExist:
        return redirect("jobs:view")
    form = NewJobBidForm()
    bids = Bid.objects.filter(selected_job_id=job_id)

    return render(request=request, template_name='jobs/view_job.html', context={"job": job, "job_bid_form": form, "bids": bids})


@user_is_authenticated()
@user_in_group("Worker")
def bid_on_job(request, job_id):
    try:
        job = Job.objects.get(pk=job_id)
    except Job.DoesNotExist:
        return redirect("jobs:view")
    if request.method == "POST":
        form = NewJobBidForm(request.POST)
        bid = form.instance
        bid.user = request.user
        bid.selected_job = job
        errors = form.errors
        if form.is_valid():
            bid.save()
            return redirect("jobs:view job", job_id)
    return redirect("jobs:view job", job_id)


@user_in_group("Worker")
@user_is_authenticated()
def complete_job(request,job_id):
    job = Job.objects.get(pk=job_id)
    job.complete = not job.complete
    job.save()

    job.customer.data.money -= job.accepted_bid.bid
    ownerCut = job.accepted_bid.bid * job.type.ownerCut
    workerCut = job.accepted_bid.bid - ownerCut
    job.accepted_bid.user.data.money += workerCut

    #this dosen't work for some reason
    User.objects.filter(groups__name="Owner").first().data.money += ownerCut
    User.objects.filter(groups__name="Owner").first().data.save()

    job.customer.data.save()
    job.accepted_bid.user.data.save()

    return redirect("jobs:view job",job.id)


@user_in_group("Customer")
@user_is_authenticated()
def cancel_accept_bid(request,job_id):
    job = Job.objects.get(pk=job_id)
    job.claimed_user = None
    job.accepted_bid = None
    job.save()

    return redirect("jobs:view job",job.id)


def _job_filter_from(key, values):
    out = {}
    if key == "state":
        if "open" in values:
            out["complete"] = False
            out["cancelled"] = False
            out["accepted_bid__isnull"] = True
        if "accepted" in values:
            out["accepted_bid__isnull"] = False
        if "completed" in values:
            out["complete"] = True
        if "cancelled" in values:
            out["cancelled"] = True
    elif key == "zip_code":
        out["zip_code__in"] = values
    elif key == "type":
        out["type__type__in"] = values
    elif values[0]:
        if key == "estimate_min":
            out["time_estimate__gte"] = values[0]
        elif key == "estimate_max":
            out["time_estimate__lte"] = values[0]
        elif key == "start_time_min":
            out["completion_window_start__gte"] = values[0]
        elif key == "start_time_max":
            out["completion_window_start__lte"] = values[0]
        elif key == "end_time_min":
            out["completion_window_end__gte"] = values[0]
        elif key == "end_time_max":
            out["completion_window_end__lte"] = values[0]
    return out

def _job_filters_from(queries):
    filters = {}
    for k,v in queries.items():
        filters = {**filters, **_job_filter_from(k,v)}
    return filters

@user_is_authenticated()
def view_all_jobs(request):
    queries = {"state": ["open"]}
    if request.GET:
        queries = dict(request.GET.lists())
    filters = _job_filters_from(queries)
    jobs = Job.objects.filter(**filters)
    return render(request=request, template_name='jobs/view_every_job.html', context={"jobs": jobs, "work_types": JobType.objects.all(), "queries": queries})


@user_in_group("Customer")
@user_is_authenticated()
def accept_bid(request, job_id, bid_id):
    try:
        job = Job.objects.get(pk=job_id)
    except Job.DoesNotExist:
        return redirect("jobs:view")
    if request.method == "POST":
        bids = [bid for bid in Bid.objects.filter(selected_job_id=job_id) if bid.id == bid_id]
        if not bids:
            return redirect("jobs:view")
        else:
            job.accepted_bid_id = bid_id
            job.save()
        return redirect("jobs:view job", job_id)


@user_is_authenticated()
def cancel_job(request, job_id):
    try:
        job = Job.objects.get(pk=job_id)
    except Job.DoesNotExist:
        return redirect("jobs:view")
    if request.method == "POST":
        job.cancelled = True
        job.save()
        return redirect("jobs:view")

