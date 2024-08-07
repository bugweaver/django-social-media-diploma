from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    content = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control width_input mx-auto',
                                                                      'placeholder': 'Comment'}))

    class Meta:
        model = Comment
        fields = ('content',)
