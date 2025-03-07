from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Article, Video, ArticleImage, EmailReceived


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = [
        'id', 'username', 'first_name', 'last_name', 'email', 'user_type', 'payment_status' ,
        'address','membership_tier', 'verification_status', 'verification_badge', 'is_email_verified',
        'startup_name', 'is_staff', 'is_active',
        'last_login', 'date_joined'
    ]
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Custom info', {'fields': (
            'user_type', 'profile_pic_url','gallery_images', 'address', 'area_of_interest', 'bio', 
            'membership_tier', 'payment_status','verification_status', 'verification_badge', 
             'startup_name', 'startup_idea', 'startup_description', 'order_tracking_id'
        )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
        }),
        ('Custom info', {'fields': (
            'user_type', 'profile_pic_url', 'address', 'area_of_interest', 'bio', 
            'membership_tier', 'verification_status', 'verification_badge', 
            'startup_idea', 'startup_name', 'startup_description'
        )}),
    )
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)


class ArticleImageInline(admin.TabularInline):
    model = ArticleImage
    extra = 1

class ArticleAdmin(admin.ModelAdmin):
    inlines = [ArticleImageInline]
    list_display = ('title', 'previewText', 'author', 'created_at', 'is_published')
    list_filter = ('is_published', 'created_at', 'author')
    search_fields = ('title', 'author__username', 'description')

class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'is_published', 'article')
    list_filter = ('is_published', 'created_at', 'author', 'article')
    search_fields = ('title', 'author__username', 'video_url')


class EmailReceivedAdmin(admin.ModelAdmin):
    list_display = ('recipient_email', 'subject', 'received_at', 'is_read', 'is_deleted')
    list_filter = ('is_read', 'is_deleted', 'received_at')
    search_fields = ( 'subject', 'content')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(EmailReceived, EmailReceivedAdmin)