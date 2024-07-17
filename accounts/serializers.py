from rest_framework.response import Response
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password

import logging
from .models import CustomUser, Article, Video, ArticleImage,EmailReceived


logger = logging.getLogger(__name__)

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        logger.debug(f"Attempting to authenticate user {data['username']}")
        user = authenticate(username=data['username'], password=data['password'])
        
        if user and user.is_active:
            logger.debug("Authentication successful")
            return user
        logger.error("Authentication failed: Invalid credentials")
        raise serializers.ValidationError("Invalid credentials")
 

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name', 'user_type', 'username', 'email', 'phone_number', 'profile_pic_url', 'address', 'area_of_interest', 'bio', 'membership_tier', 'verification_status', 'verification_badge', 'startup_name', 'startup_idea', 'startup_description', 'gallery_images', 'password', 'is_email_verified', 'is_phone_verified', 'order_tracking_id', 'merchant_reference', 'payment_status')

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
    

class InvestorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id','first_name', 'last_name', 'user_type', 'username', 'phone_number', 'profile_pic_url', 'address', 'area_of_interest', 'bio', 'membership_tier', 'verification_status', 'verification_badge')


class InvesteeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name', 'user_type', 'username', 'phone_number', 'profile_pic_url',  'address', 'area_of_interest', 'bio', 'membership_tier',  'verification_status', 'verification_badge', 'startup_name', 'startup_idea', 'startup_description')

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
    

class UserVerificationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'verification_badge', 'verification_status', 'membership_tier')


class OrderTrackingSerializer(serializers.Serializer):
    merchant_reference = serializers.CharField()
    order_tracking_id = serializers.CharField()
    membership_tier = serializers.CharField()


class OrderRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('merchant_reference', 'order_tracking_id')


class PaymentVerificationSerializer(serializers.Serializer):
    payment_status = serializers.CharField()

class EmailReceivedSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), required=False)

    class Meta:
        model = EmailReceived
        fields = ('id', 'recipient_email', 'subject', 'content', 'received_at', 'is_read', 'is_deleted', 'user')
        extra_kwargs = {
            'subject': {'required': False},  # Make subject optional
            'content': {'required': False},  # Make content optional
        }


class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailReceived
        fields = ('recipient_email', 'subject', 'content')

    def create(self, validated_data):
        return EmailReceived.objects.create(**validated_data)


class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('otp_code', 'otp_created_at')