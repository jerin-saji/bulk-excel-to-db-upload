from django.db import models

class Grade(models.Model):
    grade = models.CharField(max_length=20)
    def __str__(self):
        return self.grade


class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length = 100)
    gender = models.CharField(max_length=10)
    grade = models.ForeignKey(Grade,on_delete=models.CASCADE,null=True,blank=True)

    def full_name(self):
        return(f"{self.first_name} {self.last_name}")
        

    def __str__(self):
        return self.full_name()



    # def __str__(self):
    #     return self.first_name