import os  # os module for file deletion
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import RegistrationForm, LoginForm, ProfileUpdateForm, PostCreateForm
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.db.models import Q  # Allows complex queries like case-insensitive search
User = get_user_model()  # Reference to the custom user model

# Home page view for login
def home(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)  # If it's a POST request, validate login form
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user_obj = authenticate(request, username=username, password=password)  # Authenticate user
            if user_obj is not None:  # If authentication is successful
                login(request, user_obj)  # Log the user in
                return redirect('User_Profile')  # Redirect to the Users Profile page after successful login
            else:
                form.add_error(None, "Invalid login credentials.")  # If credentials are incorrect
    else:
        form = LoginForm()  # If it's a GET request, show the login form

    return render(request, 'welcome.html', {'form': form})  # Render the login form

# Registration view
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)  # Create the registration form
        if form.is_valid():
            form.save()  # Save the new user if the form is valid
            return redirect('home')  # Redirect to the home page (login) after successful registration
    else:
        form = RegistrationForm()  # If GET request, show the registration form
    return render(request, 'register.html', {'form': form})  # Render the registration form

# User Profile view
def User_Profile(request):
    if request.user.is_authenticated:  # Check if the user is logged in
        if request.method == 'POST':
            form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)  # Handle form submission for profile update
            if form.is_valid():
                form.save()  # Save the updated profile
                return redirect('User_Profile')  # Redirect to the same page to see updated profile
        else:
            form = ProfileUpdateForm(instance=request.user)  # Pre-fill the form with the current user's data

        posts = request.user.post_set.all()  # Get all posts made by the logged-in user
        return render(request, 'User_Profile.html', {'form': form, 'posts': posts})  # Render the profile page with the form and posts
    else:
        return redirect('home')  # Redirect to login page if user is not logged in



@login_required
def edit_profile(request):
    if request.method == 'POST':
        # Check if the 'delete_picture' flag is in the POST data
        if request.POST.get('delete_picture') == 'true':
            # Get the user's profile picture path
            if request.user.profile_picture:
                # Get the file path
                file_path = request.user.profile_picture.path
                # Delete the file from the filesystem
                if os.path.exists(file_path):
                    os.remove(file_path)
                # Set the profile_picture field to None
                request.user.profile_picture = None
                request.user.save()

        # Handle form submission for profile updates
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            if request.htmx:
                return render(request, 'profile_update.html', {'user': request.user})
            else:
                return redirect('User_Profile')

    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, 'User_Profile.html', {'form': form})

def user_logout(request):
    logout(request) # Ends the user session
    return redirect('home')  # Redirect to login or home page

@login_required
def create_post(request):
    if request.method == "POST":
        form = PostCreateForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            # After saving the post
            return redirect('User_Profile')
    else:
        form = PostCreateForm()
    return render(request, "create_post.html", {"form": form})

# Delete a post by ID (only if it belongs to the logged-in user)
@login_required
def delete_post(request, post_id):
    # Only fetch the post if it belongs to the logged-in user
    post = get_object_or_404(request.user.post_set, id=post_id)
    if request.method == "POST":
        post.delete()
        messages.success(request, "Post deleted.")
        return redirect('User_Profile')
    return HttpResponse("Invalid request", status=400)

# View for the user feed/search page
def Feed(request):
    query = request.GET.get('q', '')  # Get the search query from the URL parameters (e.g., ?q=someuser)

    # If there's a query, filter users whose usernames contain the query (case-insensitive)
    # Otherwise, return an empty list (don't show users by default)
    users = User.objects.filter(Q(username__icontains=query)) if query else []

    # Render the feed page, passing the search results and the current query (to display in input)
    return render(request, 'Feed.html', {'users': users, 'query': query})

# View for displaying another user's public profile
def other_user_profile(request, username):
    user = get_object_or_404(User, username=username)  # Look up user by username
    posts = user.post_set.all()  # Get user's posts (adjust if you renamed related_name)
    return render(request, 'OtherUserProfile.html', {'user_profile': user, 'posts': posts})