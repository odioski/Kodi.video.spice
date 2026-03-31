# Video Spice

Video Spice is a Kodi service add-on that loads `video.spice.gif` as an animated overlay while video playback is active.

It is not a `plugin.video` add-on. A plugin is the right shape when Kodi needs a browsable media source or playable URLs. This project needs to react to any video that Kodi is already playing, so a background service is the more practical and standards-aligned add-on type.

## What it does

- Starts a background service when Kodi launches.
- Watches for video playback events.
- Opens a transparent dialog that draws `video.spice.gif` over the player.
- Closes the overlay automatically when playback ends or stops.

## Files

- `addon.xml`: Kodi add-on manifest.
- `service.py`: background playback watcher.
- `resources/lib/overlay.py`: overlay window and GIF loader.
- `video.spice.gif`: overlay asset used by the add-on.
- `tools/build-release.sh`: stages a Kodi-ready zip with the correct add-on id as the archive root.

## Build

Run:

```bash
./tools/build-release.sh
```

The release zip is written to `dist/service.video.spice-1.0.0.zip`.

## Install

1. Build the release zip with `./tools/build-release.sh`.
2. Install `dist/service.video.spice-1.0.0.zip` from Kodi's **Add-ons > Install from zip file** screen.
3. Enable the add-on if Kodi prompts you.
4. Start any video playback to see the overlay.

## Standards Notes

- The packaged release is built as a service add-on because that matches the runtime behavior.
- The build script excludes development clutter such as `__pycache__`, `.pyc`, and workspace files by staging only runtime files into the archive.
- The `language` metadata tag is intentionally omitted because this add-on does not provide media content.
- For official Kodi repository submission, you should still add `icon.png` and `fanart.jpg`, then declare them in `addon.xml` under an `<assets>` block.

## Tuning

If you want to reposition or resize the overlay, edit the constants in `resources/lib/overlay.py`.
