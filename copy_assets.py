# -*- coding: utf-8 -*-
import shutil
import os

base = os.path.dirname(os.path.abspath(__file__))
dest = os.path.join(base, "portfolio", "public")

# 1. Copy ChatGPT PNG (check base and parent/Downloads)
png_name = "ChatGPT Image 2026년 3월 10일 오후 01_51_09.png"
found = False
for check_dir in [base, os.path.dirname(base)]:
    src_png = os.path.join(check_dir, png_name)
    if os.path.isfile(src_png):
        shutil.copy2(src_png, os.path.join(dest, os.path.basename(src_png)))
        print(f"Copied: {png_name}")
        found = True
        break
if not found:
    # Fallback: any ChatGPT Image*.png in base
    for f in os.listdir(base):
        if f.startswith("ChatGPT Image") and f.endswith(".png"):
            shutil.copy2(os.path.join(base, f), dest)
            print(f"Copied: {f}")
            break
    else:
        print("No ChatGPT PNG found")

# 1.5. Copy intro.png to portfolio/public
intro_png = os.path.join(base, "intro.png")
if os.path.isfile(intro_png):
    shutil.copy2(intro_png, os.path.join(dest, "intro.png"))
    print("Copied: intro.png")
else:
    print("intro.png not found in project root")

# 2. Copy folder
folder = os.path.join(base, "현실을 넘어선, 가상공간을 향하여")
dest_folder = os.path.join(dest, "현실을 넘어선, 가상공간을 향하여")
if os.path.isdir(folder):
    if os.path.exists(dest_folder):
        shutil.rmtree(dest_folder)
    shutil.copytree(folder, dest_folder)
    print("Copied folder: 현실을 넘어선, 가상공간을 향하여")
else:
    print(f"Folder not found: {folder}")
