from django.shortcuts import render
from .forms import *
from django.http import HttpResponse
import os
from Tjlg.settings import MEDIA_ROOT
# Create your views here.
def tests(request):
    if request.method=='GET':
        register_form=RegisterForm()
        return render(request,'form.html',{'form':register_form})
    else:
        register_form=RegisterForm(request.POST or None,request.FILES or None)
        if register_form.is_valid():
            myFile = register_form.cleaned_data['image']
            destination = open(os.path.join(MEDIA_ROOT+"/img", myFile.name), 'wb+')
            for chunk in myFile.chunks():
                destination.write(chunk)
            destination.close()
            return HttpResponse('username:'+register_form.cleaned_data['username']+'&password:'+register_form.cleaned_data['password']+'&email:'+register_form.cleaned_data['email']+str(register_form.cleaned_data["image"]))
        else:
            return render(request, 'form.html', {'form': register_form})