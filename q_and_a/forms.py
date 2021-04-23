from django import forms
from .models import *

class PostQuestionForm(forms.ModelForm):
    """質問投稿フォーム"""
    title = forms.CharField(widget=forms.TextInput(
        attrs={
            "class":"control is-large is-expanded ",
            "placeholder":"タイトルを入力してください",
        }
    ))

    body = forms.CharField(widget=forms.Textarea(
        attrs={
            "class":"control",
            "onKeyUp":"markdown2html()",#だめっぽい
        }
    ))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class'] = 'input is-expanded'

    class Meta:
        model = Question
        fields = ["title", "body"]

class PostDiaryForm(forms.ModelForm):
    """ナレッジ投稿フォーム"""

    title = forms.CharField(widget=forms.TextInput(
        attrs={
            "class":"control is-large is-expanded ",
            "placeholder":"タイトルを入力してください",
        }
    ))

    body = forms.CharField(widget=forms.Textarea(
        attrs={
            "class":"control",
            "onKeyUp":"markdown2html()",#だめっぽい
        }
    ))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class'] = 'input is-expanded'

    class Meta:
        model = Diary
        fields = ["title", "body"]