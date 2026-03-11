"""
Bollywood DancePro - Core Models
User profiles, songs, choreographies, learning modules, and subscriptions.
"""
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserProfile(models.Model):
    """Extended user profile with dance level and preferences."""
    USER_LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('advanced', 'Advanced'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    level = models.CharField(max_length=20, choices=USER_LEVEL_CHOICES, default='beginner')
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    dance_goals = models.TextField(blank=True, help_text="User's dance learning goals")
    favorite_songs = models.ManyToManyField('Song', blank=True, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} ({self.get_level_display()})"


class Song(models.Model):
    """Bollywood song in the library."""
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255, blank=True)
    movie = models.CharField(max_length=255, blank=True)
    year = models.PositiveIntegerField(null=True, blank=True)
    youtube_url = models.URLField(blank=True)
    thumbnail = models.ImageField(upload_to='song_thumbnails/', blank=True, null=True)
    duration_seconds = models.PositiveIntegerField(null=True, blank=True)
    is_user_requested = models.BooleanField(default=False)
    requested_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='requested_songs')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.artist}"


class Choreography(models.Model):
    """Dance choreography uploaded by advanced dancers."""
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='choreographies')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='choreographies')
    video = models.FileField(upload_to='choreography_videos/', blank=True, null=True)
    video_url = models.URLField(blank=True, help_text="External video URL")
    thumbnail = models.ImageField(upload_to='choreography_thumbnails/', blank=True, null=True)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    duration_seconds = models.PositiveIntegerField(null=True, blank=True)
    is_ai_processed = models.BooleanField(default=False, help_text="Converted to step-by-step tutorial")
    view_count = models.PositiveIntegerField(default=0)
    like_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Choreographies'

    def __str__(self):
        return f"{self.title} by {self.creator.username}"


class LearningModule(models.Model):
    """AI-generated step-by-step tutorial from choreography."""
    choreography = models.OneToOneField(Choreography, on_delete=models.CASCADE, related_name='learning_module')
    step_count = models.PositiveIntegerField(default=0)
    ai_avatar_video = models.URLField(blank=True, help_text="AI avatar tutorial video")
    transcript = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Tutorial: {self.choreography.title}"


class ModuleStep(models.Model):
    """Individual step within a learning module."""
    module = models.ForeignKey(LearningModule, on_delete=models.CASCADE, related_name='steps')
    step_number = models.PositiveIntegerField()
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    video_clip_url = models.URLField(blank=True)
    duration_seconds = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['step_number']
        unique_together = ['module', 'step_number']

    def __str__(self):
        return f"Step {self.step_number}: {self.title}"


class UserProgress(models.Model):
    """Track user progress through learning modules."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dance_progress')
    module = models.ForeignKey(LearningModule, on_delete=models.CASCADE, related_name='user_progress')
    current_step = models.PositiveIntegerField(default=1)
    completed_steps = models.JSONField(default=list, help_text="List of completed step numbers")
    completed = models.BooleanField(default=False)
    last_practiced = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'module']
        verbose_name_plural = 'User progress'

    def __str__(self):
        return f"{self.user.username} - {self.module.choreography.title}"


class SongRequest(models.Model):
    """User-requested songs for the library."""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('added', 'Added'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='song_requests_made')
    song_name = models.CharField(max_length=255)
    artist = models.CharField(max_length=255, blank=True)
    youtube_url = models.URLField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_song = models.ForeignKey(Song, on_delete=models.SET_NULL, null=True, blank=True, related_name='request')
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.song_name} (by {self.user.username})"


class MonthlyPerformance(models.Model):
    """Scheduled monthly virtual community performances."""
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    scheduled_at = models.DateTimeField()
    meeting_url = models.URLField(blank=True)
    max_participants = models.PositiveIntegerField(default=50)
    song_selections = models.ManyToManyField(Song, blank=True, related_name='performances')
    participants = models.ManyToManyField(User, blank=True, related_name='performances_joined')
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-scheduled_at']

    def __str__(self):
        return f"{self.title} - {self.scheduled_at.strftime('%B %Y')}"


class Subscription(models.Model):
    """Monthly subscription for premium access."""
    PLAN_CHOICES = [
        ('monthly', 'Monthly ($9.99)'),
        ('annual', 'Annual (Save 20%)'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='subscription')
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES, default='monthly')
    is_active = models.BooleanField(default=False)
    started_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    stripe_customer_id = models.CharField(max_length=255, blank=True)
    stripe_subscription_id = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_plan_display()} ({'Active' if self.is_active else 'Inactive'})"

    @property
    def has_access(self):
        if not self.is_active:
            return False
        if self.expires_at and self.expires_at < timezone.now():
            return False
        return True


class CommunityForum(models.Model):
    """Community forum for discussions."""
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='forum_posts')
    choreography = models.ForeignKey(Choreography, on_delete=models.SET_NULL, null=True, blank=True, related_name='discussions')
    is_pinned = models.BooleanField(default=False)
    view_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_pinned', '-created_at']

    def __str__(self):
        return self.title


class ForumReply(models.Model):
    """Replies to forum posts."""
    post = models.ForeignKey(CommunityForum, on_delete=models.CASCADE, related_name='replies')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='forum_replies')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']
        verbose_name_plural = 'Forum replies'

    def __str__(self):
        return f"Reply by {self.author.username} on {self.post.title}"
