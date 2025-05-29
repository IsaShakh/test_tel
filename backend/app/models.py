from django.db import models


class EquipmentType(models.Model):
    name = models.CharField(max_length=100)
    mask = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name


class Equipment(models.Model):
    eq_type = models.ForeignKey(EquipmentType, on_delete=models.CASCADE)
    serial_number = models.CharField(max_length=50)
    comment = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.serial_number
    

    