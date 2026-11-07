from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image']
        labels = {
            'content': '',
            'image': '',
        }
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control border-0 fs-5 shadow-none bg-transparent', 
                'placeholder': 'Що відбувається?', 
                'rows': 2
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control form-control-sm',
                'accept': 'image/*',
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get('content')
        image = cleaned_data.get('image')
        if not content and not image:
            raise forms.ValidationError("Допис не може бути порожнім: додайте текст або зображення.")
        return cleaned_data


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': '',
        }
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control border-0 shadow-none bg-transparent', 
                'placeholder': 'Напишіть відповідь...', 
                'rows': 2
            })
        }

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content or not content.strip():
            raise forms.ValidationError("Коментар не може бути порожнім.")
        return content.strip()
