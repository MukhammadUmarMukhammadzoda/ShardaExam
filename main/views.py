from django.shortcuts import redirect, render
from .models import *
from .serializers import *
from django.contrib.auth.forms import  UserCreationForm
from django.contrib.auth import authenticate, login, logout


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
