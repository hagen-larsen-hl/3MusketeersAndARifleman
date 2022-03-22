from xmlrpc.client import DateTime
from django.shortcuts import render, redirect, get_object_or_404

from main.models import UserData
from .forms import ComplaintForm
from .models import Complaint
from django.contrib import messages
from datetime import datetime
from main.auth import user_is_authenticated, user_in_group


@user_is_authenticated()
@user_in_group("Customer")
def create(request):
    if request.method == "POST":
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save()
            complaint.create_date = datetime.today()
            complaint.user = request.user
            complaint.save()
            messages.success(request, "Complaint submitted successfully." )
            return redirect("complaints:view")
        messages.error(request, "There was invalid information in your complaint form. Please review and try again.")
    form = ComplaintForm()
    return render(request=request, template_name="complaints/create.html", context={"complaint_form":form})


@user_is_authenticated()
@user_in_group("Customer")
def view(request):
    open_complaints = Complaint.objects.filter(user=request.user, state='open')
    reimbursed_complaints = Complaint.objects.filter(user=request.user, state='reimbursed')
    closed_complaints = Complaint.objects.filter(user=request.user, state='closed')
    return render(request=request, template_name="complaints/view_all.html", context={"open_complaints": open_complaints, "reimbursed_complaints": reimbursed_complaints, "closed_complaints": closed_complaints, "all": False})


@user_is_authenticated()
@user_in_group("Owner")
def viewOne(request, complaint_id):
    complaint = get_object_or_404(Complaint, pk=complaint_id)
    return render(request, 'complaints/view_one.html', {'complaint': complaint})


@user_is_authenticated()
@user_in_group("Owner")
def viewAll(request):
    open_complaints = Complaint.objects.filter(state='open')
    reimbursed_complaints = Complaint.objects.filter(state='reimbursed')
    closed_complaints = Complaint.objects.filter(state='closed')
    return render(request, template_name="complaints/view_all.html", context={"open_complaints": open_complaints, "reimbursed_complaints": reimbursed_complaints, "closed_complaints": closed_complaints, "all": True})


@user_is_authenticated()
@user_in_group("Owner")
def reimburse(request, complaint_id):
    complaint = get_object_or_404(Complaint, pk=complaint_id)
    user = get_object_or_404(UserData, pk=complaint.user)
    if complaint.state != "reimbursed":
        user.money += 200
        user.save()
        complaint.state = "reimbursed"
        complaint.save()
    else:
        messages.error(request, "This complaint is not eligible for reimbursement.")

    return render(request, "complaints/view_one.html", {"complaint": complaint})


@user_is_authenticated()
@user_in_group("Owner")
def close(request, complaint_id):
    complaint = get_object_or_404(Complaint, pk=complaint_id)
    if complaint.state != "closed":
        complaint.state = "closed"
        complaint.save()
    else:
        messages.error(request, "This complaint cannot be closed.")
    return redirect("complaints:viewOne", complaint_id=complaint.id)


@user_is_authenticated()
@user_in_group("Customer")
def open(request, complaint_id):
    complaint = get_object_or_404(Complaint, pk=complaint_id)
    if complaint.state != "open":
        complaint.state = "open"
        complaint.save()
    else:
        messages.error(request, "This complaint cannot be re-opened.")
    return redirect("complaints:viewOne", complaint_id=complaint.id)
