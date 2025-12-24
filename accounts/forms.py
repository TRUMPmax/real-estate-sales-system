from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

User = get_user_model()


class LoginForm(AuthenticationForm):
    """登录表单"""
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request=request, *args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'username',
            'password',
            Submit('submit', '登录', css_class='btn-primary w-100')
        )


class UserCreateForm(forms.ModelForm):
    """创建用户表单"""
    password1 = forms.CharField(label='密码', widget=forms.PasswordInput)
    password2 = forms.CharField(label='确认密码', widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'phone', 'first_name', 'last_name', 'is_active', 'is_staff']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('username', css_class='form-group col-md-6'),
                Column('email', css_class='form-group col-md-6'),
            ),
            Row(
                Column('password1', css_class='form-group col-md-6'),
                Column('password2', css_class='form-group col-md-6'),
            ),
            Row(
                Column('role', css_class='form-group col-md-6'),
                Column('phone', css_class='form-group col-md-6'),
            ),
            Row(
                Column('first_name', css_class='form-group col-md-6'),
                Column('last_name', css_class='form-group col-md-6'),
            ),
            'is_active',
            'is_staff',
            Submit('submit', '创建', css_class='btn-primary')
        )
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('两次输入的密码不一致')
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    """更新用户表单"""
    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'phone', 'first_name', 'last_name', 'is_active', 'is_staff']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('username', css_class='form-group col-md-6'),
                Column('email', css_class='form-group col-md-6'),
            ),
            Row(
                Column('role', css_class='form-group col-md-6'),
                Column('phone', css_class='form-group col-md-6'),
            ),
            Row(
                Column('first_name', css_class='form-group col-md-6'),
                Column('last_name', css_class='form-group col-md-6'),
            ),
            'is_active',
            'is_staff',
            Submit('submit', '更新', css_class='btn-primary')
        )


class RegisterForm(forms.ModelForm):
    """用户注册表单 - 仅限购房者"""
    password1 = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(attrs={'placeholder': '请输入密码'}),
        min_length=6,
        help_text='密码至少6个字符'
    )
    password2 = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput(attrs={'placeholder': '请再次输入密码'})
    )
    username = forms.CharField(
        label='用户名',
        widget=forms.TextInput(attrs={'placeholder': '请输入用户名'}),
        help_text='用户名只能包含字母、数字和下划线'
    )
    email = forms.EmailField(
        label='邮箱',
        widget=forms.EmailInput(attrs={'placeholder': '请输入邮箱地址'})
    )
    phone = forms.CharField(
        label='电话',
        widget=forms.TextInput(attrs={'placeholder': '请输入联系电话'}),
        required=False
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'first_name', 'last_name']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'username',
            Row(
                Column('email', css_class='form-group col-md-6'),
                Column('phone', css_class='form-group col-md-6'),
            ),
            Row(
                Column('first_name', css_class='form-group col-md-6'),
                Column('last_name', css_class='form-group col-md-6'),
            ),
            Row(
                Column('password1', css_class='form-group col-md-6'),
                Column('password2', css_class='form-group col-md-6'),
            ),
            Submit('submit', '注册', css_class='btn-primary w-100')
        )
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('该用户名已被使用，请选择其他用户名')
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('该邮箱已被注册，请使用其他邮箱')
        return email
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('两次输入的密码不一致')
        if password1 and len(password1) < 6:
            raise forms.ValidationError('密码至少需要6个字符')
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.role = 'buyer'  # 固定为购房者角色
        user.is_active = True  # 注册后自动激活
        if commit:
            user.save()
        return user

