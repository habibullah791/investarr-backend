from rest_framework.response import Response
from rest_framework import serializers
from .models import CustomUser, Article, Video, ArticleImage
from django.contrib.auth import authenticate


import logging

logger = logging.getLogger(__name__)

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


    def validate(self, data):
        logger.debug(f"Attempting to authenticate user {data['username']}")
        print("UserLoginSerializer")
        print(data)
        user = authenticate(username=data['username'], password=data['password'])
        if user and user.is_active:
            logger.debug("Authentication successful")
            return user
        logger.error("Authentication failed: Invalid credentials")
        raise serializers.ValidationError("Invalid credentials")
    

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class InvestorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id','first_name', 'last_name', 'user_type', 'username', 'phone_number', 'profile_pic_url', 'address', 'area_of_interest', 'bio', 'membership_tier', 'verification_status', 'verification_badge')


class InvesteeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name', 'user_type', 'username', 'profile_pic_url', 'phone_number', 'address', 'area_of_interest', 'bio', 'startup_name', 'startup_idea', 'startup_description')

class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()
    

class InvestorInfoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('profile_pic_url', 'gallery_images', 'first_name', 'last_name', 'address', 'area_of_interest', 'bio', 'phone_number')

class InvesteeInfoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('profile_pic_url', 'gallery_images', 'first_name', 'last_name', 'address', 'area_of_interest', 'bio', 'phone_number', 'startup_name', 'startup_idea', 'startup_description')


class UserEmailPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'password')
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        instance = super().update(instance, validated_data)
        if password:
            instance.set_password(password)
            instance.save()
        return instance


class ArticleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleImage
        fields = '__all__'

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'

class ArticleSerializer(serializers.ModelSerializer):
    videos = VideoSerializer(many=True, read_only=True)
    images = ArticleImageSerializer(many=True, read_only=True)
    subtopics = serializers.SerializerMethodField()

    class Meta:
        model = Article
        exclude = ('subTopic_1', 'subTopic_2', 'subTopic_3', 'subTopic_1_description', 'subTopic_2_description', 'subTopic_3_description')

    def get_subtopics(self, obj):
        subtopics = []
        for i in range(1, 4):
            subtopic_field = f'subTopic_{i}'
            subtopic_description_field = f'subTopic_{i}_description'
            title = getattr(obj, subtopic_field)
            description = getattr(obj, subtopic_description_field)
            if title:
                subtopics.append({
                    'title': title,
                    'description': description
                })
        return subtopics