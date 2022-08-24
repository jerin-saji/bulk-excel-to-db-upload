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
            data1 = pd.read_excel('reader/destination/destination'+f.name)
            print(type(data1))
            print (data1)
            data2 = data1.to_html()
            
            Student.objects.bulk_create(
            Student(**vals) for vals in data1.to_dict('records')
            )

            # l1 = list()
            # for row in data1.iteritems():
            #     r1 = list()
            #     for cell in row:
            #         r1.append(cell)
            #     l1.append(r1)



            return HttpResponse(data2)
            # return render(request,'reader/success.html',{'data':data2})


    else:
        form = UploadFileForm()
    return render(request, 'reader/upload.html', {'form': form})


# def success(request):
    
#     return render(request,'reader/success.html')



