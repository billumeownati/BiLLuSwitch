# 🟩 BiLLuSwitch – GPU Mode Tray App for Fedora (supergfxctl GUI)

**BiLLuSwitch** is a lightweight system-tray application for **Fedora Linux (tested on Fedora 39–43)** that provides an easy GUI for switching GPU modes on ASUS laptops using **supergfxctl**.

It supports:

- **Integrated mode (iGPU)**
- **Hybrid mode**
- **dGPU mode (AsusMuxDgpu)**

Switching GPU modes often requires logout or reboot; BiLLuSwitch handles this seamlessly with a confirmation dialog and a 10-second countdown.

The application lives in your **system tray**, uses the **KDE “nvidia” icon**, and shows the current GPU mode instantly on hover or left-click.

---

## ✨ Features

### 🎛️ GPU Mode Switching
- One-click switching between **Integrated**, **Hybrid**, and **dGPU (AsusMuxDgpu)**
- Automatically detects whether a **reboot** or **logout** is required
- Confirmation dialog with **10-second auto-confirm countdown**

### ♻️ Pending Mode Detection
- Uses `supergfxctl -p` (Fedora 43: returns `"Unknown"` when no pending mode)
- If a pending mode exists → **all buttons disabled**
- Shows pending mode in tray menu

### 🖥️ System Tray App
- **Left-click** → show current GPU mode
- **Right-click** → full context menu
- Uses KDE’s **nvidia** icon
- Menu shows:
  - **Current Mode**
  - **Pending Mode**
  - Mode switch options
  - **Restart App**
  - **Quit**

### ⚡ Auto-Refreshing
- Refreshes mode + pending status every 1.5 seconds

### 🧰 Restart App Button
- Instantly restarts itself using Python `execv()`

---
