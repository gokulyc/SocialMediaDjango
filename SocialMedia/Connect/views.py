# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse
from .forms import *


def Login(request):
    if request.user.is_authenticated:
        return redirect("UserProfile", request.user.username)

    form = AddUser_Form()
    error = False
    if request.method == "POST":
        un = request.POST["un"]
        ps = request.POST["ps"]
        usr = authenticate(username = un, password = ps)
        if usr != None:
            login(request, usr)
            return redirect("UserProfile", usr.username)
        error = True
    Dict = {
        "error":error, "form":form
    }
    return render(request, "login_register.html", Dict)

def logout_page(request):
    logout(request)
    return redirect('login')


def Register(request):
    if request.method == "POST":
        form = AddUser_Form(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            un = request.POST["un"]
            ps = request.POST["ps"]
            email = data.email

            usr = User.objects.create_user(un, email, ps)
            data.usr = usr
            data.save()
            return redirect("login")
    return HttpResponse("Register Your Self")


def UserProfile(request, Username):
    if not request.user.is_authenticated:
        return redirect('login')

    usr=User.objects.filter(username=Username)
    if not usr:
        return redirect("UserProfile", request.user.username)
    usr=usr[0]
    User_Detail = UserDataBase.objects.get(usr=usr)
    print(User_Detail)



    return render(request, "user_details.html",{'profile':User_Detail})

def Update_User_Details(request, Username):
    if not request.user.is_authenticated:
        return redirect('login')
    loggedin_user=request.user.username
    if Username!=loggedin_user:
        return redirect("UserProfile",loggedin_user)
    usr = User.objects.filter(username=Username)
    usr = usr[0]
    User_Detail = UserDataBase.objects.get(usr=usr)
    form=Edit_User_Form(request.POST or None,request.FILES or None,instance=User_Detail)

    if form.is_valid():
        form.save()
        redirect("UserProfile",loggedin_user)
    di={'profile': User_Detail,'form':form}

    return render(request, "edit_user_details.html",di)


