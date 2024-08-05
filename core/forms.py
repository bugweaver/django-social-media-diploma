from django import forms
from .models import Post, Profile, Comment
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django.contrib.auth.models import User


class PostForm(forms.ModelForm):
    body = forms.CharField(required=True, widget=forms.widgets.Textarea(
        attrs={
            'placeholder': 'Enter Your Text',
            'class': 'form-control'
        }
    ), label="",

                           )

    class Meta:
        model = Post
        exclude = 'user', 'likes'


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="",
                             widget=forms.TextInput(attrs={'class': 'form-control width_input',
                                                           'placeholder': 'Email Address'}))
    first_name = forms.CharField(label="", max_length=100,
                                 widget=forms.TextInput(attrs={'class': 'form-control width_input',
                                                               'placeholder': 'First Name'}))
    last_name = forms.CharField(label="", max_length=100,
                                widget=forms.TextInput(attrs={'class': 'form-control width_input',
                                                              'placeholder': 'Last Name'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']
        # labels = {
        #     'first_name': "First Name", 'last_name': "Last Name", 'email': "Email", 'username': "Username",
        #     'password1': 'Password', 'password2': 'Confirm Password',
        # }

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control width_input'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['username'].label = ''
        self.fields[
            'username'].help_text = ('<span class="form-text text-muted"><small>Required. 150 characters or fewer.'
                                     ' Letters, digits and @/./+/-/_ only.</small></span>')

        self.fields['password1'].widget.attrs['class'] = 'form-control width_input'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields[
            'password1'].help_text = (
            '<ul class="form-text text-muted small">'
            '<li>Your password can\'t be too similar to your other personal information.'
            '</li><li>Your password must contain at least 8 characters.</li>'
            '<li>Your password can\'t be a commonly used password.</li>'
            '<li>Your password can\'t be entirely numeric.</li></ul>')

        self.fields['password2'].widget.attrs['class'] = 'form-control width_input'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields[
            'password2'].help_text = ('<span class="form-text text-muted">'
                                      '<small>Enter the same password as before, for verification.</small></span>')


class UpdateUserForm(UserChangeForm):
    password = None
    email = forms.EmailField(label="",
                             widget=forms.TextInput(attrs={'class': 'form-control width_input',
                                                           'placeholder': 'Email Address'}))
    first_name = forms.CharField(label="", max_length=100,
                                 widget=forms.TextInput(attrs={'class': 'form-control width_input',
                                                               'placeholder': 'First Name'}))
    last_name = forms.CharField(label="", max_length=100,
                                widget=forms.TextInput(attrs={'class': 'form-control width_input',
                                                              'placeholder': 'Last Name'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control width_input'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['username'].label = ''
        self.fields[
            'username'].help_text = ('<span class="form-text text-muted"><small>Required. 150 characters or fewer.'
                                     ' Letters, digits and @/./+/-/_ only.</small></span>')


class ChangePasswordForm(SetPasswordForm):
    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']

    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

        self.fields['new_password1'].widget.attrs['class'] = 'form-control width_input'
        self.fields['new_password1'].widget.attrs['placeholder'] = 'New Password'
        self.fields['new_password1'].label = ''
        self.fields[
            'new_password1'].help_text = (
            '<ul class="form-text text-muted small">'
            '<li>Your password can\'t be too similar to your other personal information.'
            '</li><li>Your password must contain at least 8 characters.</li>'
            '<li>Your password can\'t be a commonly used password.</li>'
            '<li>Your password can\'t be entirely numeric.</li></ul>')

        self.fields['new_password2'].widget.attrs['class'] = 'form-control width_input'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'Confirm New Password'
        self.fields['new_password2'].label = ''
        self.fields[
            'new_password2'].help_text = ('<span class="form-text text-muted">'
                                          '<small>Enter the same password as before, for verification.</small></span>')


class ProfilePicForm(forms.ModelForm):
    profile_image = forms.ImageField(label="Profile Picture")
    bio = forms.CharField(label="", widget=forms.Textarea(attrs={'class': 'form-control width_input',
                                                                 'placeholder': 'Bio'}))

    class Meta:
        model = Profile
        fields = ('bio', 'profile_image')

    def __init__(self, *args, **kwargs):
        super(ProfilePicForm, self).__init__(*args, **kwargs)
        self.fields['profile_image'].required = False
        self.fields['bio'].required = False


class CommentForm(forms.ModelForm):
    content = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control width_input mx-auto',
                                                                      'placeholder': 'Comment'}))

    class Meta:
        model = Comment
        fields = ('content',)

