from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Group)
admin.site.register(Subject)
admin.site.register(Branch)
admin.site.register(Semester)
admin.site.register(Specialization)
admin.site.register(Student)