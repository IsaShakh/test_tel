from app.models import Equipment, EquipmentType
from app.validator import validate_serial_number_mask

def create_equipment_batch(equipment_list):
    """Метод для создания equipment, позволяет выводить инфу о всех серийниках не выбрасывая исключение на первом же неправильном."""
    created = []
    errors = []

    for item in equipment_list:
        type_id = item.get("type_id")
        serial = item.get("serial_number")
        comment = item.get("comment", "")

        try:
            eq_type = EquipmentType.objects.get(id=type_id)
        except EquipmentType.DoesNotExist:
            errors.append({serial: "Тип оборудования не найден"})
            continue

        if not validate_serial_number_mask(serial, eq_type.mask):
            errors.append({serial: f"Не соответствует маске {eq_type.mask}"})
            continue

        if Equipment.objects.filter(eq_type=eq_type, serial_number=serial, is_active=True).exists():
            errors.append({serial: "Такой серийный номер уже существует"})
            continue


        equipment = Equipment.objects.create(eq_type=eq_type, serial_number=serial, comment=comment)
        created.append(equipment)

    return created, errors