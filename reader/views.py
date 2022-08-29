# from urllib import request
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib import messages

from .forms import UploadFileForm   

import pandas as pd

from . models import *



def handle_uploaded_file(f):
    with open('reader/destination/destination'+f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            f=request.FILES['file']
            if not f.name.endswith('.xlsx'):
                messages.error(request,'Please insert Excel file')
                return redirect('home')
            handle_uploaded_file(f)
            
            # df = pd.read_excel('reader/destination/destination'+f.name)
            df = pd.read_excel('reader/destination/destination'+f.name)
            #--------------------------------------------------#--------------------------#
            #new codes
    
            
            
            
            
            import sqlite3

            connect2 = sqlite3.connect('db.sqlite3')
            df2 = pd.read_sql_query('Select * from reader_grade;',connect2)
            print(df2)
            new_data=pd.merge(df,df2,on="grade")
            print(new_data)
            df_records = new_data.to_dict('records')
            record_lists = [Student(
                id = record['id_x'],
                first_name=record['first_name'],
                last_name = record['last_name'],
                gender = record['gender'],
                grade_id = record['id_y'],
                ) for record in df_records]
            
            

            

            #--------------------------------------------------#--------------------------#
        
            # objs = list()
            # for index, row in df.iterrows():
            #     grade = Grade.objects.filter(code=row["grade"]).values("id")
            #     obj=Student(id=row["id"],first_name=row["first_name"],last_name=row["last_name"],email=row["email"],gender=row["gender"],grade_id =grade)
            #     objs.append(obj)
#--------------------------------------------#                             #----------------#

            # Student.objects.bulk_create(objs)    #-------->(objs)

            # object_list = Student.objects.all().values('id', 'first_name', 'last_name', 'email', 'gender', 'grade__code')
            # return render(request,'reader/success.html',{'object_list':object_list})   
            
            Student.objects.bulk_create(record_lists) 
            object_list = Student.objects.all().values('id', 'first_name', 'last_name', 'email', 'gender', 'grade__grade')
            return render(request,'reader/success.html',{'object_list':object_list})   


    else:
        form = UploadFileForm()
    return render(request, 'reader/upload.html', {'form': form})





