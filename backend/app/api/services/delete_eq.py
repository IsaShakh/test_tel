def delete_equipment(instance):
    """Мето для удаления"""
    instance.is_active = False
    instance.save()
    return instance