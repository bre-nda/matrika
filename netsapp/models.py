from django.db import models
from django.contrib.auth.models import User

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
    

# Pillow Model
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
    
    
# Cart Model
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product_type = models.CharField(max_length=50)  # e.g., "mattress", "pillow"
    product_id = models.PositiveIntegerField()  # ID of the product in its respective table
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product_type.capitalize()} - {self.quantity}"
    
    
#profile model
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    shipping_address = models.OneToOneField('ShippingAddress', on_delete=models.SET_NULL, null=True)
    billing_address = models.OneToOneField('BillingAddress', on_delete=models.SET_NULL, null=True)

class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100)
    street_address = models.CharField(max_length=255)
    flat_suite = models.CharField(max_length=255, blank=True, null=True)
    town_city = models.CharField(max_length=100)
    state_county = models.CharField(max_length=100)
    postcode = models.CharField(max_length=20)
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(max_length=100)

class BillingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100)
    street_address = models.CharField(max_length=255)
    flat_suite = models.CharField(max_length=255, blank=True, null=True)
    town_city = models.CharField(max_length=100)
    state_county = models.CharField(max_length=100)
    postcode = models.CharField(max_length=20)
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(max_length=100)
  
#order model    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, choices=[('pending', 'Pending'), ('completed', 'Completed')], default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.TextField(null=True, blank=True)  # Allow null and blank
    billing_address = models.TextField(null=True, blank=True)  # Allow null and blank


    def __str__(self):
        return f"Order {self.id} - {self.status}"

    def get_order_items(self):
        return self.order_items.all()

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product_name} x{self.quantity}"