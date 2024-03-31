from django import forms
from .models import Uploads


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Uploads
        fields = ['title', 'content', 'file']
