# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse
from .forms import *

from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template
from django.conf import settings

from django.db.models import Q

from SocialMedia.tasks import send_email_users


# def send_email_users(email_li, msg):
#     from_email = settings.EMAIL_HOST_USER
#     to_email = email_li
#     html = get_template("mail.html").render({'msg': msg})
#     # html = f'<h1>{msg}</h1>'
#     sub = 'Django test mail'
#     send_mail(sub, "", from_email, to_email, html_message=html)


def Login(request):
    if request.user.is_authenticated:
        return redirect("UserProfile", request.user.username)

    form = AddUser_Form()
    error = False
    if request.method == "POST":
        un = request.POST["un"]
        ps = request.POST["ps"]
        usr = authenticate(username=un, password=ps)
        if usr != None:
            login(request, usr)
            return redirect("UserProfile", usr.username)
        error = True
    Dict = {
        "error": error, "form": form
    }
    return render(request, "login_register.html", Dict)


def logout_page(request):
    logout(request)
    return redirect('login')


def Register(request):
    form = AddUser_Form(request.POST or None, request.FILES or None)
    error = ''
    if request.method == "POST":
        # form = AddUser_Form(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            un = request.POST["un"]
            ps = request.POST["ps"]
            email = data.email
            conpwd = request.POST["pwdconfirm"]

            existing_users = (user.username for user in User.objects.all())
            # print(existing_users)
            if ps != conpwd:
                error = "Passwords not matching ..!!"
            elif un in existing_users:
                print(list(User.objects.all()))
                error = "Username already exists !!!"
            elif error == '':
                usr = User.objects.create_user(un, email, ps)
                data.usr = usr
                data.save()
                return redirect("login")
            else:
                pass
            # return redirect("login")
    Dict = {"form": form, 'error': error}
    return render(request, "login_register.html", Dict)


def UserProfile(request, Username):
    if not request.user.is_authenticated:
        return redirect('login')

    usr = User.objects.filter(username=Username)
    if not usr:
        return redirect("UserProfile", request.user.username)
    connection = None
    if request.user.username != Username:
        user1 = User.objects.get(username=Username)
        user2 = User.objects.get(username=request.user.username)

        UData1 = UserDataBase.objects.get(usr=user1)
        UData2 = UserDataBase.objects.get(usr=user2)

        connection = Connections.objects.filter(
            Q(sender=UData1, receiver=UData2) | Q(sender=UData2, receiver=UData1))

        if len(connection) != 0:
            # print(connection)
            connection = connection[0]

    usr = usr[0]
    User_Detail = UserDataBase.objects.get(usr=usr)
    # print(User_Detail)
    blog_form = UserBlog_Form()

    all_posts = Blog_Model.objects.filter(usr=usr).order_by('-date')

    all_posts_like_luser = Post_Likes.objects.filter(usr=request.user)
    like_luser_bids = []
    for i in all_posts_like_luser:
        like_luser_bids.append(i.blog.id)

    # print('Debug: ',all_posts[0].post_likes_set.all(),all_posts[1].post_likes_set.all())
    # print('Debug: ',dir(all_posts[0]))

    di = {'profile': User_Detail,
          'connection': connection,
          'blog_form': blog_form,
          'all_posts': all_posts,
          'like_luser_bids': like_luser_bids,
          }

    return render(request, "user_details.html", di)


def like_post(request, b_id):
    if not request.user.is_authenticated:
        return redirect('login')

    blog = Blog_Model.objects.get(id=b_id)
    Post_Likes.objects.create(usr=request.user, blog=blog)
    uname = blog.usr.username
    # msg = f'{uname} post was liked,{blog.blog}'
    # send_email_users.delay(
    #     ['chaitanya1157@gmail.com', 'gokulyc@gmail.com'], msg)

    return redirect("UserProfile", uname)


def unlike_post(request, b_id):
    if not request.user.is_authenticated:
        return redirect('login')

    blog = Blog_Model.objects.get(id=b_id)
    uname = blog.usr.username
    obj = Post_Likes.objects.filter(Q(usr=request.user, blog=blog))
    obj.delete()
    # msg = f'{uname} post was liked,{blog.blog}'
    # send_email_users(['chaitanya1157@gmail.com', 'gokulyc@gmail.com'])

    return redirect("UserProfile", uname)


def Update_User_Details(request, Username):
    if not request.user.is_authenticated:
        return redirect('login')
    loggedin_user = request.user.username
    if Username != loggedin_user:
        return redirect("UserProfile", loggedin_user)
    usr = User.objects.filter(username=Username)
    usr = usr[0]
    User_Detail = UserDataBase.objects.get(usr=usr)
    form = Edit_User_Form(request.POST or None,
                          request.FILES or None, instance=User_Detail)

    if form.is_valid():
        form.save()
        redirect("UserProfile", loggedin_user)
    di = {'profile': User_Detail, 'form': form}

    return render(request, "edit_user_details.html", di)


