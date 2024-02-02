from django.contrib import admin
from .models import Device, Shift, Attendance, RawAttendance, Employee, Pattern

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['employee', 'device','current_pattern' ,'check_in_date' ,'check_in_time','check_out_date' ,'check_out_time']
    
@admin.register(RawAttendance)
class RawAttendanceAdmin(admin.ModelAdmin):
    list_display = ['uid', 'device','employee' ,'date','time' ,'status', 'punch']
    list_filter = ['employee', 'date']
