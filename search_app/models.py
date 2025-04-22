import logging
from django.db import models
from accounts.models import CustomUser
from django.contrib.auth import get_user_model
from PIL import Image

# ロガーの設定
logger = logging.getLogger(__name__)

class Category(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="products")

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     if self.image:
    #         try:
    #             img = Image.open(self.image.path)
    #             if img.height > 400 or img.width > 400:
    #                 output_size = (400, 400)
    #                 img.thumbnail(output_size)
    #                 img.save(self.image.path)
    #         except Exception as e:
    #             logger.error(f"Image processing error: {e}")
    #             raise

class Favorite(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='favorites')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorited_by')

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"

class Cart(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='cart')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='in_cart')
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name} (x{self.quantity})"

class PurchaseHistory(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='purchase_history')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='purchase_history')
    purchased_at = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user.username} - {self.product.name} (x{self.quantity}) - {self.purchased_at}"