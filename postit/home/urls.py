from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("createpost", views.createpost, name="createpost"),
    path("<str:postbox_name>/", views.postbox, name='postbox'),
    path("createpostbox", views.createpostbox, name="createpostbox"),
    # re_path(r'^(?!create$|login$|signup$|logout$|admin$)([a-zA-Z0-9_]+)/$', views.postbox, name='postbox'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
