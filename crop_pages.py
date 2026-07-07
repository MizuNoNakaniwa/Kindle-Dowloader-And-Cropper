import os
import glob
import tkinter as tk
from PIL import Image, ImageTk

IN_DIR  = "book_pages"
OUT_DIR = "book_pages_cropped"

files = sorted(glob.glob(os.path.join(IN_DIR, "*.png")))
if not files:
    print(f"找不到图片!确认 {IN_DIR} 文件夹里有 png,且脚本和它在同一目录")
    raise SystemExit

os.makedirs(OUT_DIR, exist_ok=True)

img = Image.open(files[0])
iw, ih = img.size

root = tk.Tk()
root.title("按住左键拖框圈出书页正文,拖好后按【回车】确认")

sw, sh = root.winfo_screenwidth() - 100, root.winfo_screenheight() - 150
scale = min(sw / iw, sh / ih, 1.0)
dw, dh = int(iw * scale), int(ih * scale)
disp = img.resize((dw, dh))
photo = ImageTk.PhotoImage(disp)

canvas = tk.Canvas(root, width=dw, height=dh)
canvas.pack()
canvas.create_image(0, 0, anchor="nw", image=photo)

box = {"x1": 0, "y1": 0, "x2": 0, "y2": 0}
rect_id = None

def on_press(e):
    global rect_id
    box["x1"], box["y1"] = e.x, e.y
    if rect_id:
        canvas.delete(rect_id)
    rect_id = canvas.create_rectangle(e.x, e.y, e.x, e.y, outline="red", width=3)

def on_drag(e):
    box["x2"], box["y2"] = e.x, e.y
    canvas.coords(rect_id, box["x1"], box["y1"], e.x, e.y)

def on_enter(e):
    root.quit()

canvas.bind("<ButtonPress-1>", on_press)
canvas.bind("<B1-Motion>", on_drag)
root.bind("<Return>", on_enter)

print("在弹出的窗口里拖框,然后按回车……")
root.mainloop()
root.destroy()

x1 = int(min(box["x1"], box["x2"]) / scale)
y1 = int(min(box["y1"], box["y2"]) / scale)
x2 = int(max(box["x1"], box["x2"]) / scale)
y2 = int(max(box["y1"], box["y2"]) / scale)

if x2 - x1 < 10 or y2 - y1 < 10:
    print("框太小或没拖框,退出。重新运行再试。")
    raise SystemExit

print(f"开始批量裁剪 {len(files)} 张图……")

for i, f in enumerate(files, 1):
    im = Image.open(f)
    im.crop((x1, y1, x2, y2)).save(os.path.join(OUT_DIR, os.path.basename(f)))
    if i % 20 == 0 or i == len(files):
        print(f"{i}/{len(files)}")

print(f"\n完成!裁好的图在文件夹:{OUT_DIR}(原图没动)")