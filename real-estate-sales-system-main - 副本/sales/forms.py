# sales/forms.py
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
        queryset = self.fields['property'].queryset.filter(
            status__in=['available', 'reserved']
        )

        # 关键修正：直接使用 Property 的 __str__ 方法，或者构建正确的显示
        self.fields['property'].label_from_instance = self.get_correct_display

        self.fields['property'].queryset = queryset

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

    # sales/forms.py
    def get_correct_display(self, obj):
        """正确的显示方法 - 清理多余的'栋'和'单元'"""
        # 获取字段值
        building = str(obj.building_number).strip()
        unit = str(obj.unit_number).strip()
        room = str(obj.room_number).strip()

        # 清理重复的单位
        # 如果building以"栋"结尾，去掉它（因为我们后面会加）
        if building.endswith('栋'):
            building = building.rstrip('栋')
        # 如果unit以"单元"结尾，去掉它
        if unit.endswith('单元'):
            unit = unit.rstrip('单元')

        # 重新构建：4栋1单元601
        return f"{building}栋{unit}单元{room}"