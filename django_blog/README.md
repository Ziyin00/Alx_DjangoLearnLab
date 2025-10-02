# Django Blog with Authentication System

A comprehensive Django blog application with a complete authentication system, user profile management, and blog functionality.

## Features

### 🔐 Authentication System

- User registration with email, first name, last name
- Secure login/logout functionality
- Password validation and security
- CSRF protection on all forms

### 👤 Profile Management

- Extended user profiles with additional fields
- Profile picture uploads
- Bio, location, website, and birth date fields
- Profile editing interface

### 📝 Blog Functionality

- Create and publish blog posts
- Comment system for posts
- User-specific post creation
- Responsive design with Bootstrap

### 🎨 Modern UI/UX

- Bootstrap 5 styling
- Responsive design
- Font Awesome icons
- Custom CSS for enhanced appearance

## Quick Start

### 1. Installation

```bash
# Clone or navigate to the project directory
cd django_blog

# Install dependencies (if using virtual environment)
pip install django

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

### 2. Access the Application

- **Homepage**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **Login**: http://127.0.0.1:8000/accounts/login/
- **Register**: http://127.0.0.1:8000/accounts/register/

## Project Structure

```
django_blog/
├── accounts/                    # Authentication app
│   ├── models.py               # UserProfile model
│   ├── forms.py                # Custom forms
│   ├── views.py                # Authentication views
│   ├── urls.py                 # Authentication URLs
│   └── admin.py                # Admin configuration
├── blog/                       # Blog app
│   ├── models.py               # Post and Comment models
│   ├── views.py                # Blog views
│   ├── urls.py                 # Blog URLs
│   └── admin.py                # Admin configuration
├── blog_project/               # Main project
│   ├── settings.py             # Django settings
│   └── urls.py                 # Main URL configuration
├── templates/                  # HTML templates
│   ├── base.html               # Base template
│   ├── accounts/               # Authentication templates
│   └── blog/                   # Blog templates
├── static/                     # Static files
│   └── css/
│       └── style.css           # Custom CSS
└── media/                      # User uploads
```

## User Guide

### For New Users

1. **Registration**

   - Click "Register" in the navigation
   - Fill out the registration form
   - Provide username, email, first name, last name, and password
   - Click "Create Account"

2. **Login**

   - Click "Login" in the navigation
   - Enter your username and password
   - Click "Login"

3. **Profile Management**

   - Click on your username in the navigation
   - Select "Profile" to view your profile
   - Select "Edit Profile" to update information
   - Upload a profile picture
   - Add bio, location, website, and birth date

4. **Creating Posts**

   - Click "Create Post" in the navigation
   - Enter post title and content
   - Click "Publish Post"

5. **Interacting with Posts**
   - View posts on the homepage
   - Click "Read More" to view full posts
   - Add comments to posts
   - View author information

### For Administrators

1. **Admin Panel**

   - Access http://127.0.0.1:8000/admin/
   - Login with superuser credentials
   - Manage users, posts, and comments
   - View user profiles and activity

2. **User Management**

   - View all registered users
   - Edit user information
   - Manage user profiles
   - Monitor user activity

3. **Content Management**
   - Moderate blog posts
   - Manage comments
   - Control post publication status

## Technical Details

### Models

#### UserProfile

- One-to-one relationship with User model
- Additional fields: bio, profile_picture, birth_date, location, website

#### Post

- Foreign key to User (author)
- Fields: title, content, created_at, updated_at, published

#### Comment

- Foreign key to Post and User
- Fields: content, created_at

### Forms

#### CustomUserCreationForm

- Extends Django's UserCreationForm
- Includes email, first name, last name
- Automatically creates UserProfile

#### UserProfileForm

- Handles profile information updates
- File upload for profile pictures

#### UserUpdateForm

- Updates user account information

### Security Features

- **CSRF Protection**: All forms include CSRF tokens
- **Password Security**: Django's built-in hashing and validation
- **File Upload Security**: Safe handling of profile pictures
- **Authentication Required**: Protected views require login

### URL Patterns

```
/                           # Homepage
/accounts/login/            # User login
/accounts/logout/           # User logout
/accounts/register/         # User registration
/accounts/profile/          # User profile
/accounts/profile/edit/     # Edit profile
/post/<id>/                # Post detail
/create/                   # Create post (login required)
/admin/                    # Admin panel
```

## Customization

### Adding New Features

1. **New Profile Fields**

   ```python
   # In accounts/models.py
   class UserProfile(models.Model):
       # ... existing fields ...
       new_field = models.CharField(max_length=100, blank=True)
   ```

2. **Custom Styling**

   - Modify `static/css/style.css`
   - Update Bootstrap classes in templates
   - Add custom JavaScript if needed

3. **Additional Authentication**
   - Password reset functionality
   - Email verification
   - Social authentication

### Database Changes

After modifying models:

```bash
python manage.py makemigrations
python manage.py migrate
```

## Troubleshooting

### Common Issues

1. **Server won't start**

   - Check if all dependencies are installed
   - Verify database migrations are applied
   - Check for syntax errors in code

2. **Templates not found**

   - Ensure templates are in correct directory
   - Check TEMPLATES setting in settings.py

3. **Static files not loading**

   - Verify STATIC_URL and STATICFILES_DIRS settings
   - Check if static files are in correct directory

4. **Media files not serving**

   - Ensure MEDIA_URL and MEDIA_ROOT are configured
   - Check URL patterns include media serving

5. **Authentication issues**
   - Verify LOGIN_URL and LOGIN_REDIRECT_URL settings
   - Check if user is properly authenticated
   - Ensure CSRF tokens are included in forms

### Debug Mode

For development, ensure DEBUG = True in settings.py:

```python
DEBUG = True
```

## Production Deployment

### Security Checklist

- [ ] Set DEBUG = False
- [ ] Use environment variables for SECRET_KEY
- [ ] Configure ALLOWED_HOSTS
- [ ] Use HTTPS
- [ ] Set up proper file serving
- [ ] Use production database
- [ ] Configure static file serving

### Performance Optimization

- Use PostgreSQL or MySQL for production
- Configure static file serving with nginx/Apache
- Implement caching
- Use CDN for static files
- Optimize database queries

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues and questions:

1. Check the troubleshooting section
2. Review the documentation
3. Check Django documentation
4. Create an issue in the repository

## Changelog

### Version 1.0.0

- Initial release
- Complete authentication system
- User profile management
- Blog functionality
- Responsive design
- Admin interface
- Comprehensive documentation
