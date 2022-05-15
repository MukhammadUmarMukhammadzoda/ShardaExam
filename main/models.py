from django.db import models
from django.contrib.auth.models import AbstractUser, User

# Create your models here.

class Branch(models.Model):

    name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name




class Semester(models.Model):
    year = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.year}'



class Subject(models.Model):
    code = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=50, blank=True, null=True)
    faculty = models.ManyToManyField('Specialization', related_name="subjects")
    group = models.ForeignKey('Group', on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='subject')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    credit = models.PositiveIntegerField(null=True)
    def __str__(self):
        return self.title
    

class Group(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=50, null=True, blank=True, unique=True)
    course = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='groups')
    isarchive = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}-{self.code}'



class Specialization(models.Model):
    name = models.CharField(max_length=100, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='faculty', null=True)
    def __str__(self):
        return self.name 


class Student(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    unique_id = models.CharField(max_length=100, blank=True, null=True)
    group = models.ForeignKey(Group, on_delete=models.DO_NOTHING,related_name="students")
    specializetion = models.ForeignKey(Specialization, on_delete=models.CASCADE)
    cgpa = models.FloatField(null=True, blank=True)
    sgpa = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name


class Result(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, related_name='results')
    Assignments = models.PositiveIntegerField(null=True)
    Mid_Term = models.PositiveIntegerField(null=True)
    End_Term = models.PositiveIntegerField(null=True)
    Grade = models.CharField(max_length=5, null=True, blank=True)

    def __str__(self):
        return self.student.name


    

