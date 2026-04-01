"""Bollywood DancePro - Core Views."""
import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import (
    Song, Choreography, LearningModule, UserProfile, MonthlyPerformance,
    CommunityForum, Subscription
)
from .video_embed import embed_kind, embed_src


def home(request):
    """Landing page with featured content."""
    featured_songs = Song.objects.all()[:6]
    featured_choreographies = Choreography.objects.select_related('creator', 'song')[:6]
    upcoming_performances = MonthlyPerformance.objects.filter(
        is_completed=False
    ).order_by('scheduled_at')[:3]

    context = {
        'featured_songs': featured_songs,
        'featured_choreographies': featured_choreographies,
        'upcoming_performances': upcoming_performances,
    }
    return render(request, 'core/home.html', context)


def song_library(request):
    """Browse the song library."""
    songs = Song.objects.all().order_by('-created_at')[:24]
    return render(request, 'core/song_library.html', {'songs': songs})


def choreography_list(request):
    """Browse choreographies."""
    choreographies = Choreography.objects.select_related('creator', 'song').all().order_by('-created_at')[:24]
    return render(request, 'core/choreography_list.html', {'choreographies': choreographies})


def choreography_detail(request, pk):
    """View choreography details and learning module."""
    choreography = get_object_or_404(Choreography.objects.select_related('creator', 'song'), pk=pk)
    learning_module = getattr(choreography, 'learning_module', None)
    steps = list(learning_module.steps.all() if learning_module else [])

    main_media = {'kind': 'none', 'src': None, 'label': ''}
    if choreography.video:
        main_media = {'kind': 'video_file', 'src': choreography.video.url, 'label': 'Choreography video'}
    elif choreography.video_url:
        src, kind = embed_kind(choreography.video_url)
        if kind != 'none':
            main_media = {'kind': kind, 'src': src, 'label': 'Performance video'}
    elif learning_module and learning_module.ai_avatar_video:
        src, kind = embed_kind(learning_module.ai_avatar_video)
        if kind != 'none':
            main_media = {'kind': kind, 'src': src, 'label': 'AI tutorial'}
    elif choreography.song.youtube_url:
        src = embed_src(choreography.song.youtube_url)
        if src:
            main_media = {'kind': 'iframe', 'src': src, 'label': 'Song reference'}

    steps_data = []
    for s in steps:
        entry = {
            'id': s.id,
            'step_number': s.step_number,
            'title': s.title,
            'description': s.description or '',
            'kind': 'none',
            'src': None,
        }
        if s.video_clip_url:
            src, kind = embed_kind(s.video_clip_url)
            entry['kind'] = kind
            entry['src'] = src
        steps_data.append(entry)

    context = {
        'choreography': choreography,
        'learning_module': learning_module,
        'steps': steps,
        'main_media': main_media,
        'main_media_json': json.dumps(main_media),
        'steps_json': json.dumps(steps_data),
    }
    return render(request, 'core/choreography_detail.html', context)


def community_forum(request):
    """Community forum listing."""
    posts = CommunityForum.objects.select_related('creator').all().order_by('-is_pinned', '-created_at')[:20]
    return render(request, 'core/community_forum.html', {'posts': posts})


def performance_schedule(request):
    """Monthly performance schedule."""
    performances = MonthlyPerformance.objects.all().order_by('-scheduled_at')
    return render(request, 'core/performance_schedule.html', {'performances': performances})


def pricing(request):
    """Subscription pricing page."""
    return render(request, 'core/pricing.html')


def about(request):
    """About Bollywood DancePro."""
    return render(request, 'core/about.html')


def register_view(request):
    """User registration."""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user, level='beginner')
            login(request, user)
            messages.success(request, 'Welcome to Bollywood DancePro!')
            return redirect('home')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = UserCreationForm()

    return render(request, 'core/register.html', {'form': form})


def login_view(request):
    """User login."""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            next_url = request.GET.get('next', 'dashboard')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()

    return render(request, 'core/login.html', {'form': form})


def logout_view(request):
    """User logout."""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


@login_required
def dashboard(request):
    """User dashboard based on level."""
    profile, _ = UserProfile.objects.get_or_create(user=request.user, defaults={'level': 'beginner'})
    subscription = getattr(request.user, 'subscription', None)
    has_access = subscription and subscription.has_access if subscription else False

    # Get user's progress
    from .models import UserProgress
    progress = UserProgress.objects.filter(user=request.user).select_related('module__choreography')[:5]

    # Get recommended choreographies
    choreographies = Choreography.objects.filter(
        difficulty=profile.level
    ).select_related('creator', 'song')[:6]

    context = {
        'profile': profile,
        'subscription': subscription,
        'has_access': has_access,
        'progress': progress,
        'choreographies': choreographies,
    }
    return render(request, 'core/dashboard.html', context)
