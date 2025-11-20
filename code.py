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


def run_cmd(cmd):
    try:
        return subprocess.check_output(cmd, shell=True).decode().strip()
    except Exception:
        return None


def get_current_mode():
    mode = run_cmd("supergfxctl -g")
    return mode if mode else "Unknown"


def get_pending_mode():
    p = run_cmd("supergfxctl -P")
    if not p:
        return "None"
    p_clean = p.strip().lower()
    if p_clean in ["", "none", "null", "unknown", "no pending mode"]:
        return "None"
    return p


def get_power_status():
    p = run_cmd("supergfxctl -S")
    if not p:
        return "Unknown"
    return p.capitalize()


def reboot_system():
    subprocess.call("systemctl reboot", shell=True)


def logout_system():
    subprocess.call("loginctl terminate-user $USER", shell=True)


class ConfirmDialog(QDialog):
    def __init__(self, mode, requires_reboot):
        super().__init__()
        self.setWindowIcon(QIcon.fromTheme("dialog-warning"))
        self.seconds = 10
        self.setWindowTitle(f"Switch to {mode}?")
        self.resize(330, 110)

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


class BilluSwitch(QSystemTrayIcon):
    def __init__(self):
        super().__init__()

        self.setIcon(QIcon.fromTheme("nvidia"))
        self.setToolTip(f"BiLLuSwitch – {get_current_mode()}\n\ndGPU Power: {get_power_status()}")

        self.menu = QMenu()

        # Current mode
        self.current_action = QAction(f"Current Mode: {get_current_mode()}")
        self.current_action.setEnabled(False)
        self.current_action.setIcon(QIcon.fromTheme("video-display"))
        self.menu.addAction(self.current_action)

        # dGPU power
        self.power_action = QAction(f"dGPU Power: {get_power_status()}")
        self.power_action.setEnabled(False)
        self.power_action.setIcon(QIcon.fromTheme("battery"))
        self.menu.addAction(self.power_action)

        self.menu.addSeparator()

        # Section title (unselectable)
        modes_header = QAction("Available Modes")
        modes_header.setEnabled(False)
        modes_header.setIcon(QIcon.fromTheme("preferences-system"))
        self.menu.addAction(modes_header)

        # Modes
        self.act_igpu = QAction("Integrated Mode")
        self.act_igpu.setIcon(QIcon.fromTheme("cpu"))
        self.act_hybrid = QAction("Hybrid Mode")
        self.act_hybrid.setIcon(QIcon.fromTheme("computer"))
        self.act_dgpu = QAction("dGPU Mode")
        self.act_dgpu.setIcon(QIcon.fromTheme("nvidia"))

        self.act_igpu.triggered.connect(lambda: self.apply_mode("Integrated"))
        self.act_hybrid.triggered.connect(lambda: self.apply_mode("Hybrid"))
        self.act_dgpu.triggered.connect(lambda: self.apply_mode("AsusMuxDgpu"))

        self.menu.addAction(self.act_igpu)
        self.menu.addAction(self.act_hybrid)
        self.menu.addAction(self.act_dgpu)

        self.menu.addSeparator()

        # Pending mode
        self.pending_action = QAction("Pending Mode: None")
        self.pending_action.setEnabled(False)
        self.pending_action.setIcon(QIcon.fromTheme("dialog-warning"))
        self.menu.addAction(self.pending_action)

        self.menu.addSeparator()

        # Restart App
        self.restart_action = QAction("Restart App")
        self.restart_action.setIcon(QIcon.fromTheme("view-refresh"))
        self.restart_action.triggered.connect(self.restart_app)
        self.menu.addAction(self.restart_action)

        # Quit
        self.quit_action = QAction("Quit")
        self.quit_action.setIcon(QIcon.fromTheme("application-exit"))
        self.quit_action.triggered.connect(lambda: sys.exit(0))
        self.menu.addAction(self.quit_action)

        self.setContextMenu(self.menu)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_state)
        self.timer.start(5000)

    def update_state(self):
        mode = get_current_mode()
        pending = get_pending_mode()
        power = get_power_status()

        self.setToolTip(f"BiLLuSwitch – {mode}\n\ndGPU Power: {power}")

        self.current_action.setText(f"Current Mode: {mode}")
        self.power_action.setText(f"dGPU Power: {power}")
        self.pending_action.setText(f"Pending Mode: {pending}")

        enable = (pending == "None")
        self.act_igpu.setEnabled(enable)
        self.act_hybrid.setEnabled(enable)
        self.act_dgpu.setEnabled(enable)

    def apply_mode(self, mode):
        current = get_current_mode()

        # If trying to switch to the current mode
        if current.lower() == mode.lower():
            dialog = QDialog()
            dialog.setWindowTitle("No Change Needed")
            dialog.setWindowIcon(QIcon.fromTheme("dialog-information"))
            dialog.resize(330, 90)
            layout = QVBoxLayout()
            msg = QLabel(f"You are already in {mode} mode.")
            layout.addWidget(msg)
            btn = QPushButton("OK")
            btn.clicked.connect(dialog.accept)
            layout.addWidget(btn)
            dialog.setLayout(layout)
            dialog.exec()
            return

        requires_reboot = (current == "AsusMuxDgpu" or mode == "AsusMuxDgpu")

        dialog = ConfirmDialog(mode, requires_reboot)
        if dialog.exec():
            run_cmd(f"supergfxctl -m {mode}")
            if requires_reboot:
                reboot_system()
            else:
                logout_system()


    def restart_app(self):
        python = sys.executable
        os.execv(python, [python] + sys.argv)


def main():
    app = QApplication(sys.argv)
    tray = BilluSwitch()
    tray.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
