from django.test import SimpleTestCase, TestCase, Client
from django.contrib.auth.models import User

from .video_embed import embed_kind, embed_src, youtube_video_id
from .models import Song, Choreography


class VideoEmbedTests(SimpleTestCase):
    def test_youtube_id_and_embed(self):
        self.assertEqual(
            youtube_video_id('https://www.youtube.com/watch?v=dQw4w9WgXcQ'),
            'dQw4w9WgXcQ',
        )
        self.assertIn('youtube.com/embed', embed_src('https://youtu.be/dQw4w9WgXcQ'))
        src, kind = embed_kind('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
        self.assertEqual(kind, 'iframe')
        self.assertIn('embed', src)

    def test_raw_mp4(self):
        src, kind = embed_kind('https://example.com/clip.mp4')
        self.assertEqual(kind, 'video_file')
        self.assertEqual(src, 'https://example.com/clip.mp4')


class ChoreographyDetailViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('t_dancer', password='test-pass-123')
        self.song = Song.objects.create(title='Test Song', artist='Artist', youtube_url='https://www.youtube.com/watch?v=dQw4w9WgXcQ')
        self.choreo = Choreography.objects.create(
            title='Test Dance',
            song=self.song,
            creator=self.user,
        )

    def test_detail_ok(self):
        r = self.client.get(f'/choreographies/{self.choreo.pk}/')
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Test Dance')
