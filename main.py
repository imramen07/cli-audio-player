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

    #player.play(tracks[current_index].filepath)
    # start non blocking input thread
    key_thread = threading.Thread(
        target = input_listener,
        daemon = True
    )
    key_thread.start()

    con = Console()

    try:
        with Live(render_ui(tracks, selected_index, playing_index, player.get_status()), console = con, refresh_per_second = 20) as live:
            while True:
                #status = player.get_status()
                #render_ui(tracks, selected_index, playing_index, status)

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
            
                    #time.sleep(0.05)
                status = player.get_status()
                live.update(render_ui(tracks, selected_index, playing_index, status))
                time.sleep(0.02)
            
    finally:
        player.terminate()
        print("\nexited player")
    
if __name__ == "__main__":
    main()