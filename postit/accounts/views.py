from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib import messages, auth

from . models import Member
from home.models import PostBox, Subscription

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
        
        group = Group.objects.get(name="viewer")
        account.groups.add(group)
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


def profile(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            name = request.POST.get("name", None)
            username = request.POST.get("username", None)
            password = request.POST.get("password", None)
            
            user = request.user
            user.first_name = name
            if username:  # Check if username is provided
                user.username = username
            if password:
                user.set_password(password)
            user.save()
            
            return redirect("/")  # Redirect to home page or any other desired URL
        else:
            has_verified_permission = request.user.groups.filter(name='verified').exists()
            subscribed_postbox_list = []
            if request.user.is_authenticated:
                subscribed_postbox_list = Subscription.objects.filter(user=request.user).values_list('postbox__title', flat=True)
            else:
                subscribed_postbox_list = []
            postbox_list = PostBox.objects.all()
            return render(request, "profile.html", {"user": request.user,
                                                    "postbox_list": postbox_list,
                                                    "has_verified_permission": has_verified_permission,
                                                    "subscribed_postbox_list": subscribed_postbox_list
                                                    })
    else:
        return redirect("/login")
