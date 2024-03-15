# miapp/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import FielTrial


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        


class FielTrialForm(forms.ModelForm):
    class Meta:
        model = FielTrial
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        pdf_file = cleaned_data.get('pdf_file')
        pdf_file_1 = cleaned_data.get('pdf_file_1')
        pdf_file_2 = cleaned_data.get('pdf_file_2')

        if not any([pdf_file, pdf_file_1, pdf_file_2]):
            raise forms.ValidationError('Al menos uno de los campos PDF debe tener un archivo adjunto.')
        
        if not any(cleaned_data.get(field) for field in ['TypeOfTest_es', 'TypeOfTest_Soi', 'TypeOfTest_comp']):
            raise forms.ValidationError("Debe seleccionar al menos un tipo de prueba.")
        
        return cleaned_data