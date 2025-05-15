iimport xbmc
import xbmcgui
import xbmcaddon
import os

class Overlay(xbmcgui.WindowXMLDialog):
    def __init__(self, xmlFilename, *args, **kwargs):
        super().__init__(xmlFilename, *args, **kwargs)
        self.overlay_gif = xbmcgui.ControlImage(100, 100, 300, 300, kwargs['gif_path'])
        self.addControl(self.overlay_gif)

    def onInit(self):
        self.show()

    def onAction(self, action):
        if action == xbmcgui.ACTION_CLOSE:
            self.close()

def main():
    addon = xbmcaddon.Addon()
    gif_path = os.path.join(addon.getAddonInfo('path'), 'resources', 'media', 'resources/media/video.spice.gif')
    overlay = Overlay('resources\\skins\\default\\video.spice.xml', gif_path=gif_path)
    overlay.doModal()
    # del overlay
    # if __name__ == '__main__':
    #     main()
    main()
