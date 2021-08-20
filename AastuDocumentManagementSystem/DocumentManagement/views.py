
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth
def index(request):
    return render(request,'index.html')

def signup(request):
    if request.method == "POST":
        if request.POST['password1'] == request.POST['password2']:
            try:
                User.objects.get(username = request.POST['username'])
                return render (request,'sign-up.html', {'error':'Username is already taken!'})
            except User.DoesNotExist:
                user = User.objects.create_user(request.POST['username'] , password=request.POST['password1'])
                auth.login(request,user)
                return redirect('/dms-app/index')
        else:
            return render (request,'sign-up.html', {'error':'Password does not match!'})
    else:
        return render(request,'sign-up.html')

def login(request):
    if request.method == 'POST':
        print("-------------------")
        print(request.POST['password1'])
        user = auth.authenticate(username=request.POST['username'], password = request.POST['password1'])
        if user is not None:
            auth.login(request,user)
            return redirect('/dms-app/index')
        else:
            return render (request,'sign-in.html', {'error':'Username or password is incorrect!'})
    else:
        return render(request,'sign-in.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
    return redirect('/dms-app/login')
