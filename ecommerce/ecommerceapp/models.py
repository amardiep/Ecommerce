from django.db import models

# Create your models here.
class Contact(models.Model):
    #userid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    desc = models.TextField(max_length=500)

    def __str__(self):
        return self.email



class Product(models.Model):
    productid= models.AutoField
    productname= models.CharField(max_length=200,default="")
    category = models.CharField(max_length=200,default="")
    subcategory = models.CharField(max_length=200,default="")
    price = models.IntegerField(unique=True,default=0)
   #credit = models.DecimalField(max_digits=6, decimal_places=2)
    desc = models.CharField(max_length=5000)
    image = models.ImageField(upload_to='images/images',default="")

    def __str__(self):
        return self.productname

class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    items_json = models.CharField(max_length=5000)
    amount= models.IntegerField(default=0)
    name= models.CharField(max_length=200)
    email = models.CharField(max_length=100)
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50,default="")
    zip_code = models.CharField(max_length=50)
    oid = models.CharField(max_length=150,blank=True)
    amountpaid = models.CharField(max_length=500,blank=True,null=True)
    paymentstatus = models.CharField(max_length=200,blank=True)
    phone = models.CharField(max_length=100,default="")
    
    
    def __str__(self):
        return self.name
    

class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=500)
    delivered = models.BooleanField(default=False)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.timestamp