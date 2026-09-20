# dir scanner
import os
from pathlib import Path
from tinytag import TinyTag

EXT = {".flac", ".mp3", ".wav"}

class Track:
    # init -> load metadata -> scan dir
    def __init__(self, filepath: Path):
        self.filepath = str(filepath)
        self.filename = filepath.name
        self.title = filepath.stem
        self.artist = "Unknown"
        self.duration = 0.0
        self._load_metadata()
    
    def _load_metadata(self):
        # TODO: pass for empty metadata
        # better option is always viable
        try:
            tags = TinyTag.get(self.filepath)
            if tags.title:
                self.title = tags.title
            if tags.artist:
                self.artist = tags.artist
            if tags.duration:
                self.duration = tags.duration
        except Exception as e:
            print(f"ER load metadata : {e}")

def scan_dir(dirpath: str) -> list[Track]:
    tracks = []
    path = Path(dirpath).expanduser()
    # TODO: path not found log
    if not path.exists():
        return tracks
    
    for file in path.rglob("*"):
        if file.suffix.lower() in EXT:
            tracks.append(Track(file))
        
    return sorted(tracks, key = lambda t: t.title.lower())