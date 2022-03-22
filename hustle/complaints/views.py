from xmlrpc.client import DateTime
from django.shortcuts import render, redirect
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
def viewAll(request):
    open_complaints = Complaint.objects.filter(state='open')
    reimbursed_complaints = Complaint.objects.filter(state='reimbursed')
    closed_complaints = Complaint.objects.filter(state='closed')
    return render(request=request, template_name="complaints/view_all.html", context={"open_complaints": open_complaints, "reimbursed_complaints": reimbursed_complaints, "closed_complaints": closed_complaints, "all": True})
