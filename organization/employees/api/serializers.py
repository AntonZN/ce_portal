from abc import ABC

from rest_framework import serializers

from organization.employees.models import Employee


class EmployeeLikesSerializer(serializers.Serializer):
    count = serializers.IntegerField(read_only=True)


class EmployeeSearchSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    position = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_position(obj: Employee):
        try:
            return obj.position.name
        except AttributeError:
            return

    class Meta:
        model = Employee
        fields = ("pk", "avatar", "fio", "position")
