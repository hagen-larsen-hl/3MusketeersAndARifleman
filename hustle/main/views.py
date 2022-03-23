from django.shortcuts import render, redirect
from .models import User, BlackList
from .forms import NewUserForm, MoneyForm, EditUser
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from main.auth import user_not_authenticated, user_is_authenticated


@user_not_authenticated()
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


@user_not_authenticated()
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
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request=request, template_name="main/login.html", context={"login_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("main:login")


@user_is_authenticated()
def profile(request):
    return render(request, 'main/profile.html', {})


@user_is_authenticated()
def other_profile(request, user_id):
    if request.user.is_authenticated:
        if user_id == request.user.id:
            return redirect("main:profile")

        current_user = User.objects.get(pk=user_id)

        l = BlackList.objects.filter(user=request.user, blacklisted_user=current_user)

        alreadyBlackListed = len(l) >= 1

        return render(request, 'main/other_profile.html', {"user": current_user, "bl": alreadyBlackListed})
    else:
        return redirect("main:login")


@user_is_authenticated()
def deposit_money(request):
    form = MoneyForm(data=request.POST)
    if form.is_valid():
        request.user.data.money += form.cleaned_data['money']
        request.user.data.save()
        return redirect("main:profile")
    return render(request, 'main/profile.html', {"deposit": True, "money_form": form})


@user_is_authenticated()
def withdraw_money(request):
    form = MoneyForm(data=request.POST)
    if form.is_valid():
        request.user.data.money -= form.cleaned_data['money']
        request.user.data.save()
        return redirect("main:profile")
    return render(request, 'main/profile.html', {"withdraw": True, "money_form": form})


@user_is_authenticated()
def edit_user(request):
    form = EditUser(instance=request.user)

    if request.method == "POST":
        form = EditUser(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("main:profile")
    return render(request, 'main/profile.html', {"edit": True, "edit_form": form})


@user_is_authenticated()
def blacklist_user(request, other_user_id):
    blackList = BlackList()
    blackList.user = request.user
    other_user = User.objects.get(pk=other_user_id)
    blackList.blacklisted_user = other_user

    l = BlackList.objects.filter(user=request.user, blacklisted_user=other_user)

    if len(l) < 1:
        blackList.save()
    else:
        l.delete()

    return redirect(f'/main/profile/{other_user_id}/')
