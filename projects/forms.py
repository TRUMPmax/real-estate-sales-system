from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from .models import Project


class ProjectForm(forms.ModelForm):
    """项目表单"""
    class Meta:
        model = Project
        fields = ['name', 'address', 'developer', 'description', 'total_buildings', 'total_units']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'name',
            'address',
            Row(
                Column('developer', css_class='form-group col-md-6'),
                Column('total_buildings', css_class='form-group col-md-3'),
                Column('total_units', css_class='form-group col-md-3'),
            ),
            'description',
            Submit('submit', '保存', css_class='btn-primary')
        )

