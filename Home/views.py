from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from Home.models import Message
import datetime
import hashlib
from django.contrib import messages

# Create your views here.

@login_required
def home(request):
    cur_user = request.user
    context={   
        "user_name":cur_user.username,
        "user_id":cur_user.id,
        'msgs':reversed(Message.objects.filter(uid = int_to_hash(cur_user.id))),
        'hvalue':int_to_hash(cur_user.id),
    }
    return render(request,'home.html',context)

def login_user(request):
    # POST
    if request.method == "POST":
        name = request.POST['name']
        password = request.POST['password']
        user = authenticate(request,username=name,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,"Successfully Logged In")
            return redirect('/')
        else:
            messages.error(request,"Invalid User")
            return redirect('/')
    
    # GET
    if request.user.is_authenticated:
        return redirect('/')
    else:
        return render(request,'login.html')

def logout_user(request):
    logout(request)
    return redirect('/')

def register(request):
    # POST
    if request.method == "POST":
        name = request.POST['name']
        password = request.POST['password']
        user = User.objects.create_user(username=name,password=password)
        user.save()
        messages.success(request,"User Created Successfully")
        return redirect("/")
    
    # GET
    return render(request,'register.html')


def send_message(request,u_id):
    
    # To Find The Username from Link
    obj = User.objects.all()
    out=""
    for x in obj:
        if int_to_hash(x.id) == u_id:
            out = x.username

    # Check if the slug is valid or not
    if(out!=""): #Valid Slug
        if out == request.user.username: # Logged In User has same Link
            return redirect("/")
        else: #Different User

            # POST
            if request.method == "POST":
                body = request.POST['body']
                time = datetime.datetime.now()+datetime.timedelta(hours=5.5)
                # Incoming url has hash value
                msg = Message(body=body,time=time,uid=u_id)
                msg.save()
                messages.success(request,"Message Sent Successfully")
                return render(request,'sent.html')

            # GET
            return render(request,'message.html',{'uname':out,})
    else: #Invalid Slug
        messages.error(request,"Invalid link")
        return redirect("/")
    
# Converts Int to Hash Value
def int_to_hash(inp):
    str_inp = f"{inp}"
    return hashlib.md5(str_inp.encode()).hexdigest()