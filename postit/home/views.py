from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, "home.html")

def postbox(request, postbox_name):
    postbox_description = "This is a postbox for " + postbox_name
    # post = Post.objects.get(file_name=postbox_name)
    return render(request, "postbox.html", {
        "postbox_name": postbox_name,
        "postbox_description": postbox_description
    })
    