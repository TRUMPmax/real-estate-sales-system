# projects/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Project(models.Model):
    """项目/楼盘模型"""
    name = models.CharField(max_length=200, verbose_name='项目名称')
    address = models.CharField(max_length=500, verbose_name='地址')
    developer = models.CharField(max_length=200, verbose_name='开发商')
    description = models.TextField(blank=True, verbose_name='项目描述')

    # 只需要这四个输入字段
    total_buildings = models.IntegerField(default=1, verbose_name='总楼栋数')
    units_per_building = models.IntegerField(default=2, verbose_name='每楼栋单元数')
    floors_per_unit = models.IntegerField(default=20, verbose_name='每单元楼层数')
    rooms_per_floor = models.IntegerField(default=4, verbose_name='每楼层房号数')  # 新增

    # 可选的其他信息
    construction_area = models.DecimalField(
        max_digits=12, decimal_places=2, default=0,
        verbose_name='建筑面积(㎡)', help_text='总建筑面积', blank=True
    )

    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True,
        related_name='created_projects', verbose_name='创建人'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '项目'
        verbose_name_plural = '项目'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_config_summary(self):
        """获取配置概览"""
        return f"{self.total_buildings}栋 × {self.units_per_building}单元 × {self.floors_per_unit}层 × {self.rooms_per_floor}房"