from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView, ListAPIView, RetrieveAPIView

from .models import CustomUser, Article, Video
from .serializers import CustomUserSerializer, InvesteeInfoUpdateSerializer, InvestorInfoUpdateSerializer, LogoutSerializer, UserEmailPasswordSerializer, UserLoginSerializer, InvestorSerializer, InvesteeSerializer, ArticleSerializer, VideoSerializer

class UserCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        # Hash the password before saving the user
        validated_data = serializer.validated_data
        password = validated_data.get('password')
        if password:
            validated_data['password'] = make_password(password)
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