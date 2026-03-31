import xbmc

from resources.lib.overlay import OverlayController


class OverlayPlayer(xbmc.Player):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

    def onAVStarted(self):
        self._sync_overlay()

    def onPlayBackStarted(self):
        self._sync_overlay()

    def onPlayBackStopped(self):
        self.controller.hide()

    def onPlayBackEnded(self):
        self.controller.hide()

    def onPlayBackError(self):
        self.controller.hide()

    def _sync_overlay(self):
        xbmc.sleep(250)
        if self.isPlayingVideo():
            self.controller.show()
        else:
            self.controller.hide()


def run():
    monitor = xbmc.Monitor()
    controller = OverlayController()
    player = OverlayPlayer(controller)

    xbmc.log("Video Spice: playback overlay service started", xbmc.LOGINFO)

    try:
        while not monitor.waitForAbort(1):
            if player.isPlayingVideo():
                controller.show()
            else:
                controller.hide()
    finally:
        controller.hide()
        xbmc.log("Video Spice: playback overlay service stopped", xbmc.LOGINFO)


if __name__ == "__main__":
    run()
