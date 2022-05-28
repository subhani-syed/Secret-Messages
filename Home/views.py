from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def home(request):
    cur_user = request.user
    context={
        "user_name":cur_user.username,
        "user_id":cur_user.id
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
            return redirect('/')
        else:
            return HttpResponse("Invalid Login")
    
    # GET
    return render(request,'login.html')

def logout_user(request):
    logout(request)
    return redirect('/')

def register(request):
    # POST
    if request.method == "POST":
        name = request.POST['name']
        password = request.POST['password']
        lname = request.POST['lname']
        fname = request.POST['fname']
        user = User.objects.create_user(username=name,password=password,last_name=lname,first_name=fname)
        user.save()
        return HttpResponse(f"User created with username-> {name} and password-> {password}")
    
    # GET
    return render(request,'register.html')
