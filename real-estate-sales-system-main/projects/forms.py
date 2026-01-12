from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from .models import Project


class ProjectForm(forms.ModelForm):
    """项目表单"""

    class Meta:
        model = Project
        fields = [
            'name', 'address', 'developer', 'description',
            'total_buildings',  # 总楼栋数
            'units_per_building',  # 每楼栋单元数
            'floors_per_unit',  # 每单元楼层数
            'rooms_per_floor',  # 新增：每楼层房号数
            'construction_area'  # 可选
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'total_buildings': forms.NumberInput(attrs={'min': 1, 'step': 1}),
            'units_per_building': forms.NumberInput(attrs={'min': 1, 'step': 1}),
            'floors_per_unit': forms.NumberInput(attrs={'min': 1, 'step': 1}),
            'rooms_per_floor': forms.NumberInput(attrs={'min': 1, 'step': 1}),  # 新增
            'construction_area': forms.NumberInput(attrs={'min': 0, 'step': 0.01}),
        }
        help_texts = {
            'total_buildings': '项目的总楼栋数量',
            'units_per_building': '每栋楼有多少个单元',
            'floors_per_unit': '每个单元有多少层',
            'rooms_per_floor': '每个楼层有多少个房号',  # 新增
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'name',
            'address',
            Row(
                Column('developer', css_class='form-group col-md-8'),
                Column('construction_area', css_class='form-group col-md-4'),
            ),

            # 四个核心配置字段
            Row(
                Column('total_buildings', css_class='form-group col-md-3'),
                Column('units_per_building', css_class='form-group col-md-3'),
                Column('floors_per_unit', css_class='form-group col-md-3'),
                Column('rooms_per_floor', css_class='form-group col-md-3'),  # 新增
            ),

            'description',
            Submit('submit', '保存', css_class='btn-primary')
        )