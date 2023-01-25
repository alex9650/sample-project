import uuid

from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import *
from .models import *
from django.core.mail import send_mail
from emailpro.settings import EMAIL_HOST_USER
from django.contrib import messages
from django.contrib.auth import authenticate


def regis(request):
    a=register()
    return render(request,'register.html',{'form':a})

def email_send(request):
    a=ContactusForm()
    if request.method=='POST':
        sub=ContactusForm(request.POST)
        if sub.is_valid():
            nm=sub.cleaned_data['Name']
            em=sub.cleaned_data['Email']
            ms=sub.cleaned_data['Message']
            send_mail(str(nm)+"||"+"TCS",ms,EMAIL_HOST_USER,[em])
            # send_mail(subject,message,EMAIL_HOST_USER,[EMAIL])
        return render(request,'success.html')

    return render(request,'email.html',{'form':a})

def regist(request):
    b=profile()
    if request.method=='POST':
        username=request.POST.get('username')
        password = request.POST.get('password')
        email= request.POST.get('email')
        if User.objects.filter(username=username).first():
            messages.success(request,'username already taken')
            return redirect(regist)
        if User.objects.filter(email=email).first():
            messages.success(request,'email already exist')
            return redirect(regist)
        user_obj=User(username=username,email=email)
        user_obj.set_password(password)
        user_obj.save()
        auth_token=str(uuid.uuid4())
        profile_obj=profile.objects.create(user=user_obj,auth_token=auth_token)
        profile_obj.save()
        send_mail_regist(email,auth_token)
        return render(request,'success.html')
    return render(request, 'regi.html', {'model': b})

def send_mail_regist(email,auth_token):
    subject="your account has been verified"
    message=f'paste the link to verify your account  http://127.0.0.1:8000/emailapp/verify/{auth_token}'
    email_from=EMAIL_HOST_USER
    recipient=[email]
    send_mail(subject,message,email_from,recipient)

def verify(request,auth_token):
    profile_obj=profile.objects.filter(auth_token=auth_token).first()
    if profile_obj:
        if profile_obj.is_verified:
            messages.success(request,'your account is already verified')
            return redirect(login)
        profile_obj.is_verified=True
        profile_obj.save()
        messages.success(request,'your account has been verified')
        return redirect(login)
    else:
        messages.success(request,"user not found")
        return redirect(login)

def login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user_obj=User.objects.filter(username=username).first()

        if user_obj is None:
            messages.success(request,'user not found')
            return redirect(login)
        profile_obj=profile.objects.filter(user=user_obj).first()
        if not profile_obj.is_verified:
            messages.success(request,'profile not verified check your mail')
            return redirect(login)
        user=authenticate(username=username,password=password)

        if user is None:
            messages.success(request,'wrong password or username')
            return redirect(login)
        return HttpResponse("success")

    return render(request,'login.html')