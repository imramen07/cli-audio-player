import sys
import time
from lib import scan_dir
from player import AudioPlayer
import readchar
from interface import render_ui

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

    try:
        while True:
            status = player.get_status()
            render_ui(tracks, selected_index, playing_index, status)

            key = readchar.readkey()

            if key == "q":
                break
            elif key == "j":
                selected_index = (selected_index+1) % len(tracks)
                #player.play(tracks[current_index].filepath)
            elif key == "k":
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
            
            time.sleep(0.05)
        
    finally:
        player.terminate()
        print("\nexited player")
    
if __name__ == "__main__":
    main()