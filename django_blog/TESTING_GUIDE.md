# Django Blog Authentication System - Testing Guide

## Overview

This guide provides comprehensive testing instructions for the Django blog authentication system. Follow these steps to verify that all authentication features are working correctly.

## Prerequisites

1. Ensure the Django server is running:

   ```bash
   python manage.py runserver
   ```

2. Access the application at: http://127.0.0.1:8000/

## Test Scenarios

### 1. User Registration Testing

#### Test Case 1.1: Successful Registration

1. Navigate to http://127.0.0.1:8000/accounts/register/
2. Fill out the registration form:
   - Username: `testuser`
   - First Name: `Test`
   - Last Name: `User`
   - Email: `test@example.com`
   - Password: `testpass123`
   - Password Confirmation: `testpass123`
3. Click "Create Account"
4. **Expected Result**: Success message displayed, redirected to login page

#### Test Case 1.2: Registration with Invalid Data

1. Navigate to http://127.0.0.1:8000/accounts/register/
2. Try to register with:
   - Username: `test` (too short)
   - Email: `invalid-email` (invalid format)
   - Password: `123` (too short)
   - Password Confirmation: `456` (doesn't match)
3. Click "Create Account"
4. **Expected Result**: Validation errors displayed, form not submitted

#### Test Case 1.3: Duplicate Username

1. Try to register with an existing username
2. **Expected Result**: Error message about username already existing

### 2. User Login Testing

#### Test Case 2.1: Successful Login

1. Navigate to http://127.0.0.1:8000/accounts/login/
2. Enter credentials:
   - Username: `testuser`
   - Password: `testpass123`
3. Click "Login"
4. **Expected Result**: Redirected to homepage, username displayed in navigation

#### Test Case 2.2: Invalid Login

1. Navigate to http://127.0.0.1:8000/accounts/login/
2. Enter invalid credentials:
   - Username: `wronguser`
   - Password: `wrongpass`
3. Click "Login"
4. **Expected Result**: Error message displayed, remains on login page

#### Test Case 2.3: Empty Fields

1. Try to login with empty username or password
2. **Expected Result**: Validation errors displayed

### 3. User Logout Testing

#### Test Case 3.1: Successful Logout

1. While logged in, click on username in navigation
2. Select "Logout"
3. **Expected Result**: Redirected to homepage, login/register links visible

### 4. Profile Management Testing

#### Test Case 4.1: View Profile

1. Login as a user
2. Click on username in navigation
3. Select "Profile"
4. **Expected Result**: Profile page displays user information

#### Test Case 4.2: Edit Profile

1. Navigate to profile page
2. Click "Edit Profile"
3. Update information:
   - Bio: "This is my bio"
   - Location: "New York"
   - Website: "https://example.com"
   - Birth Date: "1990-01-01"
4. Click "Save Changes"
5. **Expected Result**: Success message, updated information displayed

#### Test Case 4.3: Upload Profile Picture

1. Go to profile edit page
2. Select an image file for profile picture
3. Click "Save Changes"
4. **Expected Result**: Profile picture displayed on profile page

#### Test Case 4.4: Update User Information

1. Go to profile edit page
2. Update username, first name, last name, email
3. Click "Save Changes"
4. **Expected Result**: Updated information reflected in profile

### 5. Blog Functionality Testing

#### Test Case 5.1: Create Post (Authenticated)

1. Login as a user
2. Click "Create Post" in navigation
3. Fill out post form:
   - Title: "My First Post"
   - Content: "This is the content of my first post."
4. Click "Publish Post"
5. **Expected Result**: Success message, post appears on homepage

#### Test Case 5.2: Create Post (Unauthenticated)

1. Logout from the system
2. Try to access http://127.0.0.1:8000/create/
3. **Expected Result**: Redirected to login page

#### Test Case 5.3: View Post Detail

1. Click on a post title or "Read More" button
2. **Expected Result**: Full post content displayed with author information

#### Test Case 5.4: Add Comment (Authenticated)

1. View a post detail page
2. Scroll to comments section
3. Enter comment text
4. Click "Post Comment"
5. **Expected Result**: Comment appears in comments section

#### Test Case 5.5: Add Comment (Unauthenticated)

1. Logout from the system
2. Try to add a comment
3. **Expected Result**: Message to login first

### 6. Navigation Testing

#### Test Case 6.1: Authenticated User Navigation

1. Login as a user
2. **Expected Result**: Navigation shows:
   - Home
   - Create Post
   - Username dropdown with Profile, Edit Profile, Logout

#### Test Case 6.2: Unauthenticated User Navigation

1. Logout from the system
2. **Expected Result**: Navigation shows:
   - Home
   - Login
   - Register

### 7. Security Testing

#### Test Case 7.1: CSRF Protection

1. Try to submit forms without CSRF tokens
2. **Expected Result**: CSRF validation errors

#### Test Case 7.2: Protected Views

1. Try to access protected URLs without authentication:
   - /create/
   - /accounts/profile/
   - /accounts/profile/edit/
2. **Expected Result**: Redirected to login page

#### Test Case 7.3: Password Security

1. Try to register with weak passwords:
   - "123"
   - "password"
   - "admin"
2. **Expected Result**: Password validation errors

### 8. Responsive Design Testing

#### Test Case 8.1: Mobile View

1. Resize browser window to mobile size
2. **Expected Result**: Navigation collapses, content remains readable

#### Test Case 8.2: Tablet View

1. Resize browser window to tablet size
2. **Expected Result**: Layout adapts appropriately

### 9. Admin Interface Testing

#### Test Case 9.1: Admin Access

1. Navigate to http://127.0.0.1:8000/admin/
2. Login with superuser credentials
3. **Expected Result**: Admin dashboard accessible

#### Test Case 9.2: User Management

1. In admin, go to Users section
2. **Expected Result**: Can view and edit users

#### Test Case 9.3: Profile Management

1. In admin, go to User profiles section
2. **Expected Result**: Can view and edit user profiles

#### Test Case 9.4: Post Management

1. In admin, go to Posts section
2. **Expected Result**: Can view, edit, and delete posts

## Automated Testing

### Running Django Tests

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test accounts
python manage.py test blog

# Run with verbose output
python manage.py test --verbosity=2
```

### Test Coverage

The project includes basic test files for both apps:

- `accounts/tests.py`
- `blog/tests.py`

## Performance Testing

### Load Testing

1. Create multiple test users
2. Create multiple posts and comments
3. Test page load times
4. Monitor database queries

### File Upload Testing

1. Test profile picture uploads
2. Test with different file types
3. Test with large files
4. Verify file storage and serving

## Browser Compatibility Testing

Test the application in:

- Chrome
- Firefox
- Safari
- Edge
- Mobile browsers

## Error Handling Testing

### Test Case: Invalid URLs

1. Try to access non-existent URLs
2. **Expected Result**: 404 error page

### Test Case: Server Errors

1. Test with invalid data that might cause server errors
2. **Expected Result**: Proper error handling

## Data Validation Testing

### Test Case: Form Validation

1. Submit forms with invalid data
2. Test all form fields
3. **Expected Result**: Appropriate validation messages

### Test Case: Database Constraints

1. Test unique constraints (username, email)
2. Test foreign key relationships
3. **Expected Result**: Proper constraint enforcement

## Security Testing Checklist

- [ ] CSRF tokens present in all forms
- [ ] Password hashing working correctly
- [ ] File upload security
- [ ] Authentication required for protected views
- [ ] Proper session management
- [ ] No sensitive data in URLs
- [ ] Secure cookie settings

## Troubleshooting Common Issues

### Issue: Templates not found

**Solution**: Check TEMPLATES setting in settings.py

### Issue: Static files not loading

**Solution**: Check STATIC_URL and STATICFILES_DIRS settings

### Issue: Media files not serving

**Solution**: Check MEDIA_URL and MEDIA_ROOT settings, and URL patterns

### Issue: Authentication not working

**Solution**: Check LOGIN_URL and LOGIN_REDIRECT_URL settings

### Issue: Database errors

**Solution**: Run migrations and check database configuration

## Test Data Setup

### Create Test Users

```python
# In Django shell
from django.contrib.auth.models import User
from accounts.models import UserProfile

# Create test users
user1 = User.objects.create_user('user1', 'user1@example.com', 'pass123')
user2 = User.objects.create_user('user2', 'user2@example.com', 'pass123')

# Create profiles
UserProfile.objects.create(user=user1, bio='Test bio 1')
UserProfile.objects.create(user=user2, bio='Test bio 2')
```

### Create Test Posts

```python
# In Django shell
from blog.models import Post

# Create test posts
Post.objects.create(title='Test Post 1', content='Content 1', author=user1)
Post.objects.create(title='Test Post 2', content='Content 2', author=user2)
```

## Conclusion

This testing guide covers all major functionality of the Django blog authentication system. Follow these test cases to ensure the system is working correctly and securely. Regular testing helps maintain system reliability and user satisfaction.
