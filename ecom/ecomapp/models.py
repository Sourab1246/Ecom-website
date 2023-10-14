from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.
# class Cateogry(models.Model):
#     choices=models.ChoiceField()

class Product(models.Model):
    name=models.CharField(max_length=200)
    price=models.FloatField()
    discount_percent=models.PositiveIntegerField(default=0)
    description=models.TextField(max_length=200)
    image=models.ImageField(upload_to='products/')

    def discounted_price(self):
        return self.price * (1-self.discount_percent/100)
    def __str__(self):
        return self.name     

class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    products=models.ManyToManyField('Product',through='CartItem')
    @property
    def total_price(self):
      total=0
      for item in self.products.all():
         total += item.product.price*item.quantity
      return total    
class CartItem(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,default=0)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=0)



class PaymentOption(models.Model):
    name=models.CharField(max_length=50)
    description=models.TextField()

    def __str__(self):
        return self.name



class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    items=models.ManyToManyField(CartItem)
    total=models.DecimalField(max_digits=10,decimal_places=2)
    shipping_address = models.TextField(default=False)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    payment_option = models.CharField( max_length=20, choices=[("COD", "Cash on Delivery")],default=False)
    order_date=models.DateTimeField(default=timezone.now)
    is_paid = models.BooleanField(default=False)

    def mark_as_paid(self):
        self.is_paid = True
        self.save()


