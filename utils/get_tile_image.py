from pathlib import Path
from tkinter import PhotoImage

def get_tile_image(asset: Path | None) -> PhotoImage:
    if asset:
        return PhotoImage(file=asset)
    else:
        return PhotoImage(asset)