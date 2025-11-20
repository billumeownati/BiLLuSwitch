# 🟩 **BiLLuSwitch**
### *A Sleek GPU-Mode Tray App for ASUS Laptops on Fedora*

**BiLLuSwitch** is a lightweight, fast, and elegant system-tray utility for **ASUS laptops** running Fedora.  
It provides a clean GUI to manage GPU modes using **supergfxctl**, with automatic theme icons and smooth KDE Plasma integration.

---

## ✨ Features

### 🎛 **Effortless GPU Mode Switching**
- Switch between **Integrated**, **Hybrid**, and **dGPU (AsusMuxDgpu)** modes.
- Automatically detects whether a **logout** or a **reboot** is required.
- **10-second confirmation dialog** with auto-proceed countdown.
- Prevents unnecessary switching by detecting **"Already in this mode"**.

---

### 🕵️ **Real-Time Status Monitoring**
BiLLuSwitch displays live GPU information:

- **Current GPU Mode**
- **dGPU Power Status** *(Active, Suspended, Off, etc.)*
- **Pending Mode Change**

Status refreshes every **5 seconds** and the tray tooltip shows:

```
BiLLuSwitch – Hybrid
dGPU Power: Suspended
```

---

### 🧼 **Clean KDE-Styled UI**
- Section dividers for easy navigation  
- Automatic KDE/GTK theme icons  
- Window icons on dialogs  
- Modes neatly grouped under **Available Modes**

---

### 🧰 **Built-In Tools**
- **Restart App**  
- **Quit**

---

## 📦 Requirements
- ASUS laptop with **supergfxctl** installed.  
- Install PyQt6:

```
pip install PyQt6
```

---

## 🚀 Installation

1. Download `billuswitch.py`  
2. Make it executable:

```bash
chmod +x billuswitch.py
```

3. Run:

```bash
./billuswitch.py
```

---

## ❓ Troubleshooting

**Tray icon missing?**  
- KDE: Ensure the System Tray widget is enabled  
- GNOME: Install AppIndicator/KStatusNotifierItem

**Showing “Unknown”?**  
Restart `supergfxd`:

```bash
sudo systemctl restart supergfxd
```

---

## 📜 License  
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  Made with ❤️ for the Linux community.
</p>