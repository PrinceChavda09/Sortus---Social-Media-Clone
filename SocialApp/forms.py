from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile, Post, Comment

# --- Auth Forms ---

class RegisterForm(UserCreationForm):
    """
    A form for creating new users. Includes email and password confirmation.
    """
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "first_name", "last_name")

class LoginForm(AuthenticationForm):
    """
    Standard login form.
    """
    pass


# --- Profile and User Editing Forms ---

class UserEditForm(forms.ModelForm):
    """
    A form for updating the user's first name, last name, and email.
    """
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileForm(forms.ModelForm):
    """
    A form for updating the user's profile (bio, profile pic, cover photo).
    """
    class Meta:
        model = Profile
        fields = ['bio', 'profile_pic']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Tell us about yourself...'}),
        }


# --- Content Forms ---

class PostForm(forms.ModelForm):
    """
    A form for creating a new post.
    """
    class Meta:
        model = Post
        fields = ['content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': "What's on your mind?"}),
        }

class CommentForm(forms.ModelForm):
    """
    A form for adding a comment to a post.
    """
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.TextInput(attrs={'placeholder': 'Add a comment...', 'class': 'form-control form-control-sm'})
        }

