from rest_framework import serializers
from .models import Login,Cartitem,Products,Favourite,BuyItems,LikeItems,SaveItems

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Login
        fields = '__all__'

    # class Meta:
    #     model = Cartitem
    #     fields = '__all__'
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cartitem
        fields = '__all__'

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourite
        fields = ['id', 'user', 'product']

class BuySerializer(serializers.ModelSerializer):
    user_email=serializers.CharField(source='user.email', read_only=True)
    product_name=serializers.CharField(source='product_id.name', read_only=True)
    product_price=serializers.IntegerField(source='product_id.price',read_only=True)
    product_image=serializers.ImageField(source='product_id.pro_img', read_only=True)
    class Meta:
        model = BuyItems
        fields = ['id', 'user','product_id','quantity','feedback','rating', 'user_email', 'product_name', 'product_price', 'product_image']
        
        
class SaveSerializer(serializers.ModelSerializer):
    user_emails=serializers.CharField(source='user.email', read_only=True)
    product_names=serializers.CharField(source='product_id.name', read_only=True)
    product_prices=serializers.IntegerField(source='product_id.price',read_only=True)
    product_images=serializers.ImageField(source='product_id.pro_img', read_only=True)
    class Meta:
        model = SaveItems
        fields = ['id', 'saved_user','saved_product_id', 'user_emails', 'product_names', 'product_prices', 'product_images']
        
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=SaveItems.objects.all(),
                fields=["saved_user", "saved_product_id"],
                message="You already saved this Item..."
            )
        ]
        
class LikeSerializer(serializers.ModelSerializer):
    liked_user_emails=serializers.CharField(source='liked_user.email', read_only=True)
    liked_product_names=serializers.CharField(source='liked_product_id.name', read_only=True)
    liked_product_prices=serializers.IntegerField(source='liked_product_id.price',read_only=True)
    liked_product_images=serializers.ImageField(source='liked_product_id.pro_img', read_only=True)
    class Meta:
        model=LikeItems
        fields=['id', 'liked_user','liked_product_id', 'liked_user_emails', 'liked_product_names', 'liked_product_prices', 'liked_product_images']
        
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=LikeItems.objects.all(),
                fields=["liked_user", "liked_product_id"],
                message="You're already Liked this Item..."
            )
        ]