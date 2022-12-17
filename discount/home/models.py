from django.db import models

# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=122)
    email= models.CharField(max_length=122)
    desc = models.TextField()
    date = models.DateField()

    def __str__(self):
        return self.name 

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=50)
    category = models.CharField(max_length=50, default="")
    sub_category = models.CharField(max_length=50,default="")
    price = models.IntegerField(default=0)
    desc = models.CharField(max_length=500)
    date = models.DateField()
    image = models.ImageField(upload_to="static/images",default="")

    def __str__(self):
        return self.product_name 



class ScrappedProduct(models.Model):
    title = models.CharField(max_length=500)
    image = models.ImageField(upload_to='images')
    rating = models.FloatField()


    def __str__(self):
        return self.title
    

class Search(models.Model):
    title = models.CharField(max_length=500)
    image = models.ImageField(upload_to='images')
    rating = models.FloatField()


    def __str__(self):
        return self.title