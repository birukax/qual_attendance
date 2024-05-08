from django.shortcuts import render, render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.core.paginator import Paginator
from .forms import (
    CreateUserForm,
    EditForm,
    EditProfileForm,
    EditUserForm,
    SelectDeviceForm,
)
from employee.models import Employee, Department
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test


@login_required
@user_passes_test(lambda u: u.profile.role == "ADMIN")
def create_user(request):
    if request.method == "POST":
        user_form = CreateUserForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data["password"])
            new_user.save()
            new_profile = Profile(user=new_user)
            new_profile.save()
            return redirect(
                "account:users",
            )
        else:
            print(user_form.errors)
            return redirect("account:create_user")
    else:
        form = CreateUserForm()
        context = {"form": form}
        return render(request, "user/create.html", context)


@login_required
@user_passes_test(lambda u: u.profile.role == "ADMIN")
def edit_user(request, id):
    if request.method == "POST":
        form = EditUserForm(request.POST)
        user = get_object_or_404(Profile, id=id)
        if not user.id == request.user.profile.id:
            if form.is_valid():
                user.user.email = form.cleaned_data["email"]
                user.user.first_name = form.cleaned_data["first_name"]
                user.user.last_name = form.cleaned_data["last_name"]
                user.user.is_active = form.cleaned_data["is_active"]
                user.save()
        return redirect("account:user_detail", id=id)


@login_required
@user_passes_test(lambda u: u.profile.role == "ADMIN")
def edit_profile(request, id):
    if request.method == "POST":
        form = EditProfileForm(request.POST)
        user = get_object_or_404(Profile, id=id)
        if not user.id == request.user.profile.id:
            if form.is_valid():
                user.role = form.cleaned_data["role"]
                user.device = form.cleaned_data["device"]
                user.manages.set(form.cleaned_data["manages"])
                user.employee = form.cleaned_data["employee"]
                user.save()

        return redirect("account:user_detail", id=id)


@login_required
@user_passes_test(lambda u: u.profile.role == "ADMIN")
def users(request):
    if request.user.is_superuser:
        users = User.objects.all()
    else:
        users = User.objects.filter(is_superuser=False)
    users = users.prefetch_related().exclude(id=request.user.id).order_by("id")
    paginated = Paginator(users, 20)
    page_number = request.GET.get("page")

    page = paginated.get_page(page_number)
    context = {"page": page}
    return render(request, "user/list.html", context)


@login_required
@user_passes_test(lambda u: u.profile.role == "ADMIN")
def user_detail(request, id):
    user = get_object_or_404(Profile, id=id)
    edit_user_form = EditUserForm(instance=user.user)
    edit_profile_form = EditProfileForm(instance=user)
    manages = user.manages.all().values("name")
    context = {
        "user": user,
        "manages": manages,
        "edit_user_form": edit_user_form,
        "edit_profile_form": edit_profile_form,
    }
    return render(request, "user/detail.html", context)


@login_required
def edit(request, id):
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            user = get_object_or_404(User, id=id)
            user.email = form.cleaned_data["email"]
            user.first_name = form.cleaned_data["first_name"]
            user.last_name = form.cleaned_data["last_name"]
            user.device = form.cleaned_data["device"]
            user.save()
        return redirect("account:profile_detail")


@login_required
@user_passes_test(lambda u: u.profile.role == "ADMIN" or u.profile.role == "HR")
def select_device(request):
    if request.method == "POST":
        form = SelectDeviceForm(request.POST)
        if form.is_valid():
            user = get_object_or_404(Profile, id=request.user.profile.id)
            user.device = form.cleaned_data["device"]
            user.save()
    return redirect("account:profile_detail")


@login_required
def profile_detail(request):
    user = get_object_or_404(Profile, id=request.user.profile.id)
    form = EditForm(instance=user.user)
    select_device_form = SelectDeviceForm(instance=user)

    manages = user.manages.all().values("name")

    context = {
        "user": user,
        "manages": manages,
        "form": form,
        "select_device_form": select_device_form,
    }
    return render(request, "user/profile/detail.html", context)
