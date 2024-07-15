from django.http import Http404
from rest_framework import generics, status, serializers
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from django.core.mail import send_mail
from django.conf import settings
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from django.db.models import Q

from .models import CustomUser, Article, Video
from rest_framework.generics import (
    UpdateAPIView,
    ListAPIView,
)
from .serializers import (
    CustomUserSerializer,
    InvesteeInfoUpdateSerializer,
    InvestorInfoUpdateSerializer,
    LogoutSerializer,
    UserEmailPasswordSerializer,
    UserLoginSerializer,
    InvestorSerializer,
    InvesteeSerializer,
    ArticleSerializer,
    VideoSerializer,
    UserVerificationStatusSerializer,
    EmailReceivedSerializer,
    OrderTrackingSerializer,
    OrderRetrieveSerializer,
    PaymentVerificationSerializer
)

class UserLoginView(TokenObtainPairView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)
        user_data = CustomUserSerializer(user).data

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": user_data
        })

class UserCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save()

class UserDetailView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response(serializer.data)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        print("LogoutView", request.data)
        serializer = LogoutSerializer(data=request.data)
        if serializer.is_valid():
            refresh_token = serializer.validated_data["refresh_token"]
            try:
                token = RefreshToken(refresh_token)
                # token.blacklist()
                return Response({"message": "You have successfully logged out."}, status=status.HTTP_205_RESET_CONTENT)
            except Exception as e:
                return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class InvestorDataView(generics.ListAPIView):
    serializer_class = InvestorSerializer
    permission_classes = [AllowAny]


    def get_queryset(self):
        return CustomUser.objects.filter(user_type=CustomUser.INVESTOR)

class InvesteeDataView(generics.ListAPIView):
    serializer_class = InvesteeSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return CustomUser.objects.filter(user_type=CustomUser.INVESTEE)

class CertifiedUserDataView(generics.ListAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return CustomUser.objects.filter(Q(verification_status='Level 2'))
    
class InvestorInfoUpdateView(UpdateAPIView):
    serializer_class = InvestorInfoUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CustomUser.objects.filter(user_type=CustomUser.INVESTOR)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        try:
            self.perform_update(serializer)
        except Exception as e:
            # If the update operation fails, return an error response
            return Response({
                'message': 'Failed to update investor profile.',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Serialize the updated instance and return it along with a success message
        updated_user = self.get_queryset().get(pk=instance.pk)  # Retrieve the updated instance
        serialized_user = self.get_serializer(updated_user).data  # Serialize the updated instance
        return Response({
            'message': 'Investor profile updated successfully.',
            'user': serialized_user
        }, status=status.HTTP_200_OK)

class InvesteeInfoUpdateView(UpdateAPIView):
    serializer_class = InvesteeInfoUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CustomUser.objects.filter(user_type=CustomUser.INVESTEE)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        try:
            self.perform_update(serializer)
        except Exception as e:
            # If the update operation fails, return an error response
            return Response({
                'message': 'Failed to update investee profile.',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

        updated_user = self.get_queryset().get(pk=instance.pk)

        serialized_user = self.get_serializer(updated_user).data
        return Response({
            'message': 'Investee profile updated successfully.',
            'user': serialized_user
        }, status=status.HTTP_200_OK)

class UserEmailPasswordUpdateView(UpdateAPIView):
    serializer_class = UserEmailPasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CustomUser.objects.all()
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        try:
            self.perform_update(serializer)
        except Exception as e:
            return Response({
                'message': 'Failed to update user email and password.',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        
        updated_user = self.get_queryset().get(pk=instance.pk)
        serialized_user = self.get_serializer(updated_user).data
        return Response({
            'message': 'User email and password updated successfully.',
            'user': serialized_user
        }, status=status.HTTP_200_OK)

class ArticleListView(ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = {
            'statusCode': status.HTTP_200_OK,
            'data': serializer.data,
            'message': 'Articles retrieved successfully.'
        }
        return Response(data)

class ArticleDetailView(generics.RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        article = self.get_object()
        serializer = self.get_serializer(article)
        return Response(serializer.data)
    
class VideoListView(ListAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = {
            'statusCode': status.HTTP_200_OK,
            'data': serializer.data,
            'message': 'Videos retrieved successfully.'
        }
        return Response(data)

class CurrentUserVerificationStatusView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserVerificationStatusSerializer

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user)
        data = {
            'statusCode': status.HTTP_200_OK,
            'data': serializer.data,
            'message': 'User verification status retrieved successfully.'
        }
        return Response(data)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({
            'statusCode': status.HTTP_201_CREATED,
            'data': response.data,
            'message': 'Email sent and data saved successfully.'
        })

class OrderTrackingCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderTrackingSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        user.merchant_reference = serializer.validated_data['merchant_reference']
        user.order_tracking_id = serializer.validated_data['order_tracking_id']
        user.membership_tier = serializer.validated_data['membership_tier']
        user.save()

        return Response({
            'statusCode': status.HTTP_201_CREATED,
            'message': 'Order tracking information saved successfully.'
        })

class OrderRetrieveView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderRetrieveSerializer

    def get_object(self):
        order_tracking_id = self.kwargs['order_tracking_id']
        try:
            return CustomUser.objects.get(order_tracking_id=order_tracking_id)
        except CustomUser.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        try:
            user = self.get_object()
            serializer = self.get_serializer(user)
            return Response({
                'statusCode': status.HTTP_200_OK,
                'data': serializer.data,
                'message': 'Order tracking information retrieved successfully.'
            }, status=status.HTTP_200_OK)
        except Http404:
            return Response({
                'statusCode': status.HTTP_200_OK,
                'message': 'Order tracking ID not found.'
            }, status=status.HTTP_200_OK)

class PasswordResetView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        confirm_password = request.data.get("confirm_password")

        if not username or not password or not confirm_password:
            return Response({"message": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

        if password != confirm_password:
            return Response({
                "message": "Passwords do not match."
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(username=username)
            user.set_password(password)
            user.save()
            return Response({"message": "Password reset successful."}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({
                "message": "User not found."
            }, status=status.HTTP_404_NOT_FOUND)


class PaymentVerificationView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentVerificationSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user_id = kwargs.get('pk')
        payment_status = serializer.validated_data['payment_status']
        
        try:
            user = CustomUser.objects.get(id=user_id)
            user.payment_status = payment_status
            user.save()
            return Response({
                'statusCode': status.HTTP_200_OK,
                'message': 'Payment status updated successfully.'
            })
        except CustomUser.DoesNotExist:
            return Response({
                'statusCode': status.HTTP_404_NOT_FOUND,
                'message': 'User not found.'
            }, status=status.HTTP_404_NOT_FOUND)
        

class EmailReceivedCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmailReceivedSerializer

    def perform_create(self, serializer):
        # Save the email received data
        email_received = serializer.save()
        print("Email received", email_received)
        
        # Send the email using custom function
        sender = settings.DEFAULT_FROM_EMAIL
        recipients = ['shahid.habib791@gmail.com']
        subject = email_received.subject
        body = email_received.content
