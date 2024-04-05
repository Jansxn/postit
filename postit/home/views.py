from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Uploads, PostBox, Subscription
from .forms import CreatePostForm

def index(request):
    all_posts = Uploads.objects.all().order_by('-id')
    postbox_list = PostBox.objects.all()
    if request.user.is_authenticated:
        subscribed_postbox_list = Subscription.objects.filter(user=request.user).values_list('postbox__title', flat=True)
    else:
        subscribed_postbox_list = []
    has_verified_permission = request.user.groups.filter(name='verified').exists()
    context = {"all": all_posts,
               "postbox_list": postbox_list,
               "has_verified_permission": has_verified_permission,
               "subscribed_postbox_list": subscribed_postbox_list}

    return render(request, "home.html", context)

def postbox(request, postbox_name):
    postbox_description = "This is a postbox for " + postbox_name
    if request.user.is_authenticated:
        subscribed_postbox_list = Subscription.objects.filter(user=request.user).values_list('postbox__title', flat=True)
    else:
        subscribed_postbox_list = []
    showfrom = True
    try:
        postbox = PostBox.objects.get(title=postbox_name)
        postbox_description = postbox.content
        uploads = Uploads.objects.filter(submission_page=postbox)
    except PostBox.DoesNotExist:
        postbox_description = "Please contact an admin or verified user to create the Postbox: " + postbox_name
        uploads = Uploads.objects.none()
        showfrom = False
    has_verified_permission = request.user.groups.filter(name='verified').exists()
    print(has_verified_permission)
    postbox_list = PostBox.objects.all()
    return render(request, "postbox.html", {
        "postbox_name": postbox_name,
        "postbox_description": postbox_description,
        "subscribed_postbox_list":subscribed_postbox_list,
        "has_verified_permission": has_verified_permission,
        "postbox_list": postbox_list,
        "uploads": uploads,
        "showfrom": showfrom
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
    
def createpostbox(request):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        PostBox.objects.create(title=title, content=content)
        return redirect('index')
    else:
        postbox_list = PostBox.objects.all()
        has_verified_permission = request.user.groups.filter(name='verified').exists()
        if request.user.is_authenticated:
            subscribed_postbox_list = Subscription.objects.filter(user=request.user).values_list('postbox__title', flat=True)
        else:
            subscribed_postbox_list = []
        return render(request, "createpostbox.html", {"postbox_list": postbox_list,
                                                      "has_verified_permission": has_verified_permission,
                                                      "subscribed_postbox_list": subscribed_postbox_list
                                                      })
        
        
def subscribe(request, postbox_name):
    postbox = PostBox.objects.get(title=postbox_name)
    user = request.user
    if not Subscription.objects.filter(user=user, postbox=postbox).exists():
        Subscription.objects.create(user=user, postbox=postbox)
    return redirect('index')