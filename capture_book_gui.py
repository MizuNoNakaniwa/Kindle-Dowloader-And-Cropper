import os
import time
import threading
import tkinter as tk
import pyautogui
import keyboard

DELAY   = 3            # 每页停留秒数
OUT_DIR = "book_pages" # 图片输出文件夹
TURN_MODE = "key"      # "key"=按键翻页 / "click"=鼠标点击
TURN_KEY  = "right"
CLICK_XY  = (1800, 700)
MAX_PAGES = 2000       # 安全上限,自动停

pyautogui.FAILSAFE = True
os.makedirs(OUT_DIR, exist_ok=True)

running = False
stopped = False
count = 0

def worker():
    global count, running, stopped
    while not stopped:
        if not running:
            time.sleep(0.1)
            continue
        count += 1
        shot = pyautogui.screenshot()
        shot.save(os.path.join(OUT_DIR, f"page_{count:04d}.png"))
        status_var.set(f"运行中… 已抓 {count} 页")
        if TURN_MODE == "key":
            pyautogui.press(TURN_KEY)
        else:
            pyautogui.click(*CLICK_XY)
        for _ in range(int(DELAY * 10)):
            if stopped or not running:
                break
            time.sleep(0.1)
        if count >= MAX_PAGES:
            stop()

def toggle():
    global running
    if stopped:
        return
    running = not running
    if running:
        status_var.set("3 秒后开始,快点回阅读器窗口!")
        btn_toggle.config(text="暂停 (F8)")
    else:
        status_var.set(f"已暂停,共 {count} 页。按 F8 继续")
        btn_toggle.config(text="继续 (F8)")

def stop():
    global stopped, running
    stopped = True
    running = False
    status_var.set(f"已停止。共抓了 {count} 页,在文件夹 {OUT_DIR}")
    btn_toggle.config(state="disabled")
    btn_stop.config(state="disabled")

root = tk.Tk()
root.title("电子书抓取器")
root.attributes("-topmost", True)
root.geometry("300x150+50+50")

status_var = tk.StringVar(value="就绪。点「开始」或按 F8")
tk.Label(root, textvariable=status_var, wraplength=280).pack(pady=10)
btn_toggle = tk.Button(root, text="开始 (F8)", width=15, height=2, command=toggle)
btn_toggle.pack()
btn_stop = tk.Button(root, text="停止 (F9)", width=15, command=stop)
btn_stop.pack(pady=5)

keyboard.add_hotkey("f8", lambda: root.after(0, toggle))
keyboard.add_hotkey("f9", lambda: root.after(0, stop))

threading.Thread(target=worker, daemon=True).start()
root.mainloop()