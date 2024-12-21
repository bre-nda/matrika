from django.db import models

# Create your models here.

class Mattress(models.Model):
    TYPE_CHOICES = [
        ('plain', 'Plain Mattress'),
        ('quilted', 'Quilted Mattress'),
    ]
    SIZE_CHOICES = [
        ('3.5x6', '3.5 x 6 (42 x 74 inches)'),
        ('4x6', '4 x 6 (48 x 74 inches)'),
        ('5x6', '5 x 6 (60 x 74 inches)'),
        ('6x6', '6 x 6 (72 x 74 inches)'),
    ]
    THICKNESS_CHOICES = [
        (6, '6 inch'),
        (8, '8 inch'),
        (10, '10 inch'),
        (12, '12 inch'),
    ]

    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    size = models.CharField(max_length=5, choices=SIZE_CHOICES)
    thickness = models.PositiveIntegerField(choices=THICKNESS_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='mattresses/')
    
    def __str__(self):
        return f"{self.get_type_display()} - {self.size} - {self.thickness} inch"
    

# Pillow Modela
class Pillow(models.Model):
    material = models.CharField(max_length=50)  # e.g., 'Pure Fibre Filled'
    pair = models.BooleanField(default=True)  # Pillows are sold as pairs
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='bedding/pillows/')

    def __str__(self):
        return f"Pillow (Pair) - {self.material}"

# Bedsheet Model
class Bedsheet(models.Model):
    SIZE_CHOICES = [
        ('4x6', '4x6'),
        ('5x6', '5x6'),
        ('6x6', '6x6'),
    ]
    COLOR_CHOICES = [
        ('white', 'White'),
        ('light-blue', 'Light Blue'),
        ('brown', 'Brown'),
    ]
    size = models.CharField(max_length=10, choices=SIZE_CHOICES)
    material = models.CharField(max_length=50)  # e.g., 'Polyester'
    color = models.CharField(max_length=20, choices=COLOR_CHOICES, default='white')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='bedding/bedsheets/')

    def __str__(self):
        return f"{self.size} Bedsheet - {self.color}"

# Duvet Model
class Duvet(models.Model):
    SIZE_CHOICES = [
        ('4x6', '4x6'),
        ('5x6', '5x6'),
        ('6x6', '6x6'),
    ]
    COLOR_CHOICES = [
        ('white', 'White'),
        ('light-blue', 'Light Blue'),
        ('brown', 'Brown'),
    ]
    size = models.CharField(max_length=10, choices=SIZE_CHOICES)
    material = models.CharField(max_length=50)  # e.g., 'Cotton Microfibre'
    color = models.CharField(max_length=20, choices=COLOR_CHOICES, default='white')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='bedding/duvets/')

    def __str__(self):
        return f"{self.size} Duvet - {self.color}"
