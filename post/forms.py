from django import forms
from . models import Post, Comment

class PostForm(forms.ModelForm):
    post_body = forms.CharField(
        label='',
        widget= forms.Textarea(attrs={
            'rows':'3',
            'placeholder': "What's happening...",
            'style':"overflow:hidden;",
            'class':'post-box'
        })
    )

    class Meta:
        model = Post
        fields = ('post_body',)

class CommentForm(forms.ModelForm):
    commented_body = forms.CharField(
        label='',
        widget= forms.Textarea(attrs={
            'rows':'3',
            'placeholder': "Comment here...",
            'style':"overflow:hidden;",
            'class':'post-box'
        })
    )


    class Meta:
        model = Comment
        fields = ('commented_body', )
