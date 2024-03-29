from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    re_path(r'^(?!login$|signup$|logout$)([a-zA-Z0-9_]+)/$', views.postbox, name='postbox'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
