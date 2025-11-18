#!/usr/bin/env python3
import subprocess
import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QSystemTrayIcon, QMenu, QDialog,
    QVBoxLayout, QLabel, QPushButton, QHBoxLayout
)
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import QTimer


# -----------------------------
# Helpers
# -----------------------------
def run_cmd(cmd):
    try:
        out = subprocess.check_output(cmd, shell=True).decode().strip()
        print(f"[DEBUG] CMD `{cmd}` → '{out}'")
        return out
    except Exception as e:
        print(f"[ERROR] run_cmd('{cmd}') failed: {e}")
        return None


def get_current_mode():
    mode = run_cmd("supergfxctl -g")
    if not mode:
        mode = "Unknown"
    print(f"[DEBUG] Current Mode = {mode}")
    return mode


def get_pending_mode():
    # Fedora 43: supergfxctl -P returns "Unknown" when no pending mode
    p = run_cmd("supergfxctl -P")
    print(f"[DEBUG RAW] Pending mode output = '{p}'")

    if p is None:
        return "None"

    p_clean = p.strip().lower()

    if p_clean in ["", "none", "null", "unknown", "no pending mode"]:
        return "None"

    return p


def reboot_system():
    subprocess.call("systemctl reboot", shell=True)


def logout_system():
    subprocess.call("loginctl terminate-user $USER", shell=True)


# -----------------------------
# Confirmation dialog
# -----------------------------
class ConfirmDialog(QDialog):
    def __init__(self, mode, requires_reboot):
        super().__init__()
        self.seconds = 10
        self.setWindowTitle(f"Switch to {mode}?")

        self.resize(320,100)

        msg = "This requires a reboot." if requires_reboot else "This requires logout."

        layout = QVBoxLayout()
        self.label = QLabel(f"{msg}\nProceed in {self.seconds} seconds?")
        layout.addWidget(self.label)

        btns = QHBoxLayout()
        yes = QPushButton("Yes")
        no = QPushButton("Cancel")

        yes.clicked.connect(self.accept)
        no.clicked.connect(self.reject)

        btns.addWidget(yes)
        btns.addWidget(no)
        layout.addLayout(btns)

        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        self.timer.start(1000)

    def tick(self):
        self.seconds -= 1
        if self.seconds <= 0:
            self.timer.stop()
            self.accept()
            return

        text = self.label.text().split("\n")[0]
        self.label.setText(text + f"\nProceed in {self.seconds} seconds?")


# -----------------------------
# System Tray App
# -----------------------------
class BilluSwitch(QSystemTrayIcon):
    def __init__(self):
        super().__init__()

        print("[DEBUG] Tray icon created")

        self.setIcon(QIcon.fromTheme("nvidia"))
        self.setToolTip(f"BiLLuSwitch – {get_current_mode()}")
        self.menu = QMenu()

        # ---------- CURRENT MODE ----------
        self.current_action = QAction(f"Current Mode: {get_current_mode()}")
        self.current_action.setEnabled(False)
        self.menu.addAction(self.current_action)

        self.menu.addSeparator()

        # ---------- MODE OPTIONS ----------
        self.act_igpu = QAction("Integrated Mode")
        self.act_hybrid = QAction("Hybrid Mode")
        self.act_dgpu = QAction("dGPU Mode")

        self.act_igpu.triggered.connect(lambda: self.apply_mode("Integrated"))
        self.act_hybrid.triggered.connect(lambda: self.apply_mode("Hybrid"))
        self.act_dgpu.triggered.connect(lambda: self.apply_mode("AsusMuxDgpu"))

        self.menu.addAction(self.act_igpu)
        self.menu.addAction(self.act_hybrid)
        self.menu.addAction(self.act_dgpu)

        self.menu.addSeparator()

        # ---------- PENDING MODE ----------
        self.pending_action = QAction("Pending Mode: None")
        self.pending_action.setEnabled(False)
        self.menu.addAction(self.pending_action)

        self.menu.addSeparator()

        # ---------- RESTART APP ----------
        self.restart_action = QAction("Restart App")
        self.restart_action.triggered.connect(self.restart_app)
        self.menu.addAction(self.restart_action)
        print("[DEBUG] Restart App added")

        # ---------- QUIT ----------
        self.quit_action = QAction("Quit")
        self.quit_action.triggered.connect(lambda: sys.exit(0))
        self.menu.addAction(self.quit_action)
        print("[DEBUG] Quit added")

        self.setContextMenu(self.menu)


        # Refresh timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_state)
        self.timer.start(1500)

        print("[DEBUG] Initialization completed")

    # -----------------------------
    def update_state(self):
        print("[DEBUG] update_state() running…")

        mode = get_current_mode()
        pending = get_pending_mode()

        print(f"[DEBUG] Pending Mode normalized = '{pending}'")
        self.setToolTip(f"BiLLuSwitch – {mode}")

        # Update current mode in menu
        self.current_action.setText(f"Current Mode: {mode}")

        # Update pending in menu
        self.pending_action.setText(f"Pending Mode: {pending}")

        # disable when pending mode exists
        enable = (pending == "None")
        print(f"[DEBUG] Buttons enabled = {enable}")

        self.act_igpu.setEnabled(enable)
        self.act_hybrid.setEnabled(enable)
        self.act_dgpu.setEnabled(enable)

    # -----------------------------
    def apply_mode(self, mode):
        current = get_current_mode()
        requires_reboot = (current == "AsusMuxDgpu" or mode == "AsusMuxDgpu")

        dialog = ConfirmDialog(mode, requires_reboot)
        if dialog.exec():
            run_cmd(f"supergfxctl -m {mode}")
            if requires_reboot:
                reboot_system()
            else:
                logout_system()

    # -----------------------------
    def restart_app(self):
        python = sys.executable
        os.execv(python, [python] + sys.argv)


# -----------------------------
def main():
    app = QApplication(sys.argv)
    tray = BilluSwitch()
    tray.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
