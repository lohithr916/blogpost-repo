from django import forms
from App1.models import Comments

class EmailForm(forms.Form):
	name = forms.CharField()
	fromemail = forms.EmailField()
	toemail = forms.EmailField()
	comments = forms.CharField(required=False,widget=forms.Textarea)

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comments
		fields = ('post','email','body')

