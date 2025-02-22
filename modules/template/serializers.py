import json
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator
from modules.template.constants import PRIVATE_TYPES, CHOICE_TYPES
from modules.template.models import Template, TemplateConfigItem


class TemplateInfoSerializer(serializers.ModelSerializer):
    template_item_info = serializers.JSONField(help_text="组件配置信息", read_only=True)
    name = serializers.CharField(required=True, validators=[UniqueValidator(queryset=Template.objects.
                                                                            all(), message="组件名已存在")],
                                 help_text="组件名")
    title = serializers.CharField(required=True, validators=[UniqueValidator(queryset=Template.objects.
                                                                             all(), message="标题名已存在")],
                                  help_text="组件标题")
    payload = serializers.CharField(required=True, help_text="组件实例格式")
    desc = serializers.CharField(required=True, help_text="组件介绍")
    choice_type = serializers.IntegerField(required=True, help_text="组件是否支持多选")
    is_private = serializers.IntegerField(required=True, help_text="组件是否公开")

    def create(self, validated_data):
        validated_data["template_id"] = self.context["template_id"]
        instance = TemplateConfigItem.objects.create(**validated_data)
        return instance

    def validate_template_item_info(self, template_item_info):
        template_item_info = list(template_item_info)
        if not template_item_info:
            raise serializers.ValidationError('组件配置信息为空')
        return template_item_info

    class Meta:
        model = Template
        exclude = ("create_time", "update_time",)


class UpdateTemplateInfoSerializer(serializers.Serializer):
    template_id = serializers.IntegerField(required=True, help_text="组件id")
    template_item_info = serializers.JSONField(required=True, help_text="组件配置信息")
    name = serializers.CharField(required=True, help_text="组件名")
    title = serializers.CharField(required=True, help_text="组件标题")
    desc = serializers.CharField(required=True, help_text="组件介绍")
    payload = serializers.CharField(required=True, help_text="组件实例格式")
    choice_type = serializers.IntegerField(required=True, help_text="组件是否支持多选")
    is_private = serializers.IntegerField(required=True, help_text="组件是否公开")

    def validate_template_id(self, template_id):
        template_record = Template.objects.filter(id=template_id, user_id=self.context["user"].id)
        if not template_record:
            raise serializers.ValidationError('组件无权限操作')
        return template_id

    def validate_template_item_info(self, template_item_info):
        template_item_info = list(template_item_info)
        if not template_item_info:
            raise serializers.ValidationError('组件配置信息为空')
        return template_item_info


class DeleteTmplateSerializer(serializers.Serializer):
    """
    删除缓存任务序列化器
    """
    template_id = serializers.IntegerField(required=True, help_text="删除缓存任务")

    def validate_template_id(self, template_id):
        if not Template.objects.filter(id=template_id, user_id=self.context["user"].id).exists():
            raise ValidationError('组件无权限操作')
        return template_id


class TemplateConfigItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemplateConfigItem
        fields = "__all__"
