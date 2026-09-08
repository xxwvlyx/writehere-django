from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']  # Only include the content field in the form

        labels = {
            'content': '',
        }
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control border-0 fs-5 shadow-none bg-transparent', 
                'placeholder': 'Що відбувається?', 
                'rows': 2
            })
        }
