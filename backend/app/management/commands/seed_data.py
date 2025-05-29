from django.core.management.base import BaseCommand
from app.models import EquipmentType, Equipment


class Command(BaseCommand):
    help = 'Заполняет тестовые типы оборудования и записи, сгенерировано чатгпт, чтобы не тратить время'

    def handle(self, *args, **kwargs):
        Equipment.objects.all().delete()
        EquipmentType.objects.all().delete()

        types = [
            {
                "name": "TP-Link TL-WR74",
                "mask": "XXAAAAAXAA"
            },
            {
                "name": "D-Link DIR-300",
                "mask": "NXXAAXZXaa"
            },
            {
                "name": "D-Link DIR-300 E",
                "mask": "NAAAAXZXXX"
            },
        ]

        created_types = []

        for t in types:
            obj = EquipmentType.objects.create(name=t["name"], mask=t["mask"])
            created_types.append(obj)
            self.stdout.write(self.style.SUCCESS(f'Создан тип: {obj.name}'))

        equipment = [
            {
                "eq_type": created_types[0],
                "serial_number": "ABABCDE1BC",
                "comment": "Тестовый TP-Link"
            },
            {
                "eq_type": created_types[1],
                "serial_number": "1XZAB-xy",
                "comment": "Тестовый D-Link 1"
            },
            {
                "eq_type": created_types[1],
                "serial_number": "3RTCD_zz",
                "comment": "Тестовый D-Link 2"
            },
            {
                "eq_type": created_types[2],
                "serial_number": "5ABCD@9Z8",
                "comment": "Тестовый E-модель"
            },
            {
                "eq_type": created_types[0],
                "serial_number": "CDRTYU3DFT",
                "comment": "Ещё один TP-Link"
            }
        ]


        for e in equipment:
            Equipment.objects.create(**e)
            self.stdout.write(self.style.SUCCESS(f'Добавлено оборудование: {e["serial_number"]}'))
