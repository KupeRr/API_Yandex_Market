from django import forms
 
class UserForm(forms.Form):
    name = forms.CharField(label="Input name", initial="None")
    age = forms.IntegerField(label="Input age", initial=-1)
    comment = forms.CharField(label="Input some details", widget=forms.Textarea, help_text="Input what ever u won't")
    field_order = ["comment", "age", "name"]