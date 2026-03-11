"""Seed sample data for Bollywood DancePro."""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import (
    UserProfile, Song, Choreography, LearningModule, ModuleStep,
    MonthlyPerformance, CommunityForum
)
from django.utils import timezone
from datetime import timedelta


class Command(BaseCommand):
    help = 'Seed sample data for development'

    def handle(self, *args, **options):
        # Create demo user if not exists
        user, _ = User.objects.get_or_create(
            username='demo',
            defaults={'email': 'demo@dancepro.com'}
        )
        user.set_password('demo123')
        user.save()

        profile, _ = UserProfile.objects.get_or_create(user=user, defaults={'level': 'beginner'})

        # Create sample songs
        songs_data = [
            {'title': 'Jai Ho', 'artist': 'A.R. Rahman', 'movie': 'Slumdog Millionaire'},
            {'title': 'Tum Hi Ho', 'artist': 'Arijit Singh', 'movie': 'Aashiqui 2'},
            {'title': 'Kesariya', 'artist': 'Arijit Singh', 'movie': 'Brahmastra'},
            {'title': 'Raatan Lambiyan', 'artist': 'Jubin Nautiyal', 'movie': 'Shershaah'},
            {'title': 'Channa Mereya', 'artist': 'Arijit Singh', 'movie': 'Ae Dil Hai Mushkil'},
            {'title': 'Raabta', 'artist': 'Arijit Singh', 'movie': 'Agent Vinod'},
        ]
        songs = []
        for data in songs_data:
            song, _ = Song.objects.get_or_create(title=data['title'], defaults=data)
            songs.append(song)

        # Create sample choreographies
        for i, song in enumerate(songs[:4]):
            choreo, _ = Choreography.objects.get_or_create(
                title=f"{song.title} Choreography",
                song=song,
                creator=user,
                defaults={
                    'description': f'Learn to dance to {song.title} with this step-by-step guide.',
                    'difficulty': ['beginner', 'intermediate', 'advanced', 'beginner'][i],
                    'is_ai_processed': i < 2,
                }
            )
            if choreo.is_ai_processed and not hasattr(choreo, 'learning_module'):
                module = LearningModule.objects.create(
                    choreography=choreo,
                    step_count=5,
                    transcript='Step by step tutorial...'
                )
                for j in range(1, 6):
                    ModuleStep.objects.get_or_create(
                        module=module,
                        step_number=j,
                        defaults={
                            'title': f'Step {j}',
                            'description': f'Learn the {j}th move in this sequence.',
                            'duration_seconds': 30,
                        }
                    )

        # Create upcoming performance
        next_month = timezone.now() + timedelta(days=30)
        MonthlyPerformance.objects.get_or_create(
            title='April Community Showcase',
            defaults={
                'description': 'Join us for our monthly virtual performance!',
                'scheduled_at': next_month.replace(day=15, hour=19, minute=0, second=0),
                'max_participants': 50,
            }
        )

        # Create forum post
        CommunityForum.objects.get_or_create(
            title='Welcome to Bollywood DancePro!',
            creator=user,
            defaults={
                'description': 'Introduce yourself and share your dance journey with the community.',
                'is_pinned': True,
            }
        )

        self.stdout.write(self.style.SUCCESS('Sample data seeded! Login with demo/demo123'))
