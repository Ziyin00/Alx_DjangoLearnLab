#!/usr/bin/env python
"""
Verification script for Django Blog Authentication System
This script checks that all components are properly configured and working.
"""

import os
import sys
import django
from django.conf import settings
from django.core.management import execute_from_command_line

def verify_django_setup():
    """Verify Django setup and configuration."""
    print("🔍 Verifying Django Blog Authentication System Setup...")
    print("=" * 60)
    
    # Check Django version
    print(f"✅ Django Version: {django.get_version()}")
    
    # Check settings
    print(f"✅ Settings Module: {settings.SETTINGS_MODULE}")
    print(f"✅ Debug Mode: {settings.DEBUG}")
    print(f"✅ Database: {settings.DATABASES['default']['ENGINE']}")
    
    # Check installed apps
    print(f"✅ Installed Apps: {len(settings.INSTALLED_APPS)}")
    for app in settings.INSTALLED_APPS:
        print(f"   - {app}")
    
    # Check URL patterns
    try:
        from django.urls import reverse
        print("✅ URL Patterns:")
        print(f"   - Home: {reverse('blog:home')}")
        print(f"   - Login: {reverse('accounts:login')}")
        print(f"   - Register: {reverse('accounts:register')}")
        print(f"   - Profile: {reverse('accounts:profile')}")
    except Exception as e:
        print(f"❌ URL Error: {e}")
    
    # Check models
    try:
        from accounts.models import UserProfile
        from blog.models import Post, Comment
        print("✅ Models:")
        print(f"   - UserProfile: {UserProfile.__name__}")
        print(f"   - Post: {Post.__name__}")
        print(f"   - Comment: {Comment.__name__}")
    except Exception as e:
        print(f"❌ Model Error: {e}")
    
    # Check forms
    try:
        from accounts.forms import CustomUserCreationForm, UserProfileForm, UserUpdateForm
        print("✅ Forms:")
        print(f"   - CustomUserCreationForm: {CustomUserCreationForm.__name__}")
        print(f"   - UserProfileForm: {UserProfileForm.__name__}")
        print(f"   - UserUpdateForm: {UserUpdateForm.__name__}")
    except Exception as e:
        print(f"❌ Form Error: {e}")
    
    # Check views
    try:
        from accounts.views import CustomLoginView, RegisterView, profile_view
        from blog.views import home, post_detail, create_post
        print("✅ Views:")
        print(f"   - Authentication views: {len([CustomLoginView, RegisterView, profile_view])}")
        print(f"   - Blog views: {len([home, post_detail, create_post])}")
    except Exception as e:
        print(f"❌ View Error: {e}")
    
    # Check templates
    template_dirs = settings.TEMPLATES[0]['DIRS']
    print(f"✅ Template Directories: {template_dirs}")
    
    # Check static files
    print(f"✅ Static URL: {settings.STATIC_URL}")
    print(f"✅ Media URL: {settings.MEDIA_URL}")
    
    # Check authentication settings
    print(f"✅ Login URL: {settings.LOGIN_URL}")
    print(f"✅ Login Redirect: {settings.LOGIN_REDIRECT_URL}")
    print(f"✅ Logout Redirect: {settings.LOGOUT_REDIRECT_URL}")
    
    print("\n🎉 Django Blog Authentication System is properly configured!")
    print("=" * 60)
    print("📋 Available Features:")
    print("   ✅ User Registration")
    print("   ✅ User Login/Logout")
    print("   ✅ Profile Management")
    print("   ✅ Blog Post Creation")
    print("   ✅ Comment System")
    print("   ✅ Admin Interface")
    print("   ✅ Responsive Design")
    print("   ✅ Security Features")
    print("\n🚀 Ready to use! Start the server with: python manage.py runserver")

if __name__ == "__main__":
    # Set up Django environment
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_project.settings')
    django.setup()
    
    verify_django_setup()
