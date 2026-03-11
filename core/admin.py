"""Bollywood DancePro Admin Configuration."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import (
    UserProfile, Song, Choreography, LearningModule, ModuleStep,
    UserProgress, SongRequest, MonthlyPerformance, Subscription,
    CommunityForum, ForumReply
)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'level', 'created_at']
    list_filter = ['level']
    search_fields = ['user__username', 'bio']


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ['title', 'artist', 'movie', 'is_user_requested', 'created_at']
    list_filter = ['is_user_requested']
    search_fields = ['title', 'artist', 'movie']


@admin.register(Choreography)
class ChoreographyAdmin(admin.ModelAdmin):
    list_display = ['title', 'creator', 'song', 'difficulty', 'is_ai_processed', 'created_at']
    list_filter = ['difficulty', 'is_ai_processed']
    search_fields = ['title', 'creator__username']


class ModuleStepInline(admin.TabularInline):
    model = ModuleStep
    extra = 1


@admin.register(LearningModule)
class LearningModuleAdmin(admin.ModelAdmin):
    list_display = ['choreography', 'step_count', 'created_at']
    inlines = [ModuleStepInline]


@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'module', 'current_step', 'completed', 'last_practiced']
    list_filter = ['completed']


@admin.register(SongRequest)
class SongRequestAdmin(admin.ModelAdmin):
    list_display = ['song_name', 'user', 'status', 'created_at']
    list_filter = ['status']


@admin.register(MonthlyPerformance)
class MonthlyPerformanceAdmin(admin.ModelAdmin):
    list_display = ['title', 'scheduled_at', 'is_completed', 'created_at']
    list_filter = ['is_completed']
    filter_horizontal = ['song_selections', 'participants']


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'plan', 'is_active', 'expires_at', 'created_at']
    list_filter = ['plan', 'is_active']


@admin.register(CommunityForum)
class CommunityForumAdmin(admin.ModelAdmin):
    list_display = ['title', 'creator', 'is_pinned', 'view_count', 'created_at']
    list_filter = ['is_pinned']


@admin.register(ForumReply)
class ForumReplyAdmin(admin.ModelAdmin):
    list_display = ['post', 'author', 'created_at']
