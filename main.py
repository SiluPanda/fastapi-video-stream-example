from fastapi import (
    FastAPI,
    Header,
    Response
)
from pathlib import Path


app = FastAPI()

CHUNK_SIZE = 1024*1024
video_path = Path("video.mp4")



@app.get('/video')
def stream_video(range: str=Header(None)):
    if range:
        start, end = range.replace("bytes=", "").split("-")
    else:
        start = 0
        end = video_path.stat().st_size - 1
    start = int(start)
    end = int(end) if end else start + CHUNK_SIZE
    end = min(end, video_path.stat().st_size - 1)
    with open(video_path, "rb") as video:
        video.seek(start)
        data = video.read(end - start + 1)
        filesize = str(video_path.stat().st_size)
        headers = {
            'Content-Range': f'bytes {str(start)}-{str(end)}/{filesize}',
            'Accept-Ranges': 'bytes',
            'Content-Length': str(end - start + 1),
            'Content-Type': 'video/mp4',
        }
        return Response(data, status_code=206, headers=headers, media_type="video/mp4")
