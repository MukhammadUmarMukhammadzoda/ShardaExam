from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from .models import *
from rest_framework import generics
from .serializers import *



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


class API(generics.ListCreateAPIView):
     queryset = Group.objects.all()
     serializer_class = GroupSerializer


def spec(request, id):
    spec = Specialization.objects.get(id = id)
    subjects = Subject.objects.filter(faculty = spec, group = group)

    return render(request, 'subject.html', {'subjects' : subjects}  )

