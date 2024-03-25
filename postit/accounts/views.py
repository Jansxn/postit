from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages

def signup(request):
    if request.method == "POST":
        user = request.POST.get("user", None)
        email = request.POST.get("email", None)
        name = request.POST.get("name", None)
        password = request.POST.get("pass", None)
        print(user, name, password, email)
        
        if User.objects.filter(username=user).exists() or User.objects.filter(email=email).exists():
            print("User or email taken")
            messages.error(request, "Username or email already taken.")
            return redirect("/signup")
        
        account = User.objects.create_user(username=user, email=email, password=password, first_name=name)
        account.save()
        print("User Created")
        
        return redirect("/")   
    else:
        return render(request, "signup.html")

def login(request):
    return render(request, "login.html")
