from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from .models import Sale
from django.contrib.auth import get_user_model

User = get_user_model()


class SaleForm(forms.ModelForm):
    """销售记录表单"""
    class Meta:
        model = Sale
        fields = ['customer', 'property', 'salesperson', 'sale_price', 'down_payment', 
                 'payment_method', 'contract_number', 'contract_date', 'status', 'notes']
        widgets = {
            'contract_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 只允许选择业务员
        self.fields['salesperson'].queryset = User.objects.filter(role='salesperson')
        self.fields['salesperson'].required = False
        
        # 只显示可售或已预订的房源
        self.fields['property'].queryset = self.fields['property'].queryset.filter(
            status__in=['available', 'reserved']
        )
        
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('customer', css_class='form-group col-md-6'),
                Column('property', css_class='form-group col-md-6'),
            ),
            'salesperson',
            Row(
                Column('sale_price', css_class='form-group col-md-6'),
                Column('down_payment', css_class='form-group col-md-6'),
            ),
            'payment_method',
            Row(
                Column('contract_number', css_class='form-group col-md-6'),
                Column('contract_date', css_class='form-group col-md-6'),
            ),
            'status',
            'notes',
            Submit('submit', '保存', css_class='btn-primary')
        )

