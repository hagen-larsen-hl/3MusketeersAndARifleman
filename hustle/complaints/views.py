from xmlrpc.client import DateTime
from django.shortcuts import render, redirect
from .forms import ComplaintForm
from .models import Complaint
from django.contrib import messages
from datetime import datetime


def create(request):
    if request.user.is_authenticated:
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
    else:
        return redirect("main:login")


def view(request):
    if request.user.is_authenticated:
        complaints = Complaint.objects.filter(user=request.user)
        return render(request=request, template_name="complaints/view_all.html", context={"complaints": complaints})
    else:
        return redirect("main:login")
