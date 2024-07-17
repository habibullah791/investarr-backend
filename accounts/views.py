from django.http import Http404
from rest_framework import generics, status, serializers, permissions
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from django.core.mail import send_mail
from django.conf import settings
import random
from django.utils import timezone
from django.db.models import Q

from .utils import send_email
from .models import CustomUser, Article, Video, EmailReceived
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
    PaymentVerificationSerializer,
    ContactUsSerializer,
    OTPSerializer
)


from .email_templates import (
    HomePageCATEmailTemplate,
    SignUpEmailTemplate,
    ContactUsEmailTemplate
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
        instance = serializer.save()
        
        # Customize this part as per your needs
        first_name = instance.first_name
        last_name = instance.last_name
        content = SignUpEmailTemplate(first_name, last_name)
        
        # Example subject and sender
        subject = "Welcome to Investarr!"
        sender = settings.EMAIL_HOST_USER
        
        # Send email to the new user
        email_sent = send_email(subject, content, sender, [instance.email], settings.EMAIL_HOST_PASSWORD)
        
        if email_sent:
            print(f"Email sent successfully to {instance.email}!")
        else:
            print(f"Failed to send email to {instance.email}.")

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
    permission_classes = [AllowAny]

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

class ContactUsCreateView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = EmailReceived.objects.all()
    serializer_class = ContactUsSerializer

    def create(self, request, *args, **kwargs):
        print("ContactUsCreateView", request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Send email to the user
        recipient_email = serializer.validated_data.get('recipient_email')
        subject = f"Thank you for contacting Investarr, {request.data.get('name')}!"
        message = ContactUsEmailTemplate(request.data.get('name'))  # Get the HTML content
        sender_email = settings.EMAIL_HOST_USER
        
        # Send the email with HTML content
        send_mail(
            subject,
            message,  # This is plain text, for now, consider using `html_message`
            sender_email,
            [recipient_email],
            fail_silently=False,
            html_message=message  # Pass the HTML message here
        )

        return Response({
            'message': 'Email sent successfully!',
            'statusCode': status.HTTP_200_OK,
        }, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save()

class EmailReceivedCreateView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = EmailReceivedSerializer

    def post(self, request, *args, **kwargs):
        # Create a temporary data dictionary to include subject and content
        data = {
            'recipient_email': request.data.get('recipient_email'),
            'subject': "Find the Right Investor or Investee with Investarr",
            'content': HomePageCATEmailTemplate(),
        }

        # If user is authenticated, include user in the data
        if request.user.is_authenticated:
            data['user'] = request.user.id

        # Validate the data with the serializer
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        # Save email information to the database
        EmailReceived.objects.create(**serializer.validated_data)

        # Send the email
        email_sent = send_email(
            serializer.validated_data['subject'],
            serializer.validated_data['content'],
            settings.EMAIL_HOST_USER,
            [serializer.validated_data['recipient_email']],
            settings.EMAIL_HOST_PASSWORD
        )

        if email_sent:
            return Response({
                'message': 'Email sent successfully!',
                'statusCode': status.HTTP_200_OK,
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'message': 'Unable to send email at this time',
                'statusCode': status.HTTP_404_NOT_FOUND,
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GenerateOTPView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OTPSerializer

    def post(self, request, *args, **kwargs):

        # generate OTP
        otp = random.randint(1000, 9999)

        # send OTP to user
        subject = "OTP for Investarr"
        message = f"Your OTP is {otp}"
        sender_email = settings.EMAIL_HOST_USER
        recipient_email = request.user.email

        print("OTP", otp)
        print("recipient_email", recipient_email)
        print("sender_email", sender_email)
        print("subject", subject)

        user = request.user
        user.otp_code = otp
        user.otp_created_at = timezone.now()
        user.save()

        send_mail(
            subject,
            message,
            sender_email,
            [recipient_email],
            fail_silently=False,
        )

        return Response({
            'message': 'OTP sent successfully!',
            'statusCode': status.HTTP_200_OK,
        }, status=status.HTTP_200_OK)


class VerifyOTPView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OTPSerializer

    def post(self, request, *args, **kwargs):
        otp = request.data.get('otp')
        user = request.user
        print("user", user)
        print("otp", type(otp))
        print("user.otp_code", type(user.otp_code))

        if user.otp_code == otp and user.otp_created_at:
            time_difference = timezone.now() - user.otp_created_at
            if time_difference.total_seconds() <= 60:
                user.otp_code = None
                user.otp_created_at = None
                user.is_email_verified = True
                user.save()

                return Response({
                    'message': 'OTP verified successfully!',
                    'statusCode': status.HTTP_200_OK,
                }, status=status.HTTP_200_OK)
            
            return Response({
                'message': 'OTP expired!',
                'statusCode': status.HTTP_400_BAD_REQUEST,
            }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            'message': 'Invalid OTP!',
            'statusCode': status.HTTP_400_BAD_REQUEST,
        }, status=status.HTTP_400_BAD_REQUEST)
    