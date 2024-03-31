from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Uploads
from .forms import CreatePostForm

def index(request):
    title_field = Uploads.objects.all
    # title_list = list(title_field)
    return render(request, "home.html",{"all": title_field})

def postbox(request, postbox_name):
    postbox_description = "This is a postbox for " + postbox_name
    # post = Post.objects.get(file_name=postbox_name)
    return render(request, "postbox.html", {
        "postbox_name": postbox_name,
        "postbox_description": postbox_description
    })


def createpost(request):
    if request.method == "POST":
        form = CreatePostForm(request.POST, request.FILES or None)
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            print(form.errors)
            return redirect('createpost')


    else:
        rules = "Please make sure to follow the rules and guidlines"
        return render(request, "postbox.html", {"postbox_name": rules})