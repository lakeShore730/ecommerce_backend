from rest_framework import serializers
from . models import Category, Product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class NestedCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
   

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'discount', 'quantity', 'description',  'category', 'user', 'is_active', 'primary_image', 'secondary_image1', 'secondary_image2', 'created_at', 'updated_at']
        extra_kwargs = {'user': {'read_only': True}}

    def create(self, validated_data):
        category = validated_data.pop('category', None)
        product = Product.objects.create(**validated_data, user=self.context['user'])
        product.category.set(category)
        product.save()
        return product

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.price = validated_data.get('price', instance.price)
        instance.discount = validated_data.get('discount', instance.discount)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.description = validated_data.get('description', instance.description)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.primary_image = validated_data.get('primary_image', instance.primary_image)
        instance.secondary_image1 = validated_data.get('secondary_image1', instance.secondary_image1)
        instance.secondary_image2 = validated_data.get('secondary_image2', instance.secondary_image2)
        
        if not validated_data.get('category') == None:
            instance.category.set(validated_data.get('category', instance.category))
        
        instance.save()
        return instance


class ProductListSerializer(serializers.ModelSerializer):
    category = NestedCategorySerializer(many=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'discount', 'quantity', 'description',  'category', 'user', 'is_active', 'primary_image', 'secondary_image1', 'secondary_image2', 'created_at', 'updated_at']
      
    