from django import forms

from .models import Post

# Create your forms here.

# Form for creating Post.
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "title",
            "content"
        ]
