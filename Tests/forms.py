from django import forms


class RegisterForm(forms.Form):
    username=forms.CharField(label='username',max_length=20,required=True,error_messages={'required':'username cannot be null'})
    password=forms.CharField(label='password',widget=forms.PasswordInput,required=True,error_messages={'required':'password cannot be null'})
    email=forms.EmailField(label='email',required=True,
                            error_messages={'required': u'email cannot be null','invalid': u'email format is wrong'},
                            widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': u'email'}))
    image=forms.ImageField(label='headimage',required=False)
