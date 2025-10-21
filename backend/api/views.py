from django.shortcuts import render
from rest_framework import viewsets, status,generics
from .models import Login,Cartitem,Products,BuyItems,SaveItems,LikeItems
from .serializers import TaskSerializer,CartSerializer,ItemSerializer,LikeSerializer,BuySerializer,SaveSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import IntegrityError
from rest_framework.decorators import api_view, permission_classes
from django.http import JsonResponse
import requests
# views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
import numpy as np
import pandas as pd
from .models import Products
from .serializers import ItemSerializer
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.base import ContentFile

class LoginViewSet(viewsets.ModelViewSet):
    queryset = Login.objects.all()
    serializer_class = TaskSerializer

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cartitem.objects.all()
    serializer_class = CartSerializer

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ItemSerializer

class BuyViewSet(viewsets.ModelViewSet):
    queryset = BuyItems.objects.all()
    serializer_class = BuySerializer

    def create(self, request, *args, **kwargs):
        print("Request data:", request.data)  # ✅ Check what’s being received
        return super().create(request, *args, **kwargs)
    
class SaveViewSet(viewsets.ModelViewSet):
    queryset = SaveItems.objects.all()
    serializer_class = SaveSerializer

    def create(self, request, *args, **kwargs):
        print("Request data:", request.data)  # ✅ Check what’s being received
        return super().create(request, *args, **kwargs)
    
class LikeViewSet(viewsets.ModelViewSet):
    queryset=LikeItems.objects.all()
    serializer_class=LikeSerializer
    
    def create(self, request, *args, **kwargs):
        print("Request data: ", request.data)
        return super().create(request, *args, **kwargs)
    
#excel
class UploadExcelView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None):
        try:
            excel_file = request.FILES.get('file')
            if not excel_file:
                return Response({"error": "No file uploaded."}, status=status.HTTP_400_BAD_REQUEST)

            df = pd.read_excel(excel_file)
            
            # Check for the required columns
            required_cols = ["title", "name", "des", "price", "pro_img"]
            if not all(col in df.columns for col in required_cols):
                return Response(
                    {"error": f"Excel must contain columns: {', '.join(required_cols)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Loop through each row in the DataFrame
            for _, row in df.iterrows():
                # 1. Get or create the parent category (`Cartitem`)
                # The .get_or_create() method is perfect for this.
                cart_item, created = Cartitem.objects.get_or_create(
                    name=row['title']
                )
                
                
                pro_img_file = None
                image_url = row.get('pro_img')
                if image_url:
                    try:
                        response = requests.get(image_url, stream=True)
                        if response.status_code == 200:
                            # Create an in-memory file
                            pro_img_file = ContentFile(response.content)
                            # Give the file a name, e.g., using the last part of the URL
                            file_name = image_url.split('/')[-1]
                            pro_img_file.name = file_name
                    except requests.exceptions.RequestException as e:
                        print(f"Failed to download image from {image_url}: {e}")
                        # You can choose to skip this product or set pro_img to None

                # 2. Create the child product (`Products`)
                # Link the product to the parent using the 'title' foreign key
                Products.objects.create(
                    title=cart_item,
                    name=row['name'],
                    des=row['des'],
                    price=row['price'],
                    pro_img=pro_img_file if pro_img_file else None
                )

            return Response(
                {"message": "Excel data saved to DB successfully!"},
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )