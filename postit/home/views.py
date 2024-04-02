from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Uploads, PostBox
from .forms import CreatePostForm

def index(request):
    all_posts = Uploads.objects.all().order_by('-id')
    postbox_list = PostBox.objects.all()

    context = {"all": all_posts,
               "postbox_list": postbox_list}

    return render(request, "home.html", context)

def postbox(request, postbox_name):
    postbox_description = "This is a postbox for " + postbox_name
    try:
        postbox = PostBox.objects.get(title=postbox_name)
        postbox_description = postbox.content
        uploads = Uploads.objects.filter(submission_page=postbox)
    except PostBox.DoesNotExist:
        postbox_description = "This is a postbox for " + postbox_name
        uploads = Uploads.objects.none()
    has_verified_permission = request.user.groups.filter(name='verified').exists()
    print(has_verified_permission)
    postbox_list = PostBox.objects.all()
    return render(request, "postbox.html", {
        "postbox_name": postbox_name,
        "postbox_description": postbox_description,
        "has_verified_permission": has_verified_permission,
        "postbox_list": postbox_list,
        "uploads": uploads
    })


def createpost(request):
    if request.method == "POST":
        form = CreatePostForm(request.POST, request.FILES or None)
        if form.is_valid():
            current_user = request.user
            form.instance.user = current_user
            current_page = request.POST.get('page_name')
            postbox = PostBox.objects.get(title=current_page)
            print(f"Current user: {postbox}")
            form.instance.submission_page = postbox
            form.save()
            return redirect('index')
        else:
            print(form.errors)
            return redirect('createpost')


    else:
        rules = "Please make sure to follow the rules and guidlines"
        return render(request, "postbox.html", {"postbox_name": rules})