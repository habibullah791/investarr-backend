from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    INVESTOR = 'Investor'
    INVESTEE = 'Investee'
    
    USER_TYPE_CHOICES = [
        (INVESTOR, 'Investor'),
        (INVESTEE, 'Investee'),
    ]

    MEMBERSHIP_TIER_CHOICES = [
        ('Free', 'Free'),
        ('Basic', 'Basic'),
        ('Standard', 'Standard'),
        ('Premium', 'Premium'),
        ('Premium Plus', 'Premium Plus'),
    ]

    VERIFICATION_STATUS_CHOICES = [
        ('Basic', 'Basic'),
        ('Level 1', 'Level 1'),
        ('Level 2', 'Level 2'),
    ]

    VERIFICATION_BADGE_CHOICES = [
        ('Basic', 'Basic'),
        ('Level 1', 'Level 1'),
        ('Level 2', 'Level 2'),
    ]

    PAYMENT_STATUS = [
        ('Pending', 'Pending'),
        ('Success', 'Success'),
    ]

    id = models.AutoField(primary_key=True)
    user_type = models.CharField(max_length=255, choices=USER_TYPE_CHOICES, blank=True, null=True)
    profile_pic_url = models.TextField(blank=True, null=True)
    gallery_images = models.JSONField(default=list)
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    area_of_interest = models.TextField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    membership_tier = models.CharField(max_length=255, choices=MEMBERSHIP_TIER_CHOICES, default='Free', blank=True, null=True)
    verification_status = models.CharField(max_length=255, choices=VERIFICATION_STATUS_CHOICES, blank=True, null=True)
    verification_badge = models.CharField(max_length=255, choices=VERIFICATION_BADGE_CHOICES, blank=True, null=True)
    startup_idea = models.TextField(blank=True, null=True)
    startup_name = models.CharField(max_length=255, blank=True, null=True)
    startup_description = models.TextField(blank=True, null=True)
    is_email_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)
    order_tracking_id = models.CharField(max_length=255, blank=True, null=True)
    merchant_reference = models.CharField(max_length=255, blank=True, null=True)
    payment_status = models.CharField(max_length=255, choices=PAYMENT_STATUS, blank=True, null=True)
    
    def __str__(self):
        return self.username


class Article(models.Model):
    title = models.CharField(max_length=255)
    previewText = models.CharField(max_length=255, blank=True, null=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    description = models.TextField()
    subTopic_1 = models.CharField(max_length=255, blank=True, null=True)
    subTopic_2 = models.CharField(max_length=255, blank=True, null=True)
    subTopic_3 = models.CharField(max_length=255, blank=True, null=True)
    subTopic_1_description = models.TextField(blank=True, null=True)
    subTopic_2_description = models.TextField(blank=True, null=True)
    subTopic_3_description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Video(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    video_url = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='videos', blank=True, null=True)

    def __str__(self):
        return self.title


class ArticleImage(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images/', blank=True)  # Correct the path here
    caption = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Image for {self.article.title}"
