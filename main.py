import sys
import time
from lib import scan_dir
from player import AudioPlayer
import readchar
from interface import render_ui
import queue
import threading
from rich.live import Live
from rich.console import Console

inpq = queue.Queue()

def input_listener():
    while True:
        try:
            key = readchar.readkey()
            inpq.put(key)
            if key == "q":
                break
        except Exception:
            break

def main():
    if len(sys.argv) < 2:
        print("usage: python main.py /path/to/file")
        sys.exit(1)
    
    main_dir = sys.argv[1]
    tracks = scan_dir(main_dir)

    if not tracks:
        print(f"No compatible fies found in {main_dir}")
        sys.exit(1)
    
    player = AudioPlayer()
    selected_index = 0
    playing_index = -1
    # last_played_index to track song transitions
    last_played_index = -1 

    #player.play(tracks[current_index].filepath)
    # start non blocking input thread
    key_thread = threading.Thread(
        target = input_listener,
        daemon = True
    )
    key_thread.start()

    con = Console()

    try:
        '''
        render with ms sleep
        update using rich
        self causing flashes and inconsistency in scrolling
        no such issues in rich
        '''
        with Live(render_ui(tracks, selected_index, playing_index, player.get_status()), console = con, refresh_per_second = 20) as live:
            while True:
                #status = player.get_status()
                #render_ui(tracks, selected_index, playing_index, status)
                #TODO: Slide and update using arrows
                #TODO: 5s inc/dec using < >

                #key = readchar.readkey()
                while not inpq.empty():
                    key = inpq.get()

                    if key == "q":
                        break
                    elif key in ("j", readchar.key.DOWN):
                        selected_index = (selected_index+1) % len(tracks)
                        #player.play(tracks[current_index].filepath)
                    elif key in ("k", readchar.key.UP):
                        selected_index = (selected_index-1) % len(tracks)
                        #player.play(tracks[current_index].filepath)
                    elif key in ("\r", "\n", readchar.key.ENTER):
                        playing_index = selected_index
                        player.play(tracks[playing_index].filepath)
                    elif key in (" ", "p"):
                        player.pause()
                    elif key in ("+", "="):
                        player.set_vol(player.get_vol() + 5)
                    elif key in ("-", "_"):
                        player.set_vol(player.get_vol() - 5)
                    elif key in (readchar.key.LEFT):
                        player.seek(-5)
                    elif key in (readchar.key.RIGHT):
                        player.seek(5)



                    #time.sleep(0.05)
                status = player.get_status()

                '''
                # failed approach 1
                # play next track if eof, stop playback if last
                if playing_index != -1 and status.get("eof_reached"):
                    if playing_index < len(tracks)-1:
                        player.play(tracks[++playing_index].filepath)
                    else:
                        playing_index = -1
                        player.stop()
                '''
                # approach 2
                if playing_index != -1 and playing_index == last_played_index:
                    dur = status.get("duration", 0)
                    pos = status.get("time_pos", 0)

                    # check eof manuually
                    if dur > 0 and pos >= dur - 0.5 and not status.get("paused"):
                        if playing_index < len(tracks)-1:
                            playing_index = playing_index+1
                            last_played_index = playing_index
                            player.play(tracks[playing_index].filepath)
                        else:
                            playing_index = -1
                            last_played_index = -1
                            player.stop()
                # update tracking mech if track is manually selected by user
                if playing_index != last_played_index:
                    last_played_index = playing_index

                live.update(render_ui(tracks, selected_index, playing_index, status))
                '''
                sleep -> cpu usage
                0.50 -> 0.1x
                0.40
                0.35
                0.30
                0.25
                0.20
                0.15
                0.10 -> 0.4x <- Win11
                0.05
                0.09
                0.08
                0.07 -> ~1.3 <- Arch GNOME
                0.06
                0.04 -> ~1.9
                0.03 -> ~2.0 <- Arch Hyprland
                0.02 -> 2.x
                0.01 -> xx
                '''
                time.sleep(0.02)
            
    finally:
        player.terminate()
        print("\nexited player")
    
if __name__ == "__main__":
    main()
