from django import forms
from comment.models import Comment

class CommentForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={"class": "comment-content textarea subtitle is-4", "placeholder": "Add a comment...", "rows": 4 }), required=True)

    class Meta:
        model = Comment
        fields = ('body',)