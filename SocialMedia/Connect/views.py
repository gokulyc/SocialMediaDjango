# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse
from .forms import *

from django.db.models import Q


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
    connection=None
    if request.user.username != Username:
        user1=User.objects.get(username=Username)
        user2=User.objects.get(username=request.user.username)

        UData1=UserDataBase.objects.get(usr=user1)
        UData2 = UserDataBase.objects.get(usr=user2)

        connection=Connections.objects.filter(Q(sender=UData1,receiver=UData2)|Q(sender=UData2,receiver=UData1))

        if len(connection)!=0:
            # print(connection)
            connection=connection[0]
            # print(connection)



    # sent_con=Connections.objects.filter(sender=request.user.id)
    # received_con=Connections.objects.filter(receiver=request.user.id)
    # print(sent_con,received_con)
    # sent_

    usr=usr[0]
    User_Detail = UserDataBase.objects.get(usr=usr)
    # print(User_Detail)



    return render(request, "user_details.html",{'profile':User_Detail,'connection':connection})

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

def all_profession(request, d_type):
    if not request.user.is_authenticated:
        return redirect('login')

    logged_in_user=User.objects.get(username=request.user.username)
    me=UserDataBase.objects.get(usr=logged_in_user)

    # count

    con_req = len(Connections.objects.filter(receiver=me, status='Sent'))
    con_sent= len(Connections.objects.filter(sender=me, status='Sent'))
    con_friend=len(Connections.objects.filter(Q(sender=me, status='friend')|Q(receiver=me, status='friend')).order_by('-date'))

    # count

    data=[]
    if d_type== 'all':
        print(d_type)
        data = UserDataBase.objects.all()
        d_num=len(data)
        # print(data)
    elif d_type== 'requests':
        print(d_type)
        requests=Connections.objects.filter(receiver=me,status='Sent')
        user_data=[]
        for con in requests:
            ud=UserDataBase.objects.get(id= con.sender.id)
            user_data.append(ud)
        data = user_data
        d_num = len(data)
        # print(data)
    elif d_type== 'sent':
        print(d_type)
        sent = Connections.objects.filter(sender=me, status='Sent')
        user_data=[]
        for con in sent:
            ud=UserDataBase.objects.get(id= con.receiver.id)
            user_data.append(ud)
        data=user_data
        d_num = len(data)
        # print(data)
    elif d_type== 'friends':
        print(d_type)
        friendscon = Connections.objects.filter(Q(sender=me, status='friend')|Q(receiver=me, status='friend')).order_by('-date')
        print(friendscon)
        user_data = []
        for con in friendscon:
            # if con.sender==me
            ud = UserDataBase.objects.get(id=con.sender.id)
            if ud.id != me.id:
                user_data.append(ud)
            ud = UserDataBase.objects.get(id=con.receiver.id)
            if ud.id != me.id:
                user_data.append(ud)
            # print(ud)
        data = user_data
        d_num = len(data)
        # print(data)
        # data=Connections.objects.filter(Q(sender=me,status='friend')|Q(receiver=me,status='friend')).order_by('-date')
    # all_users=UserDataBase.objects.all()
    di={
        'all_users':data,'d_type':d_type,'d_num':d_num,'con_req':con_req,'con_sent':con_sent,'con_friend':con_friend,
    }
    return render(request,'professionals.html',di)

def all_profession_html(request, d_type):
    if not request.user.is_authenticated:
        return redirect('login')
    test=''

    logged_in_user=User.objects.get(username=request.user.username)
    me=UserDataBase.objects.get(usr=logged_in_user)
    test=str(me.sender.all())+str(me.receiver.all())
    # count

    con_req = len(Connections.objects.filter(receiver=me, status='Sent'))
    con_sent= len(Connections.objects.filter(sender=me, status='Sent'))
    con_friend=len(Connections.objects.filter(Q(sender=me, status='friend')|Q(receiver=me, status='friend')).order_by('-date'))

    # count

    data=[]
    if d_type== 'all':
        print(d_type)
        data = UserDataBase.objects.all()
        d_num=len(data)
        # print(data)
    elif d_type== 'requests':
        print(d_type)
        requests=Connections.objects.filter(receiver=me,status='Sent')
        user_data=[]
        for con in requests:
            ud=UserDataBase.objects.get(id= con.sender.id)
            user_data.append(ud)
        data = user_data
        d_num = len(data)
        # print(data)
    elif d_type== 'sent':
        print(d_type)
        sent = Connections.objects.filter(sender=me, status='Sent')
        user_data=[]
        for con in sent:
            ud=UserDataBase.objects.get(id= con.receiver.id)
            user_data.append(ud)
        data=user_data
        d_num = len(data)
        # print(data)
    elif d_type== 'friends':
        print(d_type)
        friendscon = Connections.objects.filter(Q(sender=me, status='friend')|Q(receiver=me, status='friend')).order_by('-date')
        print(friendscon)
        user_data = []
        for con in friendscon:
            # if con.sender==me
            ud = UserDataBase.objects.get(id=con.sender.id)
            if ud.id != me.id:
                user_data.append(ud)
            ud = UserDataBase.objects.get(id=con.receiver.id)
            if ud.id != me.id:
                user_data.append(ud)
            # print(ud)
        data = user_data
        d_num = len(data)
        # print(data)
        # data=Connections.objects.filter(Q(sender=me,status='friend')|Q(receiver=me,status='friend')).order_by('-date')
    # all_users=UserDataBase.objects.all()
    di={
        'all_users':data,'d_type':d_type,'d_num':d_num,'con_req':con_req,'con_sent':con_sent,'con_friend':con_friend,'test':test
    }
    return render(request,'professionals_html.html',di)

def manage_your_connection(request,action,u_id):
    if not request.user.is_authenticated:
        return redirect('login')
    # print(action,u_id)
    if action=="Send_Request":
        sender_user=User.objects.get(username=request.user.username)
        sender=UserDataBase.objects.get(usr=sender_user)
        receiver=UserDataBase.objects.get(id=u_id)
        Connections.objects.create(sender=sender,receiver=receiver)
        return redirect('UserProfile',receiver.usr.username)
    if action=='Accept_Request' or action == "Reject_Request":
        receive_user = User.objects.get(username=request.user.username)
        receiver = UserDataBase.objects.get(usr=receive_user)
        sender = UserDataBase.objects.get(id=u_id)
        con = Connections.objects.filter(sender=sender, receiver=receiver)
        if con:
            for c in con:
                if action=="Accept_Request":
                    c.status="friend"
                    c.save()
                elif action=="Reject_Request":
                    c.status="rejected"
                    c.save()
        return redirect('professional', "all")




    return HttpResponse("<h1>manage_your_connection</h1>")

def Register_Company(request):
    if not request.user.is_authenticated:
        return redirect('login')
    # loggedin_user = request.user.username
    # if Username != loggedin_user:
    #     return redirect("UserProfile", loggedin_user)
    # usr = User.objects.filter(username=Username)
    # usr = usr[0]
    # User_Detail = UserDataBase.objects.get(usr=usr)

    form = RegisterCompany_Form(request.POST or None, request.FILES or None)

    di={'form':form}
    return render(request,'register_company.html',di)





