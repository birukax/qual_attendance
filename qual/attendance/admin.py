from django.contrib import admin
from .models import Shift, Attendance, RawAttendance, Employee, Pattern

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['employee_id','name', 'shift', 'pattern', 'last_updated' ]
    search_fields = ['name',]


@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'continous', 'saturday_half']
    prepopulated_fields = {'slug': ('name',)}
    
@admin.register(Pattern)
class PatternAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'day_span', 'shift', 'next', 'start_time', 'end_time', 'tolerance']
    prepopulated_fields = {'slug': ('name',)}
    
@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['employee', 'device','current_pattern' ,'check_in_date' ,'check_in_time','check_out_date' ,'check_out_time']
    
@admin.register(RawAttendance)
class RawAttendanceAdmin(admin.ModelAdmin):
    list_display = ['uid', 'device','employee' ,'date','time' ,'status', 'punch']
    list_filter = ['employee', 'date']
    