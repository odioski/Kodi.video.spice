import os

import xbmc
import xbmcaddon
import xbmcgui
import xbmcvfs


ADDON = xbmcaddon.Addon()
ADDON_PATH = xbmcvfs.translatePath(ADDON.getAddonInfo("path"))
GIF_PATH = os.path.join(ADDON_PATH, "video.spice.gif")

OVERLAY_WIDTH = 360
OVERLAY_HEIGHT = 360
OVERLAY_MARGIN_X = 48
OVERLAY_MARGIN_Y = 48


def _screen_size():
    width = _read_dimension("System.ScreenWidth", 1920)
    height = _read_dimension("System.ScreenHeight", 1080)
    return width, height


def _read_dimension(label, fallback):
    try:
        return int(xbmc.getInfoLabel(label))
    except (TypeError, ValueError):
        return fallback


class OverlayWindow(xbmcgui.WindowDialog):
    def __init__(self, gif_path):
        super().__init__()

        screen_width, _ = _screen_size()
        x_pos = max(0, screen_width - OVERLAY_WIDTH - OVERLAY_MARGIN_X)
        y_pos = OVERLAY_MARGIN_Y

        self.overlay = xbmcgui.ControlImage(
            x_pos,
            y_pos,
            OVERLAY_WIDTH,
            OVERLAY_HEIGHT,
            gif_path,
            colorDiffuse="FFFFFFFF",
        )
        self.addControl(self.overlay)


class OverlayController:
    def __init__(self):
        self.window = None

    def show(self):
        if self.window is not None:
            return

        if not xbmcvfs.exists(GIF_PATH):
            xbmc.log(
                "Video Spice: could not find overlay GIF at {}".format(GIF_PATH),
                xbmc.LOGERROR,
            )
            return

        self.window = OverlayWindow(GIF_PATH)
        self.window.show()

    def hide(self):
        if self.window is None:
            return

        self.window.close()
        self.window = None
