from rest_framework import serializers
from .models import Advertisement

class AdvertisementSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Advertisement
        fields = '__all__'

    def get_image(self, obj):
        if not obj.image: 
            return None
        return self.context['request'].build_absolute_uri( obj.image.url)
