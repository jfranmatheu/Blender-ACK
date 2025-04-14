# /icons.py
# Code automatically generated!
from pathlib import Path
from .ackit.auto_code.icons import IconsEnum, IconsViewer

icons_dirpath = Path("lib/icons")


class Icons(IconsViewer):

	class MAIN(IconsEnum):
		BLUE_BUTTON = icons_dirpath / "blue_button.png"
		GALLERY_OUTLINE = icons_dirpath / "gallery_outline.png"
		MUSIC_AUDIO_WAVES = icons_dirpath / "music_audio_waves.png"
		ADD_TO_INBOX = icons_dirpath / "[icons8]add_to_inbox.png"
		TEXTURE_SMALL = icons_dirpath / "[icons8]texture_small.png"

