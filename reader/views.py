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
            # return HttpResponseRedirect('success/')
            df = pd.read_excel('reader/destination/destination'+f.name)
            
            # if not Student.objects.filter(id=data2[0]).exists():
            #         obj = Student(id=data2[0], first_name=data2[1], last_name=data2[2], email=data2[3], gender=data2[4])
            # col1=data1[0]
            # if data1.loc[id] not in data2:
            # data3 = data1.copy(deep=True)
            # print(data1.columns)
            # print(data1['id'])
            # if  data3['id'] not in data1['id'] :
            objs = list()
            for index, row in df.iterrows():
                grade = Grade.objects.filter(code=row["grade"]).values("id")
                obj=Student(id=row["id"],first_name=row["first_name"],last_name=row["last_name"],email=row["email"],gender=row["gender"],grade_id =grade)
                objs.append(obj)

            # Student.objects.bulk_create(
            # Student(**vals) for vals in data1.to_dict('records')
            # )
            Student.objects.bulk_create(objs)

            object_list = Student.objects.all().values('id', 'first_name', 'last_name', 'email', 'gender', 'grade__code')
            return render(request,'reader/success.html',{'object_list':object_list})   


    else:
        form = UploadFileForm()
    return render(request, 'reader/upload.html', {'form': form})


# def success(request):
    
#     return render(request,'reader/success.html')



