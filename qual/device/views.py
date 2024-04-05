from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from zk import ZK
from attendance.models import RawAttendance
from .models import Device, DeviceUser
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import CreateDeviceForm, AddDeviceUserForm
from django.utils.text import slugify
from .tasks import add_user, get_users
from datetime import datetime


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
    device_serialnumber = device_connected.get_serialnumber()
    device_mac = device_connected.get_mac()
    device_version = device_connected.get_firmware_version()
    device_connected.disconnect()
    users = DeviceUser.objects.filter(device=device)
    attendances = RawAttendance.objects.filter(device=device)
    context = {
        "device": device,
        "users": users,
        "attendances": attendances,
        "device_time": device_time,
        "device_serialnumber": device_serialnumber,
        "device_mac": device_mac,
        "device_version": device_version,
    }
    return render(
        request,
        "device/detail.html",
        context,
    )


@login_required
def device_users(request, id):
    device = get_object_or_404(Device, id=id)
    users = DeviceUser.objects.filter(device=device).order_by("name")
    attendances = RawAttendance.objects.filter(device=device)
    paginated = Paginator(users, 10)
    page_number = request.GET.get("page")
    page = paginated.get_page(page_number)
    context = {
        "device": device,
        "users": users,
        "attendances": attendances,
        "page": page,
    }

    return render(request, "device/user/list.html", context)


@login_required
def add_employee(request, id):
    if request.method == "POST":
        form = AddDeviceUserForm(data=request.POST)
        if form.is_valid():
            device_id = form.cleaned_data["device"].id

            if DeviceUser.objects.filter(employee_id=id, device_id=device_id):
                print("user exists!")
                return redirect("employee:employee_detail", id=id)
            else:
                print("adding user to device")
                add_user.delay(id, device_id)
                get_users.delay(id=device_id)
    return redirect("employee:employee_detail", id=id)


@login_required
def sync_users(request, id):
    get_users.delay(id)
    return redirect("device:device_detail", id=id)


@login_required
def sync_time(request, id):
    device = get_object_or_404(Device, id=id)
    device_connected = ZK(
        ip=device.ip,
        port=device.port,
        timeout=50,
        # force_udp=True,
        # ommit_ping=True,
        # verbose=True,
    )
    time = datetime.now()
    print(time)
    try:
        device_connected.connect()
        device_connected.set_time(time)
        device_connected.disconnect()
    except Exception as e:
        print("error: ", e)
    return redirect("device:device_detail", id=id)
