from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages, auth

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
        
        return redirect("/login")   
    else:
        return render(request, "signup.html")

def login(request):
    if request.method == "POST":
        user = request.POST.get("user", None)
        password = request.POST.get("pass", None)
        print(user, password)
        
        user = User.objects.filter(username=user).first()
        if user is None:
            print("User does not exist")
            messages.error(request, "User does not exist.")
            return redirect("/login")
        
        if not user.check_password(password):
            print("Incorrect Password")
            messages.error(request, "Incorrect Password.")
            return redirect("/login")
        
        auth.login(request, user)
        
        print("User Logged In")
        return redirect("/")
    else:
        return render(request, "login.html")
    
def logout(request):
    auth.logout(request)
    return redirect("/")
