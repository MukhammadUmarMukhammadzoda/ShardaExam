from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Group)
admin.site.register(Subject)
admin.site.register(Branch)
admin.site.register(Semester)
admin.site.register(Specialization)
# admin.site.register(Student)
admin.site.register(Result)



@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = [
        "name",
    "unique_id",
    "group",
    "specializetion",
    "cgpa",
    "sgpa",
        ]
    list_filter=['group', 'specializetion']

admin.site.register(File)