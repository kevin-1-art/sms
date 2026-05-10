from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from apps.users.forms import LoginForm, PasswordResetForm, SetPasswordForm
from apps.users.models import CustomUser

@require_http_methods(["GET", "POST"])
def login_view(request):
    """User login view."""
    if request.user.is_authenticated:
        return redirect('dashboard:admin_dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                if not user.is_active:
                    messages.error(request, 'This account has been deactivated.')
                else:
                    login(request, user)
                    messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
                    return redirect('dashboard:admin_dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    
    return render(request, 'users/login.html', {'form': form})


@login_required
@require_http_methods(["POST"])
def logout_view(request):
    """User logout view."""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('users:login')


@require_http_methods(["GET", "POST"])
def password_reset_view(request):
    """Password reset request view."""
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = CustomUser.objects.get(email=email)
                # In production, send an email with reset link
                messages.success(request, 'Password reset link has been sent to your email.')
                return redirect('users:login')
            except CustomUser.DoesNotExist:
                messages.error(request, 'No user found with this email.')
    else:
        form = PasswordResetForm()
    
    return render(request, 'users/password_reset.html', {'form': form})


@require_http_methods(["GET", "POST"])
def set_password_view(request):
    """Set new password view (for demo purposes, simplified)."""
    if not request.user.is_authenticated:
        return redirect('users:login')
    
    if request.method == 'POST':
        form = SetPasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['new_password1']
            request.user.set_password(password)
            request.user.save()
            messages.success(request, 'Password has been changed successfully.')
            return redirect('users:login')
    else:
        form = SetPasswordForm()
    
    return render(request, 'users/set_password.html', {'form': form})