def all_profession(request, d_type):
    if not request.user.is_authenticated:
        return redirect('login')

    logged_in_user = User.objects.get(username=request.user.username)
    me = UserDataBase.objects.get(usr=logged_in_user)

    # count

    con_req = len(Connections.objects.filter(receiver=me, status='Sent'))
    con_sent = len(Connections.objects.filter(sender=me, status='Sent'))
    con_friend = len(
        Connections.objects.filter(Q(sender=me, status='friend') | Q(receiver=me, status='friend')).order_by('-date'))

    # count

    data = []
    if d_type == 'all':
        print(d_type)
        data = UserDataBase.objects.all()
        d_num = len(data)
        # print(data)
    elif d_type == 'requests':
        print(d_type)
        requests = Connections.objects.filter(receiver=me, status='Sent')
        user_data = []
        for con in requests:
            ud = UserDataBase.objects.get(id=con.sender.id)
            user_data.append(ud)
        data = user_data
        d_num = len(data)
        # print(data)
    elif d_type == 'sent':
        print(d_type)
        sent = Connections.objects.filter(sender=me, status='Sent')
        user_data = []
        for con in sent:
            ud = UserDataBase.objects.get(id=con.receiver.id)
            user_data.append(ud)
        data = user_data
        d_num = len(data)
        # print(data)
    elif d_type == 'friends':
        print(d_type)
        friendscon = Connections.objects.filter(
            Q(sender=me, status='friend') | Q(receiver=me, status='friend')).order_by('-date')
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
    di = {
        'all_users': data, 'd_type': d_type, 'd_num': d_num, 'con_req': con_req, 'con_sent': con_sent,
        'con_friend': con_friend,
    }
    return render(request, 'professionals.html', di)


def all_profession_html(request, d_type):
    if not request.user.is_authenticated:
        return redirect('login')
    test = ''

    logged_in_user = User.objects.get(username=request.user.username)
    me = UserDataBase.objects.get(usr=logged_in_user)
    test = str(me.sender.all()) + str(me.receiver.all())
    # count

    con_req = len(Connections.objects.filter(receiver=me, status='Sent'))
    con_sent = len(Connections.objects.filter(sender=me, status='Sent'))
    con_friend = len(
        Connections.objects.filter(Q(sender=me, status='friend') | Q(receiver=me, status='friend')).order_by('-date'))

    # count

    data = []
    if d_type == 'all':
        print(d_type)
        data = UserDataBase.objects.all()
        d_num = len(data)
        # print(data)
    elif d_type == 'requests':
        print(d_type)
        requests = Connections.objects.filter(receiver=me, status='Sent')
        user_data = []
        for con in requests:
            ud = UserDataBase.objects.get(id=con.sender.id)
            user_data.append(ud)
        data = user_data
        d_num = len(data)
        # print(data)
    elif d_type == 'sent':
        print(d_type)
        sent = Connections.objects.filter(sender=me, status='Sent')
        user_data = []
        for con in sent:
            ud = UserDataBase.objects.get(id=con.receiver.id)
            user_data.append(ud)
        data = user_data
        d_num = len(data)
        # print(data)
    elif d_type == 'friends':
        print(d_type)
        friendscon = Connections.objects.filter(
            Q(sender=me, status='friend') | Q(receiver=me, status='friend')).order_by('-date')
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
    di = {
        'all_users': data, 'd_type': d_type, 'd_num': d_num, 'con_req': con_req, 'con_sent': con_sent,
        'con_friend': con_friend, 'test': test
    }
    return render(request, 'professionals_html.html', di)


def manage_your_connection(request, action, u_id):
    if not request.user.is_authenticated:
        return redirect('login')
    # print(action,u_id)
    if action == "Send_Request":
        sender_user = User.objects.get(username=request.user.username)
        sender = UserDataBase.objects.get(usr=sender_user)
        receiver = UserDataBase.objects.get(id=u_id)
        Connections.objects.create(sender=sender, receiver=receiver)
        return redirect('UserProfile', receiver.usr.username)
    if action == 'Accept_Request' or action == "Reject_Request":
        receive_user = User.objects.get(username=request.user.username)
        receiver = UserDataBase.objects.get(usr=receive_user)
        sender = UserDataBase.objects.get(id=u_id)
        con = Connections.objects.filter(sender=sender, receiver=receiver)
        if con:
            for c in con:
                if action == "Accept_Request":
                    c.status = "friend"
                    c.save()
                elif action == "Reject_Request":
                    c.status = "rejected"
                    c.save()
        return redirect('professional', "all")

    return HttpResponse("<h1>manage_your_connection</h1>")


def Register_Company(request):
    if not request.user.is_authenticated:
        return redirect('login')
    c_obj = Company_Model.objects.get(usr=request.user)
    form = Register_Company_Form(
        request.POST or None, request.FILES or None, instance=c_obj)
    if request.method == "POST":
        # form = Register_Company_Form(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            Map_str = data.map_embed
            if 'width="600"' in Map_str:
                t = Map_str.split('width="600"')
                Map_str = 'width="100%"'.join(t)
                data.map_embed = Map_str

            data.usr = request.user
            data.save()
            return redirect('login')
    # print(special_dir(form))

    di = {'form': form}
    return render(request, 'register_company.html', di)


def company_details(request):
    if not request.user.is_authenticated:
        return redirect('login')
    usr = request.user
    company = Company_Model.objects.filter(usr=usr)
    if not company:
        return redirect('login')
    # print('debug:',company[0].name)
    di = {'company': company.first()}

    return render(request, 'companies-detail.html', di)


def newpost(request):
    if not request.user.is_authenticated:
        return redirect('login')
    # blog_form = UserBlog_Form()
    if request.method == "POST":
        form = UserBlog_Form(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.usr = request.user
            data.save()
            print('Debug: Blog Submitted')
    return redirect("login")

# def special_dir(obj):
#     li=dir(obj)
#     # li=li.copy()
#     for i in li.copy():
#         if i[0]!='_':
#             del i
#     return obj
