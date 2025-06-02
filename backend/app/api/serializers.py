from rest_framework import serializers
from app.models import *
from app.validator import validate_serial_number_mask

class EquipmentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentType
        fields = ['id', 'name', 'mask']


class EquipmentSerializer(serializers.ModelSerializer):
    eq_type_id = serializers.PrimaryKeyRelatedField(queryset=EquipmentType.objects.all(), source='eq_type')
    eq_type_name = serializers.CharField(source='eq_type.name', read_only=True)

    class Meta:
        model = Equipment
        fields = ['id', 'eq_type_id', 'serial_number', 'comment', 'eq_type_name']

    def validate(self, attrs):
        eq_type = attrs.get('eq_type')
        serial = attrs.get('serial_number')

        if not eq_type or not serial:
            return attrs

        if not validate_serial_number_mask(serial, eq_type.mask):
            raise serializers.ValidationError({
                "serial_number": f"Серийный номер не соответствует маске {eq_type.mask}"
            })

        return attrs
