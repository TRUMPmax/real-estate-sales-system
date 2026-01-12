from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from .models import Property, PropertyImage, PriceHistory
from projects.models import Project


class PropertyForm(forms.ModelForm):
    """房源表单"""

    class Meta:
        model = Property
        fields = [
            'project', 'building_number', 'unit_number', 'floor', 'room_number',
            'building_area', 'interior_area', 'shared_area',
            'unit_price', 'total_price',
            'location_description', 'status'
        ]
        widgets = {
            'location_description': forms.Textarea(attrs={'rows': 3}),
            'building_number': forms.HiddenInput(),
            'unit_number': forms.HiddenInput(),
            'floor': forms.HiddenInput(),
            'room_number': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 在编辑页面时设置隐藏字段的初始值
        if self.instance and self.instance.pk:
            self.initial['building_number'] = self.instance.building_number
            self.initial['unit_number'] = self.instance.unit_number
            self.initial['floor'] = self.instance.floor
            self.initial['room_number'] = self.instance.room_number

        self.helper = FormHelper()
        self.helper.layout = Layout(
            'project',
            Row(
                Column(
                    forms.HiddenInput(),  # 占位，实际选择器在模板中
                    css_class='form-group col-md-3'
                ),
                Column(
                    forms.HiddenInput(),
                    css_class='form-group col-md-3'
                ),
                Column(
                    forms.HiddenInput(),
                    css_class='form-group col-md-3'
                ),
                Column(
                    forms.HiddenInput(),
                    css_class='form-group col-md-3'
                ),
            ),
            # 隐藏字段
            'building_number',
            'unit_number',
            'floor',
            'room_number',
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
        self.helper.form_id = 'property-form'
        self.helper.form_tag = True

    def clean(self):
        cleaned_data = super().clean()
        project = cleaned_data.get('project')
        building_number = cleaned_data.get('building_number')
        unit_number = cleaned_data.get('unit_number')
        floor = cleaned_data.get('floor')
        room_number = cleaned_data.get('room_number')

        print(
            f"DEBUG 表单数据: project={project}, building={building_number}, unit={unit_number}, floor={floor}, room={room_number}")

        # 检查所有必需字段是否都有值
        if not building_number or not unit_number or not floor or not room_number:
            print("DEBUG: 缺少级联字段值")
            if not building_number:
                self.add_error('building_number', '请选择楼栋号')
            if not unit_number:
                self.add_error('unit_number', '请选择单元号')
            if not floor:
                self.add_error('floor', '请选择楼层')
            if not room_number:
                self.add_error('room_number', '请选择房号')
            return cleaned_data

        if project:
            try:
                # 验证楼栋号
                building_int = int(building_number)
                if building_int < 1 or building_int > project.total_buildings:
                    self.add_error('building_number', f'楼栋号必须在1-{project.total_buildings}之间')

                # 验证单元号
                unit_int = int(unit_number)
                if unit_int < 1 or unit_int > project.units_per_building:
                    self.add_error('unit_number', f'单元号必须在1-{project.units_per_building}之间')

                # 验证楼层
                floor_int = int(floor)
                if floor_int < 1 or floor_int > project.floors_per_unit:
                    self.add_error('floor', f'楼层必须在1-{project.floors_per_unit}之间')

                # 验证房号格式
                if room_number:
                    # 检查房号格式是否符合规则
                    expected_prefix = str(floor_int)
                    if not room_number.startswith(expected_prefix):
                        self.add_error('room_number', f'{floor}层的房号应以{expected_prefix}开头')

                # 验证房号唯一性
                if room_number:
                    existing = Property.objects.filter(
                        project=project,
                        building_number=str(building_int),
                        unit_number=str(unit_int),
                        room_number=room_number
                    )
                    if self.instance and self.instance.pk:
                        existing = existing.exclude(pk=self.instance.pk)

                    if existing.exists():
                        self.add_error('room_number', '该房号已存在')

            except (ValueError, TypeError) as e:
                print(f"DEBUG: 转换错误 - {e}")
                if not building_number:
                    self.add_error('building_number', '请选择楼栋号')
                if not unit_number:
                    self.add_error('unit_number', '请选择单元号')
                if not floor:
                    self.add_error('floor', '请选择楼层')
                if not room_number:
                    self.add_error('room_number', '请选择房号')

        return cleaned_data


# PriceUpdateForm - 必须存在这个类
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


# PropertyImageForm - 必须存在这个类
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