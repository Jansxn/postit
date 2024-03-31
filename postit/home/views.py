from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Uploads
from .forms import CreatePostForm

def index(request):
    # all_posts= Uploads.objects.all
    all_posts = Uploads.objects.all().order_by('-id')
    # username = request.user
    # title_list = list(title_field)

    context = {"all": all_posts}

    return render(request, "home.html", context)

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
            current_user = request.user
            form.instance.user = current_user
            current_page = request.POST.get('page_name')
            print(f"Current Page: {current_page}")
            form.instance.submission_page = current_page
            form.save()
            return redirect('index')
        else:
            print(form.errors)
            return redirect('createpost')


    else:
        rules = "Please make sure to follow the rules and guidlines"
        return render(request, "postbox.html", {"postbox_name": rules})