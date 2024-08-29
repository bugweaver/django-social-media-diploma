from django import forms
from .models import Comment, Reply


class CommentForm(forms.ModelForm):
    content = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control width_input mx-auto',
                                                                      'placeholder': 'Add a comment...',
                                                                      'autocomplete': 'off'}))

    class Meta:
        model = Comment
        fields = ('content',)


class ReplyForm(forms.ModelForm):
    content = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control mx-auto',
                                                                      'placeholder': 'Reply...',
                                                                      'autocomplete': 'off'}))

    class Meta:
        model = Reply
        fields = ('content',)
