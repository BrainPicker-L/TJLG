from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class LoginForm(forms.Form):
    username = forms.CharField(label='用户名',
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入用户名'}))
    password = forms.CharField(label='密码',
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入密码'}))


    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = auth.authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError('用户名或密码不正确')
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data


class RegForm(forms.Form):
    username = forms.CharField(label='用户名',
                               max_length=30,
                               min_length=3,
                               widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'请输入3-30位用户名'}))
    avatar = forms.ImageField(label="头像", required=True)
    email = forms.EmailField(label='邮箱',
                             widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'请输入邮箱'}))
    password = forms.CharField(label='密码',
                               min_length=6,
                               widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'请输入密码'}))
    password_again = forms.CharField(label='再输入一次密码',
                                     min_length=6,
                                     widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'再输入一次密码'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名已存在')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱已存在')
        return email

    def clean_password_again(self):
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        if password != password_again:
            raise forms.ValidationError('两次输入的密码不一致')
        return password_again

class ArticleForm(forms.Form):
    title = forms.CharField(label="标题",max_length=50)
    detail_url = forms.URLField(label="文章详情链接--(可选)(注:只能添加已关联公众号文章链接或通过本网站发布的详情文章链接):",required=False)
    excerpt = forms.CharField(label="摘要",error_messages={'required': '摘要内容不能为空'},widget=forms.Textarea)
    img1 = forms.ImageField(label="图片1",required=False)
    img2 = forms.ImageField(label="图片2",required=False)
    img3 = forms.ImageField(label="图片3",required=False)
    img4 = forms.ImageField(label="图片4",required=False)
    img5 = forms.ImageField(label="图片5",required=False)
    img6 = forms.ImageField(label="图片6",required=False)
    img7 = forms.ImageField(label="图片7",required=False)
    img8 = forms.ImageField(label="图片8",required=False)
    img9 = forms.ImageField(label="图片9",required=False)

class DetailArticleForm(forms.Form):
    title = forms.CharField(label="标题")
    content = forms.CharField(widget=CKEditorUploadingWidget())
