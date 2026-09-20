# cli-audio-player

A lightweight terminal-based audio player.
Built with python, `rich`, `libmpv`.
Focuses on high-fidelity bit-perfect playback.

## Features
- Format Support: `.flac`, `.wav`, `.mp3`.
- Keyboard Navigation: vim style `j`/`k` controls with smooth viewport autoscrolling.
- Double buffer terminal interface by Rich Live and non-blocking input threading.
- Direct `libmpv` binding for minimum memory overhead.

## Prerequisites
- Requires `mpv` installed on the system
```bash
sudo pacman -S mpv python
```

## Installation
clone the repo
```bash
git clone https://github.com/imramen07/cli-audio-player.git
cd cli-audio-player
```
setup python virtual environmentand install dependencies
```bash
python -m venv cap
source cap/bin/activate
pip install -r requirements.txt
```

## Usage
run the player by passing the path to the audio directory
```bash
python main.py ~/Music
```

## Keybindings
j/DOWN - move selection down
k/UP - move selection up
ENTER - play selected track
SPACE/p - toggle play/pause
+/- - increase/decrease volume
q - quit player

## Project Structure
cli-audio-player/
├── main.py
├── player.py
├── library.py
├── interface.py
└── requirements.txt