from django import forms
 
class UserForm(forms.Form):
    name = forms.CharField(label="Input name", initial="None", required=True)
    age = forms.IntegerField(label="Input age", initial=-1, min_value=0, max_value=100)
    comment = forms.CharField(label="Input some details", widget=forms.Textarea, 
                                help_text="Input what ever u won't", required=False,
                                max_length=150)
    field_order = ["comment", "age", "name"]