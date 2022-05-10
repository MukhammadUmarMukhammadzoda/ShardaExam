from django.db import models

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
    name = models.CharField(max_length=50)
    result = models.FileField(upload_to='files')
    faculty = models.ManyToManyField('Specialization', related_name="subjects")
    group = models.ForeignKey('Group', on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='subject')
    def __str__(self):
        return self.name
    

class Group(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=50, null=True, blank=True, unique=True)
    year = models.CharField(max_length=20, null=True)
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
    subject = models.ManyToManyField(Subject, related_name='student')
    specializetion = models.ForeignKey(Specialization, on_delete=models.CASCADE)
    sgpa1 = models.FloatField()
    sgpa2 = models.FloatField()
    cgpa = models.FloatField()

    def __str__(self):
        return self.name

