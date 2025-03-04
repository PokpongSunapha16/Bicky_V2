from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ("customer", "Customer"),
        ("admin", "Admin"),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="customer")

    groups = models.ManyToManyField(Group, related_name="customuser_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="customuser_permissions", blank=True)

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
    category = models.CharField(
        max_length=100,
        choices=(
            ('electronics', 'อิเล็กทรอนิกส์'),
            ('clothing', 'เสื้อผ้า'),
            ('accessories', 'อุปกรณ์เสริม'),
            ('home_appliances', 'เครื่องใช้ไฟฟ้าภายในบ้าน'),
            ('books', 'หนังสือ'),
            ('others', 'อื่นๆ')
        ),
        default='others'  # กำหนดค่าเริ่มต้นเป็น 'อื่นๆ'
    )


    def __str__(self):
        return self.name


# ✅ Cart Model
class Cart(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="cart")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    updated_at = models.DateTimeField(auto_now=True)  # ✅ เพิ่ม auto_now=True

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'รอดำเนินการ'),
        ('completed', 'สั่งซื้อสำเร็จ'),
        ('rejected', 'ถูกปฏิเสธ'),  # ✅ เพิ่มสถานะ "ไม่อนุมัติ"
    ]

    customer = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name="orders")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    payment_slip = models.ImageField(upload_to='payment_slips/', blank=True, null=True)  # ✅ อัปโหลดสลิป

    def approve_order(self):
        """ ✅ ฟังก์ชันสำหรับ Admin ใช้เปลี่ยนสถานะคำสั่งซื้อเป็น 'สั่งซื้อสำเร็จ' """
        self.status = 'completed'
        self.save()

    def reject_order(self):
        """ ❌ ฟังก์ชันสำหรับ Admin ใช้เปลี่ยนสถานะคำสั่งซื้อเป็น 'ถูกปฏิเสธ' """
        if self.payment_slip:
            self.payment_slip.delete()  # ✅ ลบไฟล์สลิปจากฐานข้อมูล
        self.status = 'rejected'
        self.save()

    def __str__(self):
        return f"Order {self.id} - {self.get_status_display()}"


# ✅ Order Items Model
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")  # ✅ ต้องมี related_name
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)  # ✅ เผื่อกรณีสินค้าถูกลบ
    product_name = models.CharField(max_length=255, default="Unknown Product")  # หรือค่าที่เหมาะสม
    product_description = models.TextField(blank=True, null=True)  # ✅ คำอธิบายสินค้า ณ ตอนนั้น
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # ✅ เก็บราคาสินค้าตอนสั่ง
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, editable=False)

    def save(self, *args, **kwargs):
        """ คำนวณ total_price ก่อนบันทึก """
        self.total_price = self.quantity * self.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product_name} x {self.quantity} ({self.total_price} บาท)"




# ✅ Payment Model
#class Payment(models.Model):
#    PAYMENT_METHODS = [
#        ('cod', 'Cash on Delivery'),
#        ('paypal', 'PayPal'),
#        ('stripe', 'Stripe'),
#    ]
#    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="payment")
#    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS)
#    transaction_id = models.CharField(max_length=255, blank=True, null=True)
#    paid = models.BooleanField(default=False)
#    paid_at = models.DateTimeField(blank=True, null=True)

class StorePayment(models.Model):
    order = models.ForeignKey('store.Order', on_delete=models.CASCADE, null=True, blank=True)
    payment_method = models.CharField(max_length=20)
    transaction_id = models.CharField(max_length=255, null=True, blank=True)
    paid = models.BooleanField(default=False)
    paid_at = models.DateTimeField(null=True, blank=True)
    receipt = models.ImageField(upload_to='receipts/', null=True, blank=True)  # เก็บไฟล์สลิป