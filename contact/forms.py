from django import forms
from . import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import password_validation
 
class ContactForm(forms.ModelForm):
    first_name = forms.CharField(
        label='Nome',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Escreva seu nome aqui',
            }
        ),
        help_text='Você deve digitar seu nome'
    )

    last_name = forms.CharField(
        label='Sobrenome',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Escreva seu sobrenome aqui',
            }
        ),
        help_text='Você deve digitar seu sobrenome'
    )

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:

        model = models.Contact
        fields = ('first_name', 'last_name',)

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')

        if first_name == last_name:
            msg = ValidationError('Nome não pode ser igual ao sobrenome', code='invalid')    
            self.add_error('last_name',msg)
        return cleaned_data    

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if first_name and any(char.isdigit() for char in first_name):
            raise ValidationError('Não pode possuir números', code='invalid')
        return first_name
    
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if last_name and any(char.isdigit() for char in last_name):
            raise ValidationError('Não pode possuir números', code='invalid')
        return last_name
    
class RegisterForm(UserCreationForm):
    first_name = forms.CharField(required=True, min_length=3, label='Primeiro Nome')
    last_name = forms.CharField(required=True, min_length=3, label='Segundo Nome')
    email = forms.EmailField(required=True)
    username = forms.CharField(required=True, label='Usuario', help_text='Este sera usado para o seu login!')
    
    class Meta:
        model = User
        fields = (
            'username','first_name', 'last_name', 'email',
            'password1', 'password2',
                  )


    def save(self, commit=True):
        cleaned_data = self.cleaned_data
        user = super().save(commit=False)
        password1 = cleaned_data.get('password1')

        if password1:
            user.set_password(password1)

        if commit:
            user.save()    

        return user


    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 or password2:
            if password1 != password2:
                self.add_error('password2', ValidationError('Senhas não são iguais'))
        
        
        return super().clean()

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
            'Este email já está em uso.'
        )

        return email
    


class RegisterUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        min_length=2,
        max_length=30,
        required=True,
        help_text='Required.',
        error_messages={
            'min_length': 'Please, add more than 2 letters.'
        }
    )
    last_name = forms.CharField(
        min_length=2,
        max_length=30,
        required=True,
        help_text='Required.'
    )

    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
        required=False,
    )

    password2 = forms.CharField(
        label="Password 2",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text='Use the same password as before.',
        required=False,
    )


    class Meta:
        model = User
        fields = (
            'username','first_name', 'last_name', 'email',
                )
            
    def clean_email(self):
        email = self.cleaned_data.get('email')
        current_email = self.instance.email

        if current_email != email:
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError(
                'Este email já está em uso.', code='invalid'
            )

        return email       

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        if password1:
            try:
                password_validation.validate_password(password1)
            except ValidationError as errors:
                self.add_error('password1', ValidationError(errors))

        return password1