from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import RegisterForm, LoginForm, ProfileForm, PostForm, CommentForm, UserEditForm
from .models import Profile, Post, Comment, Follow
from django.http import JsonResponse


@login_required
def feed_view(request):
    """
    Displays the main feed with posts from the user and people they follow.
    """
    following_ids = request.user.following.values_list('following_id', flat=True)
    
    user_ids_to_show = list(following_ids) + [request.user.id]

    posts = Post.objects.all().order_by('-created_at')
    
    comment_form = CommentForm()

    context = {
        'posts': posts,
        'comment_form': comment_form
    }
    return render(request, "socialapp/feed.html", context)


@login_required
def post_detail_view(request, post_id):
    """
    Displays a single post and its comments, and handles new comment submissions.
    """
    post = get_object_or_404(Post, id=post_id)
    comment_form = CommentForm()
    
    if request.method == 'POST':
        # This part handles the form submission for adding a new comment
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, "Your comment has been added.")
            return redirect("SocialApp:post_detail", post_id=post.id)

    context = {
        'post': post,
        'comment_form': comment_form
    }
    return render(request, "socialapp/post_detail.html", context)


@login_required
def create_post_view(request):
    """
    Handles the creation of a new post.
    """
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "Your post has been created!")
            return redirect("SocialApp:feed_view")
    else:
        form = PostForm()
    
    return render(request, "socialapp/create_post.html", {"form": form})


@login_required
def profile_view(request, username):
    """
    Displays a user's profile page.
    """
    profile_user = get_object_or_404(User, username=username)
    profile = profile_user.profile
    posts = Post.objects.filter(author=profile_user).order_by("-created_at")

    is_following = request.user.following.filter(following=profile_user).exists()

    context = {
        "profile_user": profile_user,
        "profile": profile,
        "posts": posts,
        "is_following": is_following,
    }
    return render(request, "socialapp/profile.html", context)

@login_required
def edit_profile_view(request):
    """
    Handles editing the user's profile and user details.
    """
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('SocialApp:profile', username=request.user.username)
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'socialapp/edit_profile.html', context)


# @login_required
# def like_post_view(request, post_id):
#     """
#     Toggles a like on a post.
#     """
#     post = get_object_or_404(Post, id=post_id)
#     if post.likes.filter(id=request.user.id).exists():
#         post.likes.remove(request.user)
#     else:
#         post.likes.add(request.user)
#     return redirect(request.META.get('HTTP_REFERER', 'SocialApp:feed_view'))

def like_post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    liked = False
    
    if user.is_authenticated:
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            liked = False
        else:
            post.likes.add(request.user)
            liked = True
    
    # Return a JSON response with the new like count and liked status
    return JsonResponse({
        'likes_count': post.likes.count(),
        'liked': liked
    })


@login_required
def add_comment_view(request, post_id):
    """
    Handles adding a comment to a post.
    """
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, "Comment added.")
    return redirect(request.META.get('HTTP_REFERER', 'SocialApp:feed_view'))


@login_required
def follow_toggle_view(request, username):
    """
    Toggles following a user.
    """
    user_to_toggle = get_object_or_404(User, username=username)
    if request.user == user_to_toggle:
        messages.warning(request, "You cannot follow yourself.")
        return redirect("SocialApp:profile", username=username)

    follow, created = Follow.objects.get_or_create(follower=request.user, following=user_to_toggle)

    if created:
        messages.success(request, f"You are now following {username}.")
    else:
        follow.delete()
        messages.info(request, f"You have unfollowed {username}.")
        
    return redirect("SocialApp:profile", username=username)


def register_view(request):
    """
    Handles new user registration.
    """
    if request.user.is_authenticated:
        return redirect("SocialApp:feed_view")
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! Please log in.")
            return redirect("SocialApp:login")
    else:
        form = RegisterForm()
    return render(request, "socialapp/register.html", {"form": form})


def login_view(request):
    """
    Handles user login.
    """
    if request.user.is_authenticated:
        return redirect("SocialApp:feed_view")
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("SocialApp:feed_view")
    else:
        form = LoginForm()
    return render(request, "socialapp/login.html", {"form": form})


@login_required
def logout_view(request):
    """
    Logs the user out.
    """
    logout(request)
    messages.info(request, "You have been successfully logged out.")
    return redirect("SocialApp:login")


@login_required
def edit_post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('SocialApp:post_detail', post_id=post.id)
    else:
        form = PostForm(instance=post)
        
    return render(request, 'socialapp/edit_post.html', {'form': form, 'post': post})


@login_required
def delete_post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post has been deleted.')
        return redirect('SocialApp:feed_view')
        
    return render(request, 'socialapp/delete_post_confirm.html', {'post': post})

@login_required
def delete_profile_view(request):
    if request.method == 'POST':
        user = request.user
        # Log the user out first to invalidate their session
        logout(request)
        # Delete the user object. All related data will be deleted automatically.
        user.delete()
        messages.success(request, 'Your account has been successfully deleted.')
        return redirect('SocialApp:login') # Redirect to a safe page
    
    return render(request, 'socialapp/delete_profile_confirm.html')
