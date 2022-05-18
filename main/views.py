from multiprocessing import context
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import *
from django.contrib.auth.forms import  UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

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



def group(request, name, code):
    global group
    group = Group.objects.get(code = code)
    spec = Specialization.objects.filter(branch = group.course)

    search = request.GET.get('search')
    if search:
        search = search.capitalize()
        

        students = group.students.filter(name = search)
    else:
        students = group.students.all()

    return render(request, 'group.html', {"specs" : spec, 'students': students, 'group' : group})



def spec(request, id):
    spec = Specialization.objects.get(id = id)
    subjects = Subject.objects.filter(faculty = spec, group = group)

    return render(request, 'subject.html', {'subjects' : subjects}  )



def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    context = {
        'form' : form
    }
    return render(request, 'signup.html', context)





def loginPage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('index')

    return render(request, 'login.html')


def logoutPage(request):
    logout(request)
    return redirect('index')



@login_required
def my_subjects(request):
    subject = Subject.objects.filter(teacher = request.user)

    context = {
        'subjects' : subject
    }

    return render(request, 'mysub.html', context)







def result(request,code):
    result = Result.objects.filter(subject__code = code)
    for r in result:
        u = r.Assignments+r.Mid_Term+r.End_Term
        if u >= 80:
            r.Grade = "A"
        elif u >= 70:
            r.Grade = "B"
        elif u >= 60:
            r.Grade = "C"
        elif u >= 50:
            r.Grade = "D"
        else:
            r.Grade = "F"
        r.save()
    context = {
        'results' : result,
        "code":code,
    }

    if request.method == 'POST':
        id = request.POST.get("re_id")
        print(id)
        result = Result.objects.get(id = id)
        context["active"]=result
        return render(request,"result.html",context)


    return render(request, 'result.html', context)

def change_student(request,code):

    if request.method == 'POST':
        id = request.POST['re_id']
        result = Result.objects.get(id = id)
        result.Assignments = request.POST['assigment']
        result.Mid_Term = request.POST['mid_term']
        result.End_Term = request.POST['end_term']
        result.save()
    
        return redirect("result",code=code)


def studentinfo(request, id , name):
    student = Student.objects.get(id = id)
    results = student.results.all()
    DATA = {
        "s1":[],
        "s2":[],
        "s3":[],
        "s4":[],
        "s5":[],
        "s6":[],
        "s7":[],
        "s8":[],
        "student":student,
        "results":results,
    }
    for i in range(1,9):
        for r in results:
            if int(r.subject.semester.year) == i:
                DATA[f's{i}'].append(r)

    return render(request,"studentinfo.html",DATA)