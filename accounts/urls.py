from django.urls import path
from .views import ArticleListView, ArticleDetailView, VideoListView, InvesteeInfoUpdateView, InvestorInfoUpdateView, UserEmailPasswordUpdateView, UserLoginView, UserCreateView, UserDetailView, LogoutView, InvestorDataView, InvesteeDataView

urlpatterns = [
    path('articles/', ArticleListView.as_view(), name='article-list'),
    path('articles/<int:pk>/', ArticleDetailView.as_view(), name='article-detail'),
    path('videos/', VideoListView.as_view(), name='video-list'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('signup/', UserCreateView.as_view(), name='user-create'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('logout/', LogoutView.as_view(), name='user-logout'),
    path('investors_data/', InvestorDataView.as_view(), name='investor-data'),
    path('investee_data/', InvesteeDataView.as_view(), name='investee-data'),
    path('investor-info/update/<int:pk>/', InvestorInfoUpdateView.as_view(), name='investor_update'),
    path('investee-info/update/<int:pk>/', InvesteeInfoUpdateView.as_view(), name='investor_update'),
    path('email-pass/update/<int:pk>/', UserEmailPasswordUpdateView.as_view(), name='investor_update'),
]
