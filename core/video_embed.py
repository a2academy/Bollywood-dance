"""Resolve common video URLs to iframe embed sources."""
import re
from typing import Optional, Tuple


def youtube_video_id(url: str) -> Optional[str]:
    if not url or not isinstance(url, str):
        return None
    url = url.strip()
    patterns = [
        r'(?:youtube\.com/watch\?v=)([A-Za-z0-9_-]{11})',
        r'(?:youtu\.be/)([A-Za-z0-9_-]{11})',
        r'(?:youtube\.com/embed/)([A-Za-z0-9_-]{11})',
        r'(?:youtube\.com/shorts/)([A-Za-z0-9_-]{11})',
    ]
    for p in patterns:
        m = re.search(p, url)
        if m:
            return m.group(1)
    return None


def vimeo_video_id(url: str) -> Optional[str]:
    if not url or not isinstance(url, str):
        return None
    m = re.search(r'vimeo\.com/(?:video/)?(\d+)', url.strip())
    return m.group(1) if m else None


def embed_src(url: str) -> Optional[str]:
    """Return https URL suitable for iframe src, or None."""
    if not url or not isinstance(url, str):
        return None
    url = url.strip()
    yid = youtube_video_id(url)
    if yid:
        return f'https://www.youtube.com/embed/{yid}'
    vid = vimeo_video_id(url)
    if vid:
        return f'https://player.vimeo.com/video/{vid}'
    return None


def embed_kind(url: str) -> Tuple[Optional[str], str]:
    """
    Returns (src, kind): kind is 'iframe', 'video_file', 'link', or 'none'.
    """
    if not url:
        return None, 'none'
    url = url.strip()
    lower = url.lower().split('?')[0]
    if lower.endswith(('.mp4', '.webm', '.ogg', '.mov')):
        return url, 'video_file'
    src = embed_src(url)
    if src:
        return src, 'iframe'
    if url.startswith('http'):
        return url, 'link'
    return None, 'none'
