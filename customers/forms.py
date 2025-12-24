from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from .models import Customer
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomerForm(forms.ModelForm):
    """客户表单"""
    class Meta:
        model = Customer
        fields = ['name', 'gender', 'phone', 'email', 'id_card', 'address', 'notes', 'salesperson']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 只允许选择业务员
        self.fields['salesperson'].queryset = User.objects.filter(role='salesperson')
        self.fields['salesperson'].required = False
        
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-6'),
                Column('gender', css_class='form-group col-md-6'),
            ),
            Row(
                Column('phone', css_class='form-group col-md-6'),
                Column('email', css_class='form-group col-md-6'),
            ),
            Row(
                Column('id_card', css_class='form-group col-md-6'),
                Column('salesperson', css_class='form-group col-md-6'),
            ),
            'address',
            'notes',
            Submit('submit', '保存', css_class='btn-primary')
        )

