from django.db import models

# Create your models here.


# user registration model

class reg(models.Model):
    fullname = models.CharField(max_length=20)
    address = models.CharField(max_length=20)
    contact = models.IntegerField()
    cardno = models.CharField(max_length=12)
    card = models.CharField(max_length=12)
    password = models.CharField(max_length=20)
    image = models.ImageField()
    
# shop owner registraion model

class sreg(models.Model):
    fullname = models.CharField(max_length=20)
    address = models.CharField(max_length=20)
    contact = models.IntegerField()
    license = models.CharField(max_length=12)
    password = models.CharField(max_length=20)
    
    
# products add model

class pro(models.Model):
    license = models.IntegerField()
    image = models.ImageField()
    name = models.CharField(max_length=20)
    apl = models.CharField(max_length=20)
    bpl = models.CharField(max_length=20)
    ay = models.CharField(max_length=20)
    price = models.IntegerField()
    stock = models.IntegerField()
    
    
# shops add model

class shop(models.Model):
    license = models.IntegerField()
    image = models.ImageField()
    locality = models.CharField(max_length=20)
    time = models.CharField(max_length=20)

# feedback model

class feed(models.Model):
    cardno = models.CharField(max_length=12) 
    fullname = models.CharField(max_length=20)
    message = models.CharField(max_length=50)
    email = models.EmailField()
    
# add2cart model

class add2cart(models.Model):
    user = models.ForeignKey(reg, on_delete=models.CASCADE)  # Foreign key to User model
    product = models.ForeignKey(pro, on_delete=models.CASCADE)  # Foreign key to Product model
    quantity = models.IntegerField(default=1)  # Number of products added to the cart
    date_added = models.DateField(auto_now_add=True) 
    
    
# admin model

class super_user(models.Model):
    username=models.CharField(max_length=20)
    password=models.CharField(max_length=20)
    
# payment view

class Payment(models.Model):
    user = models.ForeignKey(reg, on_delete=models.CASCADE)
  # Store username or user ID
    
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    razorpay_order_id = models.CharField(max_length=100)
    razorpay_payment_id = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=50)
    products = models.TextField()  # Store product information as a string (e.g., JSON)

    def __str__(self):
        return f"Payment {self.id} - {self.user}"
    