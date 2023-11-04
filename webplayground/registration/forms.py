from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class UserCreationFormWithEmail(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Requerido, 254 caracteres como máximo y debe ser válido")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):  # Validación de email
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():   # Si el email ya existe
            raise forms.ValidationError("El email ya está registrado, prueba con otro.")    # Lanzamos un error
        return email

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'link']
        widgets = {
            'avatar': forms.ClearableFileInput(attrs={'class':'form-control-file mt-3'}),   # Añadimos clases para que se vea mejor
            'bio': forms.Textarea(attrs={'class':'form-control mt-3', 'rows':3, 'placeholder':'Biografía'}),    # Añadimos clases para que se vea mejor
            'link': forms.URLInput(attrs={'class':'form-control mt-3', 'placeholder':'Enlace'}),    # Añadimos clases para que se vea mejor
        }

class EmailForm(forms.ModelForm):
    email = forms.EmailField(required=True, help_text="Requerido, 254 caracteres como máximo y debe ser válido")

    class Meta:
        model = User
        fields = ["email"]

    def clean_email(self):  # Validación de email
        email = self.cleaned_data.get("email")
        if "email" in self.changed_data:    # Si el email ha cambiado
            if User.objects.filter(email=email).exists():   # Si el email ya existe
                raise forms.ValidationError("El email ya está registrado, prueba con otro.")    # Lanzamos un error
        return email