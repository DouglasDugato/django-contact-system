from django import forms
from . import models
from django.core.exceptions import ValidationError

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