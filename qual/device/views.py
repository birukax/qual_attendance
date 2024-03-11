from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from zk import ZK
from .models import Device
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
import datetime
from datetime import time, date
from .forms import CreateDeviceForm
from django.utils.text import slugify
from django.contrib.postgres.search import SearchVector
import threading


@login_required
def devices(request):
    devices = Device.objects.all()
    create_device_form = CreateDeviceForm()
    return render(
        request,
        "device/list.html",
        {"devices": devices, "form": create_device_form},
    )


@login_required
def create_device(request):
    if request.method == "POST":
        form = CreateDeviceForm(data=request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            ip = form.cleaned_data["ip"]
            slug = slugify(name)
            Device.objects.create(name=name, ip=ip, slug=slug)

    return redirect("device:devices")


@login_required
def device_detail(request, id):
    device = get_object_or_404(Device, id=id)
    device_connected = ZK(
        ip=device.ip,
        port=device.port,
        timeout=50,
        # force_udp=True,
        # ommit_ping=True,
        # verbose=True,
    )
    device_connected.connect()
    device_time = device_connected.get_time()
    device_users = device_connected.get_users()
    paginated = Paginator(device_users, 10)
    page_number = request.GET.get("page")
    page = paginated.get_page(page_number)
    device_connected.disconnect()

    return render(
        request,
        "device/detail.html",
        {"device": device, "device_time": device_time, "page": page},
    )
