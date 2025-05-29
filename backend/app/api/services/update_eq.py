from app.models import Equipment
from app.validator import validate_serial_number_mask
from rest_framework.exceptions import ValidationError

def update_equipment(instance, validated_data):
    eq_type = validated_data.get('eq_type', instance.eq_type)
    serial = validated_data.get('serial_number', instance.serial_number)
    comment = validated_data.get('comment', instance.comment)

    if not validate_serial_number_mask(serial, eq_type.mask):
        raise ValidationError(f"Серийный номер не соответствует маске {eq_type.mask}")

    if Equipment.objects.exclude(pk=instance.pk).filter(eq_type=eq_type, serial_number=serial, is_active=True).exists():
        raise ValidationError("Серийный номер уже существует")


    instance.eq_type = eq_type
    instance.serial_number = serial
    instance.comment = comment
    instance.save()
    return instance