# Importing Essential libraries
from multiprocessing import context
from urllib.request import Request
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import *
from django.contrib.auth.forms import  UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import pandas as pd



#Index page that is responsible for first page of Website
def index(request):

    branch = Branch.objects.all()
    group = Group.objects.all()
    spec = Specialization.objects.all()

    context = {
        'branchs' : branch,
        'groups' : group,
        'specs' : spec
    }

    return render(request, 'index.html', context)




# Group Page to show groups among branches like btech or bba
def group(request, name, code):
    global group
    group = Group.objects.get(code = code)
    spec = Specialization.objects.filter(branch = group.course)
    search = request.GET.get('search')
    if search:
        search = search.capitalize()
        print(search)
        

        students = group.students.filter(name__startswith = search)
    else:
        students = group.students.all()

    return render(request, 'group.html', {"specs" : spec, 'students': students, 'group' : group})




# It will return filtered students who studies at specific branch
def spec(request, id):
    spec = Specialization.objects.get(id = id)
    search = request.GET.get('search')

    if search:
        search = search.capitalize()
        

        students = group.students.filter(name__startswith = search)
    else:
        students = group.students.all()

    students = group.students.filter(specializetion = spec)
    spec = Specialization.objects.filter(branch = group.course)

    return render(request, 'group.html', {'students' : students, 'specs' :spec}  )




# Login Page to use login part of website
def loginPage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return redirect('login')

    return render(request, 'login.html')





# Logout Page
def logoutPage(request):
    logout(request)
    return redirect('index')



# My subject Page is responsible for subjetcs which are teacher is belonged to
@login_required
def my_subjects(request):
    subject = Subject.objects.filter(teacher = request.user)

    context = {
        'subjects' : subject
    }

    return render(request, 'mysub.html', context)




# Result page is for Teacher to change marks of students
def result(request,code):
    result = Result.objects.filter(subject__code = code)
    subject = Subject.objects.get(code = code)
    students = Student.objects.filter(group__code = subject.group.code)
    sts = []
    facts = subject.faculty.all()
    for i in students:
        if i.specializetion in facts:
            sts.append(i)
            for rs in result:
                if rs.student.id == i.id:
                    sts.remove(i)
    students = sts
    context = {
        'results' : result,
        "code":code,
        'students' : students,
        'subject' : subject
    }

    if request.method == 'POST':
        try:
          filedata = request.FILES['myFile']
          if filedata:
            data = pd.DataFrame(pd.read_excel(filedata))
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
                    

        except:
           id = request.POST.get("re_id")
        
           if id:
             result = Result.objects.get(id = id)
             context["active"]=result
        return render(request,"result.html",context)


    return render(request, 'result.html', context)




# It will change student
def change_student(request,code):

    if request.method == 'POST':
        grade = request.POST['grade']
        grade = grade.upper()

        id = request.POST['re_id']
        if id != 'new':
            result = Result.objects.get(id = id)
            result.Assignments = request.POST['assigment']
            result.Mid_Term = request.POST['mid_term']
            result.End_Term = request.POST['end_term']
            result.Grade = grade
            result.save()
        else:
            result = Result.objects.create(
                subject=Subject.objects.get(code=code),
                student=Student.objects.get(id=request.POST['student_id']),
                Assignments = request.POST['assigment'],
                Mid_Term = request.POST['mid_term'],
                End_Term = request.POST['end_term'],
                Grade = grade
                )
        return redirect("result",code=code)




# Student info page is for getting info of student
def studentinfo(request, id , name):
    student = Student.objects.get(id = id)
    results = student.results.all()
    semesters = Semester.objects.all()
    context = {
        "results": results,
        "semesters": semesters,
        'student' : student
    }
    return render(request,"studentinfo.html", context)



