# render terminal
# handle keybinds

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.console import Group

#con = Console()

def format_time(sec: float) -> str:
    mins,secs = divmod(int(sec), 60)
    return f"{mins:02d}:{secs:02d}"

def render_ui(tracks: list, selected_index: int, playing_index: int, status: dict, max_visible: int = 20):
    #con.clear()

    # header
    if status.get("paused"):
        status_str = "paused"
    else:
        status_str = "playing"

    #vol_str = f"vol: {status.get('vol')}%"
    if playing_index >= 0:
        now_playing = tracks[playing_index].title
    else:
        now_playing = "none"

    header_panel = Panel(
        f"[bold green]CLI Player[/bold green] | Status: [bold yellow]{status_str}[/bold yellow] {now_playing}",
        expand = False,
    )
    #con.print(header_panel)

    # track table
    tab = Table(
        show_header = True,
        header_style = "bold yellow",
        expand = True
    )
    tab.add_column(
        "state",
        style = "bold cyan",
        width = 6,
        justify = "center"
    )
    tab.add_column(
        "#",
        style = "dim",
        width = 4
    )
    tab.add_column(
        "title",
        style = "white"
    )
    tab.add_column(
        "artist",
        style = "yellow"
    )
    tab.add_column(
        "duration",
        style = "white"
    )

    # slicing viewport
    total_tracks = len(tracks)

    half_window = max_visible // 2
    start_index = max(0, selected_index - half_window)
    end_index = min(total_tracks, start_index + max_visible)

    if end_index - start_index < max_visible:
        start_index = max(0, end_index - max_visible)
    
    visible_tracks = tracks[start_index: end_index]

    #for index, track in enumerate(tracks):
    for offset, track in enumerate(visible_tracks):
        index = start_index + offset
        is_playing = (index == playing_index)
        is_selected = (index == selected_index)

        if is_playing:
            state_icon = " ▶ "
        else:
            state_icon = "   "
        
        if is_selected:
            style = "reverse yellow"
        elif is_playing:
            style = "bold cyan"
        else:
            style = None
        
        dur = format_time(track.duration)
        tab.add_row(
            state_icon,
            str(index+1),
            track.title,
            track.artist,
            dur,
            style = style
        )
    
    #con.print(tab)

    # playback
    pos = format_time(status.get("time_pos", 0))
    dur = format_time(status.get("duration", 0))
    #con.print(
        #f"\n[bold]progress:[/bold] {pos} / {dur}\n", style = "white"
    #)
    progress_panel = f"\n[bold]progress:[/bold] {pos} / {dur}\n"
    # controls
    #con.print(
        #"[dim]controls: {j/k} navigate | {space} play/pause | {+/-} volume | {q} quit[/dim]"
    #)
    controls_panel = "[dim]controls: {j/k} navigate | {space} play/pause | {+/-} volume | {q} quit[/dim]"

    return Group(
        header_panel,
        tab,
        progress_panel,
        controls_panel
    )