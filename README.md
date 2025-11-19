# 🟩 **BiLLuSwitch**
### *A Sleek GPU-Mode Tray App for ASUS Laptops on Fedora*

**BiLLuSwitch** is a tiny, fast, and elegant system-tray utility for **ASUS laptops** running Fedora.  
It provides a clean GUI to manage GPU modes using **supergfxctl** — without needing to touch the terminal.

It blends perfectly with KDE Plasma, using automatic theme icons and non-intrusive tray UI.

---

## ✨ Features

### 🎛 **Effortless GPU Mode Switching**
- Switch between **Integrated**, **Hybrid**, and **dGPU (AsusMuxDgpu)** modes.
- BiLLuSwitch automatically determines if a **logout** or a **reboot** is required.
- Beautiful confirmation dialog with a **10-second auto-confirm** countdown.

---

### 🕵️ **Real-Time Status Monitoring**
BiLLuSwitch shows:

- **Current GPU Mode**
- **Pending Mode Change**
- **dGPU Power Status** *(Active, Suspended, Off, etc.)*

Status updates refresh every **5 seconds**.

---

### 🔒 **Smart Safety Logic**
- Already in that mode? BiLLuSwitch informs you.
- Pending mode change? Options auto-disable until safe.

---

### 🧰 **Tools Built In**
- **Restart App** — quickly reload the script  
- **Quit** — closes the tray icon  
- Icon-based menu that blends with KDE

---

## 📦 Requirements

ASUS laptop with **supergfxctl** installed.

Install PyQt6:

```
pip install PyQt6
```

---

## 🚀 Installation

1. Download `billuswitch.py`
2. Make executable:
   ```
   chmod +x billuswitch.py
   ```
3. Run:
   ```
   ./billuswitch.py
   ```

---

## ❓ Troubleshooting

**Tray icon not visible?**  
- KDE: ensure system tray is enabled  
- GNOME: requires AppIndicator extension  

**Shows "Unknown"?**  
Restart:
```
sudo systemctl restart supergfxd
```

---

## 📜 License  
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  Made with ❤️ for the Linux community.
</p>