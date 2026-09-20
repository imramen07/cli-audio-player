# handles libmpv
import mpv

class AudioPlayer:
    def __init__(self):
        # no video self init
        self.mpv = mpv.MPV(
            ytdl = False,
            audio_display = "no",
            audio_fallback_to_null = "no",
        )
        self.current_track = None

    def play(self, trackpath: str):
        self.current_track = trackpath
        self.mpv.play(trackpath)
    
    def pause(self):
        self.mpv.pause = not self.mpv.pause
    
    def stop(self):
        self.mpv.stop()
    
    def set_vol(self, val: int):
        self.mpv.volume = max(0, min(100, val))

    def get_vol(self) -> int:
        return int(self.mpv.volume or 100)
    
    def get_status(self) -> dict:
        return {
            "paused": self.mpv.pause,
            "time_pos": self.mpv.time_pos or 0,
            "duration": self.mpv.duration or 0,
            "volume": self.get_vol(),
        }
    
    def terminate(self):
        self.mpv.terminate()