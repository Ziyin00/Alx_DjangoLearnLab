#!/usr/bin/env python
"""
Simple Static Files Testing Script for Django Blog Authentication System
This script tests that all static files are being served correctly using curl.
"""

import subprocess
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
            result = subprocess.run(['curl', '-s', '-o', '/dev/null', '-w', '%{http_code}', url], 
                                  capture_output=True, text=True, timeout=10)
            status_code = result.stdout.strip()
            if status_code == "200":
                print(f"   ✅ {file_path} - Status: {status_code}")
            else:
                print(f"   ❌ {file_path} - Status: {status_code}")
        except Exception as e:
            print(f"   ❌ {file_path} - Error: {e}")
    
    # Test pages that use static files
    pages = [
        ("/", "Homepage"),
        ("/accounts/login/", "Login Page"),
        ("/accounts/register/", "Register Page"),
    ]
    
    print("\n📄 Testing Pages with Static Files:")
    for page_path, page_name in pages:
        url = base_url + page_path
        try:
            result = subprocess.run(['curl', '-s', url], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                content = result.stdout
                if 'static/css/style.css' in content:
                    print(f"   ✅ {page_name} - CSS loaded")
                else:
                    print(f"   ⚠️  {page_name} - CSS not found")
                
                if 'static/js/main.js' in content:
                    print(f"   ✅ {page_name} - JS loaded")
                else:
                    print(f"   ⚠️  {page_name} - JS not found")
            else:
                print(f"   ❌ {page_name} - Error: {result.stderr}")
        except Exception as e:
            print(f"   ❌ {page_name} - Error: {e}")
    
    print("\n🎉 Static Files Testing Complete!")
    print("=" * 60)

if __name__ == "__main__":
    test_static_files()
