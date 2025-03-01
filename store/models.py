from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ("customer", "Customer"),
        ("seller", "Seller"),
        ("admin", "Admin"),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="customer")

    groups = models.ManyToManyField(Group, related_name="customuser_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="customuser_permissions", blank=True)

    def is_seller(self):
        return self.role == "seller"

    def is_customer(self):
        return self.role == "customer"

    def is_admin(self):
        return self.role == "admin"


class Profile(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField(null=True, blank=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title


# ✅ Product Model (ใช้ CustomUser เป็น Seller)
class Product(models.Model):
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)  # ✅ อนุญาตให้ว่างได้
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# ✅ Cart Model
class Cart(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="cart")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    updated_at = models.DateTimeField(auto_now=True)  # ✅ เพิ่ม auto_now=True


# ✅ Order Model
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
    ]
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="orders")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)


# ✅ Order Items Model
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")  # ✅ ต้องมี related_name
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def total_price(self):
        return self.quantity * self.price



# ✅ Payment Model
class Payment(models.Model):
    PAYMENT_METHODS = [
        ('cod', 'Cash on Delivery'),
        ('paypal', 'PayPal'),
        ('stripe', 'Stripe'),
    ]
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="payment")
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS)
    transaction_id = models.CharField(max_length=255, blank=True, null=True)
    paid = models.BooleanField(default=False)
    paid_at = models.DateTimeField(blank=True, null=True)