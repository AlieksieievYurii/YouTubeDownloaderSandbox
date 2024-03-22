import re


YT_LINK_RE = re.compile(r"https:\/\/www\.youtube\.com\/watch\?v=(\S+)")


def extract_video_id(url: str) -> str:
    """Extract video ID from YouTube URL"""
    res = YT_LINK_RE.match(url)
    if not res:
        raise RuntimeError("Can't parse YouTube vide URL")
    return res.group(1)
