# 🟩 BiLLuSwitch – GPU Mode Tray App for Fedora

**BiLLuSwitch** is a lightweight system-tray application for **Fedora Linux** (tested on Fedora 39–43). It provides an easy GUI for switching GPU modes on ASUS laptops by interfacing directly with **supergfxctl**.



It lives in your system tray using the KDE "nvidia" icon. The current GPU mode is shown instantly when you **hover** over the icon.

## ✨ Features

### 🎛️ GPU Mode Switching
- One-click switching between **Integrated**, **Hybrid**, and **dGPU (AsusMuxDgpu)**.
- Automatically detects whether a **reboot** or **logout** is required to apply the change.
- Confirmation dialog with a **10-second auto-confirm countdown**.

### ♻️ Pending Mode Detection
- Automatically detects if a mode change is already queued via `supergfxctl`.
- If a change is pending (waiting for reboot), **all buttons are disabled** to prevent conflicts.
- Displays the pending status clearly in the menu.

### ⚡ Auto-Refreshing
- Refreshes GPU status every **1.5 seconds**.
- Hover tooltip updates automatically.

### 🧰 Extra Tools
- **Restart App:** Instantly restarts the script if it glitches.
- **Quit:** Closes the tray icon.

---

## 📦 Requirements

You need an ASUS laptop with `supergfxctl` configured.

**Python Dependencies:**
```bash
pip install PyQt6
```

---

## 🚀 Installation & Usage

1.  **Download the script**
    Save the code as `billuswitch.py`.

2.  **Make it executable**
    Open your terminal in the folder where you saved it:
    ```bash
    chmod +x billuswitch.py
    ```

3.  **Run it**
    ```bash
    ./billuswitch.py
    ```

---

## ❓ Troubleshooting

**The icon doesn't show up?**
- Make sure you have `AppIndicator` or `System Tray` support enabled in your Desktop Environment (GNOME users usually need an extension for this).

**"Unknown" Mode?**
- Ensure the supergfxctl service is running.

---

## 📜 License
Open Source. Feel free to modify and share.