from django import forms
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.core.validators import validate_email
from django.contrib.auth.forms import UserCreationForm
from website.models import Proposal
from django.core.validators import MinLengthValidator, MinValueValidator, \
RegexValidator, URLValidator


class CommentForm(forms.ModelForm):
    pass
    
class ProposalForm(forms.ModelForm):
    # content_link = forms.CharField(required=False, help_text='Link to the content of your Talk')
    # speaker_link = forms.CharField(required=False, help_text='Link to information about the Speaker')
    attachment = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))   
    phone = forms.CharField(max_length = 12, widget=forms.TextInput(),required=False, validators = [RegexValidator(regex = '^[0-9-_+.]*$')])
    title = forms.CharField(widget=forms.TextInput(),
                        required = True,
                        error_messages = {'required':'Title field required.'})
    class Meta:
        model = Proposal
        exclude = ('user', 'email','prerequisite')

    def clean_title(self):
        title = self.cleaned_data['title']
        if Proposal.objects.filter(title=title).exists():
            raise forms.ValidationError("This title already exist.")
        return title

    # def clean_attachment(self):
    #     cleaned_data = self.cleaned_data
    #     attachment = cleaned_data.get('attachment', None)
    #     if attachment:
    #         # if not attachment.name.endswith('.pdf') :
    #         #     raise forms.ValidationError('Only [.pdf] files are allowed')
    #         if attachment.size > (5*1024*1024):
    #             raise forms.ValidationError('File size exceeds 5MB')
    #     return attachment


class WorkshopForm(forms.ModelForm):
    attachment = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))   
    phone = forms.CharField(max_length = 12, widget=forms.TextInput(),required=False, validators = [RegexValidator(regex = '^[0-9-_+.]*$')])
    title = forms.CharField(widget=forms.TextInput(),
                        required = True,
                        error_messages = {'required':'Title field required.'})


    class Meta:
        model = Proposal
        exclude = ('user', 'email')

    def clean_title(self):
        title = self.cleaned_data['title']
        if Proposal.objects.filter(title=title).exists():
            raise forms.ValidationError("This title already exist.")
        return title


class UserRegisterForm(UserCreationForm):
	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email', 'username', 'password1',
		          'password2')


class UserLoginForm(forms.Form):
    username = forms.CharField(
			widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}), 
			label=''
		)
    password = forms.CharField(
			widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}), 
			label=''
		)
