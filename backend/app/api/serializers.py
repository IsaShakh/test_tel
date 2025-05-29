from rest_framework import serializers
from app.models import *
from app.validator import validate_serial_number_mask

class EquipmentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentType
        fields = ['id', 'name', 'mask']


class EquipmentSerializer(serializers.ModelSerializer):
    type_id = serializers.PrimaryKeyRelatedField(queryset=EquipmentType.objects.all(), source='eq_type')

    class Meta:
        model = Equipment
        fields = ['id', 'type_id', 'serial_number', 'comment']

    def validate_serial_number(self, value):
        equipment_type = self.initial_data.get("type_id")
        mask = EquipmentType.objects.get(id=equipment_type).mask
        if not validate_serial_number_mask(value, mask):
            raise serializers.ValidationError("Серийный номер не прошел валидацию")
        return value
    