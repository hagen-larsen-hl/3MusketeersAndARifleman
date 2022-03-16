from django.shortcuts import render, redirect
from .forms import NewUserForm, MoneyForm, EditUser
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm


def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			return redirect("main:profile")
	else:
		form = NewUserForm()
	return render(request=request, template_name="main/register.html", context={"register_form": form})


def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("main:profile")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	else:
		form = AuthenticationForm()
	return render(request=request, template_name="main/login.html", context={"login_form":form})

def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("main:login")


def profile(request):
    if request.user.is_authenticated:
        return render(request, 'main/profile.html', {})
    else:
        return redirect("main:login")

def deposit_money(request):
    if request.user.is_authenticated:
        form = MoneyForm(data=request.POST)
        if form.is_valid():
            request.user.data.money += form.cleaned_data['money']
            request.user.data.save()
            return redirect("main:profile")
        return render(request, 'main/profile.html', {"deposit": True,"money_form": form})
    else:
        return redirect("main:login")

def withdraw_money(request):
    if request.user.is_authenticated:
        form = MoneyForm(data=request.POST)
        if form.is_valid():
            request.user.data.money -= form.cleaned_data['money']
            request.user.data.save()
            return redirect("main:profile")
        return render(request, 'main/profile.html', {"withdraw": True, "money_form": form})
    else:
        return redirect("main:login")

def edit_user(request):
    if request.user.is_authenticated:
        #this is how you pre populate the form
        form = EditUser(data=request.POST,initial=
        {"email": request.user.email,
         "username": request.user.username,
         "first_name": request.user.first_name,
         "last_name": request.user.last_name,})

        if form.is_valid():
            request.user.email = form.cleaned_data['email']
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.save()
            return redirect("main:profile")
        return render(request, 'main/profile.html', {"edit": True, "edit_form": form})

    else:
        return redirect("main:login")

