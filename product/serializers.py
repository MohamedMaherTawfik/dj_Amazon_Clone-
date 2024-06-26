from rest_framework import serializers
from .models import Product,Brand,Review
from django.db.models.aggregates import Avg
from taggit.serializers import (TagListSerializerField,TaggitSerializer)
                                

class BrandListSerializers(serializers.ModelSerializer):
    class Meta:
        model=Brand
        fields="__all__"


class ProductListSerializers(serializers.ModelSerializer):
    brand=serializers.StringRelatedField()
    avg_rate=serializers.SerializerMethodField()
    reviews_count=serializers.SerializerMethodField()
    tags = TagListSerializerField()
    # price_with_tax=serializers.SerializerMethodField()
    
    class Meta:
        
        model=Product
        fields='__all__'
        
    def get_avg_rate(self,product):# Self = object
        avg= product.product_review.aggregate(rate_avg=Avg('rate'))
        if not avg['rate_avg']:
            result=0
            return result
        return avg['rate_avg']
    
    def get_reviews_count(self,product:Product):
        reviews=product.product_review.all().count()
        return reviews
    
    # def get_price_with_tax(self,product:Product):
    #     return product.price*1.5

class ReviewSerializers(serializers.ModelSerializer):
    class Meta:
        model=Review
        fields="__all__"
    
class ProductDetailSerializers(serializers.ModelSerializer):
    tags = TagListSerializerField()
    brand=serializers.StringRelatedField()
    avg_rate=serializers.SerializerMethodField()
    reviews_count=serializers.SerializerMethodField()
    reviews=ReviewSerializers(source='product_review',many=True)
    
    class Meta:
        model=Product
        fields='__all__'
        
    def get_avg_rate(self,product):# Self = object
        avg= product.product_review.aggregate(rate_avg=Avg('rate'))
        if not avg['rate_avg']:
            result=0
            return result
        return avg['rate_avg']
    
    def get_reviews_count(self,product:Product):
        reviews=product.product_review.all().count()
        return reviews
    


class BrandDetailSerializers(serializers.ModelSerializer):
    products=ProductListSerializers(source='Product_brand',many=True)
    
    class Meta:
        model=Brand
        fields="__all__"