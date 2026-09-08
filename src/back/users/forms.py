from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm

class CustomRegisterForm(UserCreationForm):
    # Додаємо поле email і робимо його обов'язковим
    email = forms.EmailField(
        required=True, 
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'name@example.com'})
    )

class CustomLoginForm(AuthenticationForm):
    # Змінюємо підпис і підказку для поля
    username = forms.CharField(
        label='Логін або Email',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'name@example.com або логін'})
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ваш пароль'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email') # Вказуємо, які поля показувати
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Додаємо стилі Bootstrap для всіх полів форми
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'