from django.contrib import admin
# --- MODIFIED: Import the default UserAdmin to extend it ---
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile, Post, Comment, Follow

# --- This is the key to customizing the admin ---

# 1. Define an "inline" view for the Profile model.
# This allows you to see and edit the Profile on the User page.
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

# 2. Define a new User admin class that includes the Profile inline.
class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )

    # This is optional: it displays the user's email on the main list view.
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


# --- The Fix: Unregister the default User admin, then re-register with our custom one ---
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# --- Register your other models so you can manage them in the admin panel ---
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'content', 'created_at')
    search_fields = ('content', 'author__username')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'content', 'created_at')
    search_fields = ('content', 'author__username', 'post__content')

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('follower', 'following', 'created_at')

