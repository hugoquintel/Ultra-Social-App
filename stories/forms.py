import os
from django import forms

from stories.models import Story
from django.core.exceptions import ValidationError

from django.forms import ClearableFileInput

def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.jpg','.jpeg','.png','.mp4']
    if not ext in valid_extensions:
        raise ValidationError('File is not supported!')

class NewStoryForm(forms.ModelForm):
    content = forms.FileField(widget=forms.ClearableFileInput(attrs={"class": "img-input", "multiple": False}), validators=[validate_file_extension], required=True)
    caption = forms.CharField(widget=forms.Textarea(attrs={"class": "input is-medium"}), required=True)

    class Meta:
        model = Story
        fields = ('content', 'caption')