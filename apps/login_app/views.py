from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
import bcrypt

from .models import User

def root(request):
    return render(request,'login_app/root_page.html')

def login_page(request):
    return render(request,'login_app/login_page.html')

def logout(request):
    request.session.clear()
    return redirect("/")

def login(request):
    user= User.objects.get(email=request.POST["login_email"])
    if bcrypt.checkpw(request.POST['login_password'].encode(), user.password.encode()):
        request.session["first_name"]=user.first_name
        request.session["email"]=request.POST['login_email']
        return redirect("/success")
    else:
        messages.error(request,"Wrong Password",extra_tags="wrong_password")
        return redirect("/")

def register(request):
    errors = User.objects.basic_validation(request.POST)
    if len(errors)>0:
        for key,value in errors.items():
            messages.error(request,value,extra_tags=key)
        return redirect ("/")
    else:
        # PASSWORD HASHING
        form_password = request.POST["password"]
        password_hash=bcrypt.hashpw(form_password.encode(),bcrypt.gensalt())
        request.session["first_name"]=request.POST['first_name']
        request.session["email"]=request.POST['email']
        User.objects.create(first_name=request.POST["first_name"],last_name=request.POST["last_name"],email=request.POST["email"],password=password_hash)
        return redirect("/success")
