from rest_framework import serializers
from . models import Category, Product

class CategorySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = '__all__'

    def get_image(self, obj):
        if not obj.image: 
            return None
        return self.context['request'].build_absolute_uri( obj.image.url)


class NestedCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
   

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'discount', 'quantity', 'description',  'category', 'user', 'is_active', 'is_feature' 'primary_image', 'secondary_image1', 'secondary_image2', 'created_at', 'updated_at']
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
    # primary_image = serializers.ImageField(max_length=None, use_url=True, allow_null=False, required=True)
    primary_image = serializers.SerializerMethodField()
    secondary_image1 = serializers.SerializerMethodField()
    secondary_image2 = serializers.SerializerMethodField()


    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'discount', 'quantity', 'description',  'category', 'user', 'is_active', 'is_feature', 'primary_image', 'secondary_image1', 'secondary_image2', 'created_at', 'updated_at']
      
    def get_primary_image(self, obj):
        if not obj.primary_image: 
            return None
        return self.context['request'].build_absolute_uri( obj.primary_image.url)
    
    def get_secondary_image1(self, obj):
        if not obj.secondary_image1: 
            return None
        return self.context['request'].build_absolute_uri( obj.secondary_image1.url)

    def get_secondary_image2(self, obj):
        if not obj.secondary_image2: 
            return None
        return self.context['request'].build_absolute_uri( obj.secondary_image2.url)
