#!/usr/bin/env python
"""
Static Files Testing Script for Django Blog Authentication System
This script tests that all static files are being served correctly.
"""

import requests
import sys

def test_static_files():
    """Test that all static files are being served correctly."""
    base_url = "http://127.0.0.1:8001"
    
    print("🔍 Testing Static Files for Django Blog Authentication System...")
    print("=" * 60)
    
    # Test static files
    static_files = [
        "/static/css/style.css",
        "/static/js/main.js",
    ]
    
    print("📁 Testing Static Files:")
    for file_path in static_files:
        url = base_url + file_path
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"   ✅ {file_path} - Status: {response.status_code}")
            else:
                print(f"   ❌ {file_path} - Status: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"   ❌ {file_path} - Error: {e}")
    
    # Test pages that use static files
    pages = [
        ("/", "Homepage"),
        ("/accounts/login/", "Login Page"),
        ("/accounts/register/", "Register Page"),
        ("/accounts/profile/", "Profile Page"),
    ]
    
    print("\n📄 Testing Pages with Static Files:")
    for page_path, page_name in pages:
        url = base_url + page_path
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                # Check if CSS is referenced
                if 'static/css/style.css' in response.text:
                    print(f"   ✅ {page_name} - CSS loaded (Status: {response.status_code})")
                else:
                    print(f"   ⚠️  {page_name} - CSS not found (Status: {response.status_code})")
                
                # Check if JS is referenced
                if 'static/js/main.js' in response.text:
                    print(f"   ✅ {page_name} - JS loaded")
                else:
                    print(f"   ⚠️  {page_name} - JS not found")
            else:
                print(f"   ❌ {page_name} - Status: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"   ❌ {page_name} - Error: {e}")
    
    print("\n🎉 Static Files Testing Complete!")
    print("=" * 60)

if __name__ == "__main__":
    test_static_files()
