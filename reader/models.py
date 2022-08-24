from django.db import models




class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length = 100)
    gender = models.CharField(max_length=10)

    def full_name(self):
        f"{self.first_name}+ {self.last_name}"

    def __str__(self):
        return self.full_name()