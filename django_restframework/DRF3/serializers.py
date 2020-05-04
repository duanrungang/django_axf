from rest_framework import serializers

from DRF3.models import User, Blog


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'u_name', 'u_password']


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['id', 'b_title', 'b_content']
