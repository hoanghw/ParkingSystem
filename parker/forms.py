from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from parker.models import Parker

class RegistrationForm(ModelForm):
    userId      = forms.CharField(label=(u'User Id'))
    email       = forms.EmailField(label=(u'Email Address'))
    password    = forms.CharField(label=(u'Password'), widget=forms.PasswordInput(render_value=False))
    verifypassword = forms.CharField(label=(u'Verify Password'), widget=forms.PasswordInput(render_value=False))

    class Meta:
        model = Parker
        exclude = ('user',)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError("Username is already taken, please select another.")

    def clean_verifypassword(self):
        if 'password' in self.cleaned_data:
            password = self.cleaned_data['password']
            verifypassword = self.cleaned_data['verifypassword']
            if password == verifypassword:
                return verifypassword
        raise forms.ValidationError('The passwords you entered do not match.')