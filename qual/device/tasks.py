from __future__ import absolute_import
from .models import Device, DeviceUser
from employee.models import Employee
from zk import ZK
from django.shortcuts import get_object_or_404


def add_user(employee_id, device_id):
    employee = get_object_or_404(Employee, id=employee_id)
    device = Device.objects.get(id=device_id)
    uid = DeviceUser.objects.filter(device=device).order_by("-uid").first().uid + 1
    device_connected = ZK(
        ip=device.ip,
        port=device.port,
        timeout=500,
    )
    device_connected.connect()
    device_connected.set_user(uid=uid, name=employee.name, user_id=employee.employee_id)
    device_connected.disconnect()


def get_users(id):
    device = get_object_or_404(Device, id=id)
    device_connected = ZK(
        ip=device.ip,
        port=device.port,
        timeout=120,
    )
    device_connected.connect()
    users = device_connected.get_users()
    for user in users:
        i = str(user.user_id).rjust(4, "0")
        emp = Employee.objects.get(employee_id=i)
        u, created = DeviceUser.objects.filter(
            device=device, employee=emp
        ).get_or_create(
            uid=user.uid,
            name=user.name,
            privilege=user.privilege,
            group_id=user.group_id,
            user_id=user.user_id,
            card=user.card,
            device=device,
            employee=emp,
        )
    device_connected.disconnect()
