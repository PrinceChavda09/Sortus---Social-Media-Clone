from django.urls import path
from . import views

app_name = 'SocialApp'

urlpatterns = [
    # Auth
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Core Feed & Post
    path('', views.feed_view, name='feed_view'),
    path('post/create/', views.create_post_view, name='create_post'),
    path('post/<int:post_id>/', views.post_detail_view, name='post_detail'),
    path('post/<int:post_id>/edit/', views.edit_post_view, name='edit_post'),
    path('post/<int:post_id>/delete/', views.delete_post_view, name='delete_post'),

    # ================================================================
    # THIS IS THE FIX: Specific profile URLs now come BEFORE the
    # general <username> URL.
    # ================================================================
    path('profile/edit/', views.edit_profile_view, name='edit_profile_view'),
    path('profile/delete/', views.delete_profile_view, name='delete_profile'),
    
    # This general pattern MUST be last.
    path('profile/<str:username>/', views.profile_view, name='profile'),

    # Actions
    path('post/<int:post_id>/like/', views.like_post_view, name='like_post'),
    path('post/<int:post_id>/comment/', views.add_comment_view, name='add_comment'),
    path('profile/<str:username>/follow/', views.follow_toggle_view, name='follow_toggle'),
]

