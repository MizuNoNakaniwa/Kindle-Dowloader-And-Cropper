# -*- coding: utf-8 -*-
"""
极简劈图:窗口显示第一张图,红线跟着鼠标,点一下 → 所有图片全部按这个位置劈完。
用法:把本文件放进图片文件夹,运行  py split_all.py
结果在 split 子文件夹。
"""
from PIL import Image, ImageTk
import tkinter as tk
import glob, re, os, sys

OUT = 'split'
os.makedirs(OUT, exist_ok=True)

def natkey(p):
    return [int(t) if t.isdigit() else t for t in re.split(r'(\d+)', p)]

EXTS = ('*.jpg', '*.jpeg', '*.png', '*.webp')
files = sorted([f for e in EXTS for f in glob.glob(e)], key=natkey)
if not files:
    sys.exit('当前文件夹没找到图片')

root = tk.Tk()
root.title('点一下红线位置,全部图片自动劈开')
sw, sh = root.winfo_screenwidth() - 100, root.winfo_screenheight() - 150

first = Image.open(files[0])
scale = min(sw / first.width, sh / first.height, 1.0)
disp = first.resize((int(first.width * scale), int(first.height * scale)))
tkimg = ImageTk.PhotoImage(disp)

canvas = tk.Canvas(root, width=disp.width, height=disp.height,
                   cursor='crosshair')
canvas.pack()
status = tk.Label(root, text=f'共 {len(files)} 张图。移动鼠标对准中缝,'
                             '左键点一下,剩下的全自动。', font=('', 12))
status.pack()

canvas.create_image(0, 0, anchor='nw', image=tkimg)
line = canvas.create_line(disp.width // 2, 0, disp.width // 2, disp.height,
                          fill='red', width=2)

canvas.bind('<Motion>',
            lambda e: canvas.coords(line, e.x, 0, e.x, disp.height))

def go(e):
    canvas.unbind('<Button-1>')
    ratio = e.x / disp.width  # 记住比例,应用到所有图
    for i, f in enumerate(files, 1):
        im = Image.open(f)
        w, h = im.size
        x = max(1, min(w - 1, int(w * ratio)))
        im.crop((0, 0, x, h)).save(f'{OUT}/{i:04d}_1.jpg', quality=95)
        im.crop((x, 0, w, h)).save(f'{OUT}/{i:04d}_2.jpg', quality=95)
        status.config(text=f'处理中… {i}/{len(files)}')
        root.update()
    status.config(text=f'完成!{len(files)} 张 → {len(files)*2} 页,'
                       '在 split 文件夹里。本窗口 3 秒后关闭。')
    root.after(3000, root.destroy)

canvas.bind('<Button-1>', go)
root.mainloop()
