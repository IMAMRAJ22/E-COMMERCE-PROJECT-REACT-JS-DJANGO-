from django.db import models


class Login(models.Model):
    email=models.CharField(max_length=50)
    password=models.CharField(max_length=50)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    dob=models.DateField(null=True, blank=True)
    profile_img=models.ImageField(upload_to='profile_images/',null=True, blank=True)
    def __str__(self):
        return self.email

class Cartitem(models.Model):
    name=models.CharField(max_length=100)
    des=models.CharField(max_length=100)
    img=models.ImageField(upload_to='cart_images/',null=True,blank=True)
    def __str__(self):
        return self.name
    
class Products(models.Model):
    title=models.ForeignKey(Cartitem, on_delete=models.CASCADE,related_name='products')
    name=models.CharField(max_length=100)
    des=models.CharField(max_length=100)
    price=models.FloatField(max_length=100)
    pro_img=models.ImageField(upload_to='product_images/',blank=True,null=True)
    def __str__(self):
        return self.name
    
class Favourite(models.Model):
    product=models.ForeignKey(Products, on_delete=models.CASCADE,related_name='sections')
    user=models.ForeignKey(Login,on_delete=models.CASCADE,related_name='user')
    class Meta:
        unique_together=('product','user')
        
    def __str__(self):
        return f"{self.user.email} likes {self.product.name}"

class BuyItems(models.Model):
    user=models.ForeignKey(Login,on_delete=models.CASCADE, related_name='user_detail')
    product_id=models.ForeignKey(Products,on_delete=models.CASCADE,related_name='product_details')
    quantity=models.IntegerField(default=0)
    feedback=models.CharField(max_length=500)
    rating=models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user} bought {self.product_id}"

class SaveItems(models.Model):
    saved_user=models.ForeignKey(Login,on_delete=models.CASCADE, related_name='saved_user_details')
    saved_product_id=models.ForeignKey(Products,on_delete=models.CASCADE,related_name='saved_product_details')

    def __str__(self):
        return f"{self.saved_user} bought {self.saved_product_id}"
    
class LikeItems(models.Model):
    liked_user = models.ForeignKey(Login, on_delete=models.CASCADE, related_name='liked_user')
    liked_product_id = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='liked_product_id')
    
    def __str__(self):
        return f"{self.liked_user} liked {self.liked_product_id}"