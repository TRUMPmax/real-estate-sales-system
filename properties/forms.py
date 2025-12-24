from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from .models import Property, PropertyImage


class PropertyForm(forms.ModelForm):
    """房源表单"""
    class Meta:
        model = Property
        fields = [
            'project', 'building_number', 'unit_number', 'room_number', 'floor',
            'building_area', 'interior_area', 'shared_area',
            'unit_price', 'total_price',
            'location_description', 'status'
        ]
        widgets = {
            'location_description': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'project',
            Row(
                Column('building_number', css_class='form-group col-md-3'),
                Column('unit_number', css_class='form-group col-md-3'),
                Column('room_number', css_class='form-group col-md-3'),
                Column('floor', css_class='form-group col-md-3'),
            ),
            Row(
                Column('building_area', css_class='form-group col-md-4'),
                Column('interior_area', css_class='form-group col-md-4'),
                Column('shared_area', css_class='form-group col-md-4'),
            ),
            Row(
                Column('unit_price', css_class='form-group col-md-6'),
                Column('total_price', css_class='form-group col-md-6'),
            ),
            'location_description',
            'status',
            Submit('submit', '保存', css_class='btn-primary')
        )


class PriceUpdateForm(forms.ModelForm):
    """价格更新表单"""
    reason = forms.CharField(label='调价原因', required=False, widget=forms.Textarea(attrs={'rows': 3}))
    
    class Meta:
        model = Property
        fields = ['unit_price', 'total_price']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('unit_price', css_class='form-group col-md-6'),
                Column('total_price', css_class='form-group col-md-6'),
            ),
            'reason',
            Submit('submit', '更新价格', css_class='btn-primary')
        )


class PropertyImageForm(forms.ModelForm):
    """房源图片上传表单"""
    class Meta:
        model = PropertyImage
        fields = ['image', 'description', 'is_main']
        widgets = {
            'description': forms.TextInput(attrs={'placeholder': '图片描述（可选）'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'image',
            'description',
            'is_main',
            Submit('submit', '上传图片', css_class='btn-primary')
        )

