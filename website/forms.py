from django import forms
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.core.validators import validate_email
from django.contrib.auth.forms import UserCreationForm
from website.models import Proposal
from django.core.validators import MinLengthValidator, MinValueValidator, \
RegexValidator, URLValidator


MY_CHOICES = (
    ('Beginner', 'Beginner'),
    ('intermediate', 'Intermediate'),
    ('Advanced', 'Advanced'),
)
rating=(
    ('1','1'),
    ('2','2'),
    ('3','3'),
    ('4','4'),
    ('5','5'),
    ('6','6'),
    ('7','7'),
    ('8','8'),
    ('9','9'),
    ('10','10'),
)
    

class ContactForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'About Me'}),
                        required = True,
                        error_messages = {'required':'Name field required.'},  
                        )
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'About Me'}),
                        required = True,
                        error_messages = {'required':'Email field required.'},  
                        )
    # subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
                        required = True,
                        error_messages = {'required':'Message field required.'},  
                            )
    # rate = forms.ChoiceField(choices=rating)

class ProposalForm(forms.ModelForm):

    about_me = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'About Me'}),
                        required = True,
                        error_messages = {'required':'Title field required.'},  
                        )
    attachment = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}),
                        required = True,
                        error_messages = {'required':'Attachment field required.'},)   
    phone = forms.CharField(max_length = 12, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),required=False, validators = [RegexValidator(regex = '^[0-9-_+.]*$', message='Enter a Valid Phone Number',)],
                             # error_messages = {'required':'Title field required.'},  
                                )
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
                        required = True,
                        error_messages = {'required':'Title field required.'},  
                            )
    abstract = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Abstract'}),
                        required = True,
                        error_messages = {'required':'Abstract field required.'},  
                        )
    proposal_type = forms.CharField(widget = forms.HiddenInput(), label = '', initial = 'ABSTRACT', required=False)
    
    tags = forms.ChoiceField(choices=MY_CHOICES)

    class Meta:
        model = Proposal
        exclude = ('user', 'email','prerequisite','status','rate')

    def clean_title(self):
        title = self.cleaned_data['title']
        if Proposal.objects.filter(title=title).exists():
            raise forms.ValidationError("This title already exist.")
        return title

    def clean_attachment(self):
        import os
        cleaned_data = self.cleaned_data
        attachment = cleaned_data.get('attachment', None)
        if attachment:
            ext = os.path.splitext(attachment.name)[1]
            valid_extensions = ['.pdf']
            if not ext in valid_extensions:
                raise forms.ValidationError(u'File not supported!')
            if attachment.size > (5*1024*1024):
                raise forms.ValidationError('File size exceeds 5MB')
        return attachment


class WorkshopForm(forms.ModelForm):
    about_me = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'About Me'}),
                        required = True,
                        error_messages = {'required':'Title field required.'},  
                        )
    attachment = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}),
                        required = True,
                        error_messages = {'required':'Attachment field required.'},)   
    phone = forms.CharField(max_length = 12, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),required=False, validators = [RegexValidator(regex = '^[0-9-_+.]*$', message='Enter a Valid Phone Number',)],
                             error_messages = {'required':'Title field required.'},  
                                )
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
                        required = True,
                        error_messages = {'required':'Title field required.'},  
                            )
    abstract = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Desciption'}),
                        required = True,
                        label = 'Description',
                        error_messages = {'required':'Abstract field required.'},  
                        )
    prerequisite = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Prerequisite'}),
                        label = 'Prerequisites',
                        required = False,
                        )
    proposal_type = forms.CharField(widget = forms.HiddenInput(), label = '', required=False, initial = 'WORKSHOP')

    tags = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tags'}),
                        required = False,
                        )
    
    class Meta:
        model = Proposal
        exclude = ('user', 'email','status','rate')

    def clean_title(self):
        title = self.cleaned_data['title']
        if Proposal.objects.filter(title=title).exists():
            raise forms.ValidationError("This title already exist.")
        return title

    def clean_attachment(self):
        import os
        cleaned_data = self.cleaned_data
        attachment = cleaned_data.get('attachment', None)
        if attachment:
            ext = os.path.splitext(attachment.name)[1]
            valid_extensions = ['.pdf',]
            if not ext in valid_extensions:
                raise forms.ValidationError(u'File not supported!')
            if attachment.size > (5*1024*1024):
                raise forms.ValidationError('File size exceeds 5MB')
        return attachment

class UserRegisterForm(UserCreationForm):
	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email', 'username', 'password1',
		          'password2')
        first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First Name'}),
                        label = 'First Name'
                        )
        last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name'}),
                        label = 'Last Name'
                        )
        email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email'}),
                        required = True,
                        error_messages = {'required':'Email field required.'},  
                        label = 'Email'
                        )
        username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}),
                        required = True,
                        error_messages = {'required':'Username field required.'},  
                        label = 'Username'
                        )
        password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
                        required = True,
                        error_messages = {'required':'Password field required.'},  
                        label = 'Password'
                        )
        password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
                        required = True,
                        error_messages = {'required':'Password Confirm field required.'},  
                        label = 'RePassword'
                        )


class UserLoginForm(forms.Form):
    username = forms.CharField(
			widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}), 
			label=''
		)
    password = forms.CharField(
			widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}), 
			label=''
		)
