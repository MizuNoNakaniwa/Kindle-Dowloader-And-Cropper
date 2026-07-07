[中文](./README.md) | **English**

# Kindle-Dowloader-And-Cropper

Two small tools that work together to turn e-books locked inside proprietary reader apps (with no export option) into clean page images:

- `capture_book_gui.py` — auto page-turn + screenshot, with an always-on-top control panel; start and stop whenever you want
- `crop_pages.py` — drag one box on the first screenshot to batch-crop the UI clutter off every image, keeping only the page content

Works strictly inside its own folder: screenshots go to `book_pages`, cropped results go to `book_pages_cropped`. No subfolders entered, no files elsewhere touched, and original screenshots are never modified. Delete them manually if you want them gone.

## How to Use

1. Download the two scripts above — just these two: `capture_book_gui.py` and `crop_pages.py` — and put them in the same folder
2. Open a terminal (Win+R, type cmd), go to that folder, and run `pip install pyautogui pillow keyboard` (one-time install)
3. Open your e-book reader and go to the first page
4. Run `python capture_book_gui.py`; an always-on-top control panel appears. Click "Start" (or press F8), click back into the reader window within 3 seconds, then walk away — it turns pages and screenshots on its own. Press F9 to stop when done
5. Run `python crop_pages.py`; your first screenshot pops up. Hold the left mouse button and drag a red box around the page content, press Enter, and all images are batch-cropped automatically
6. Enjoy! Clean page images are in the `book_pages_cropped` folder in the same directory

## Notes

- Requires Python 3 (on Windows, install from [python.org](https://www.python.org) and check "Add Python to PATH" during setup)
- Capture tool hotkeys are global: F8 start/pause, F9 stop — they work even when the reader is fullscreen; emergency brake: slam your mouse into the top-left corner of the screen to abort instantly
- Page turning defaults to the Right Arrow key (→); if your reader only turns pages via mouse click, open `capture_book_gui.py` and set `TURN_MODE` to `"click"` in the config section, then fill in the click coordinates
- Each page waits 3 seconds to render by default; increase `DELAY` in the config section if pages load slowly
- Recommended: capture five or six pages first, press F9, check the images in `book_pages`, then run the full capture
- Dragged the crop box wrong? Just drag again — the last box counts. Cropped badly? No loss — originals are untouched, rerun and re-drag
- One-box-fits-all cropping assumes the reader window never moved during capture
