from enum import unique
from turtle import title
from django import forms
from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect, render
import csv
import pandas as pd
from .models import *
# Register your models here.

admin.site.register(Group)
# admin.site.register(Subject)
admin.site.register(Branch)
admin.site.register(Semester)
admin.site.register(Specialization)
# admin.site.register(Student)
admin.site.register(Result)



# @admin.register(Student)
# class StudentAdmin(admin.ModelAdmin):
#     list_display = [
#         "name",
#     "unique_id",
#     "group",
#     "specializetion",
#     "cgpa",
#     "sgpa",
#         ]
#     list_filter=['group', 'specializetion']


class CsvImportForm(forms.Form):
    csv_file = forms.FileField()

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

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('upload-csv/', self.upload_csv),
        ]
        return my_urls + urls

    def upload_csv(self, request):
        if request.method == "POST":
            excel_file = request.FILES["csv_file"]
            data = pd.DataFrame(pd.read_excel(excel_file))
            data = data.reset_index()
            for index, row in data.iterrows():
                group = Group.objects.filter(name=row['group (programm-term)']).first()
                spec = Specialization.objects.filter(name=row['specialization']).first()
                obj, created = Student.objects.get_or_create(
                    name=row['Full name'],
                    unique_id=row['Unique ID'],
                    group=group,
                    specializetion=spec
                )
            self.message_user(request, "Your csv file has been imported")
            return redirect("/admin/main/student/")
        form = CsvImportForm()
        return render(request, 'admin/csv_upload.html', {"form": form})



@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('upload-subject-csv/', self.upload_csv),
        ]
        return my_urls + urls

    def upload_csv(self, request):
        if request.method == "POST":
            excel_file = request.FILES["csv_file"]
            data = pd.DataFrame(pd.read_excel(excel_file))
            data = data.reset_index()
            for index, row in data.iterrows():
                teacher = User.objects.filter(username = row['teacher']).first()
                group = Group.objects.filter(name=row['group(pro-term)']).first()
                semester = Semester.objects.filter(year = int(row['semester'])).first()
                specs_data = row['specialization'].split(",")
                specs = [Specialization.objects.filter(name=spec.strip()).first() for spec in specs_data]
                obj, created = Subject.objects.get_or_create(
                    code=row['code'],
                    title=row['title'],
                    group=group,
                    semester = semester,
                    teacher = teacher,
                    credit =  row['credit']
                )
                if created:
                    for spec in specs:
                        obj.faculty.add(spec)
                    obj.save()
                    
            self.message_user(request, "Your csv file has been imported")
            return redirect("/admin/main/subject/")
        form = CsvImportForm()
        return render(request, 'admin/csv_upload.html', {"form": form})

admin.site.register(File)

