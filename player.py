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
        return int(self.mpv.volume or 60)
    
    def get_status(self) -> dict:
        #
        return {
            "paused": self.mpv.pause,
            "time_pos": self.mpv.time_pos or 0,
            "duration": self.mpv.duration or 0,
            "volume": self.get_vol(),
            #"eof_reached": self.mpv.eof_reached,
            # mpv's eof handles inconstently due to resetting state on state shift/new track
            # another option is check time_pos == duration
        }

    # to jump +/- 5s
    def seek(self, offset: float):
        curr = self.mpv.time_pos or 0
        dur = self.mpv.duration or 0
        if dur > 0:
            new_pos = max(0, min(dur, curr+offset))
            self.mpv.time_pos = new_pos
    
    def terminate(self):
        self.mpv.terminate()
