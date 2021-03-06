#!/user/bin/even Python3
# -*- coding:utf-8 -*-
# serializers.py
# 序列化器定义
# author:zhaohexin
# time：2019/12/27 11:53 上午

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from projects.models import Projects
from interfaces.models import Interfaces
from . import models
from envs.models import EnvsModel


class ProjectsModelSerializers(serializers.ModelSerializer):
    """
    定义父表序列化器
    """

    class Meta:
        model = Projects
        fields = "__all__"


class InterfacesSerializers(serializers.ModelSerializer):
    """
    定义接口模型序列化器
    """
    # 获取父表项目名称，默认read_only=true
    project = serializers.StringRelatedField(label="所属项目名称", help_text="所属项目名称")
    # 从新指认项目ID
    project_id = serializers.PrimaryKeyRelatedField(queryset=Projects.objects.all(), label="项目ID", help_text="项目ID",
                                                    write_only=True)

    class Meta:
        """
        设置元数据属性
        """
        # 设置自动生成模型
        model = models.Interfaces
        # 指定所需字段
        fields = ("id", "name", "tester", "create_time", "desc", "project", "project_id")

    # 重写update
    def update(self, instance, validated_data):
        if 'project_id' in validated_data:
            project = validated_data.pop('project_id')
            validated_data['project'] = project

        return super().update(instance, validated_data)

    # 重写create
    def create(self, validated_data):
        validated_data["project_id"] = validated_data["project_id"].id
        interface_obj = super().create(validated_data)
        return interface_obj


# 定义全局环境变量序列化校验器
class InterfaceRunSerializers(serializers.ModelSerializer):
    """
    定义全局环境变量序列化校验器
    """
    env_id = serializers.IntegerField(write_only=True, label="全局变量ID", help_text="全局变量ID")

    class Meta:
        model = Interfaces
        fields = ("id", "env_id")

    def validate(self, attrs):
        """
        校验 env_id是否存在
        :param attrs: 传入参数attrs
        :return:传出参数attrs
        """
        # 判断env_id是否存在
        if EnvsModel.objects.filter(id=attrs.get("env_id")).exists():
            return attrs
        else:
            raise serializers.ValidationError("所选接口不存在！")

