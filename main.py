import sys
import os
import shutil
import time
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QListWidget,
                             QProgressBar, QMessageBox, QHBoxLayout)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QPalette, QColor


class FileCopyThread(QThread):
    progress_signal = pyqtSignal(int)
    status_signal = pyqtSignal(str)
    speed_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)

    def __init__(self, source_files, dest_folder):
        super().__init__()
        self.source_files = source_files
        self.dest_folder = dest_folder
        self.paused = False
        self.stop_transfer = False

    def run(self):
        total_size = sum(os.path.getsize(f) if os.path.isfile(f) else sum(
            os.path.getsize(os.path.join(root, file)) for root, _, files in os.walk(f) for file in files) for f in
                         self.source_files)
        copied_size = 0
        start_time = time.time()

        for src in self.source_files:
            while self.paused:
                self.msleep(100)
            if self.stop_transfer:
                return

            dest_path = os.path.join(self.dest_folder, os.path.basename(src))
            try:
                if os.path.isdir(src):
                    shutil.copytree(src, dest_path, dirs_exist_ok=True)
                    for root, _, files in os.walk(src):
                        for file in files:
                            file_path = os.path.join(root, file)
                            copied_size += os.path.getsize(file_path)
                            progress = int((copied_size / total_size) * 100)
                            self.progress_signal.emit(progress)
                            self.update_speed(copied_size, start_time)
                else:
                    shutil.copy2(src, dest_path)
                    copied_size += os.path.getsize(src)
                    progress = int((copied_size / total_size) * 100)
                    self.progress_signal.emit(progress)
                    self.update_speed(copied_size, start_time)
            except Exception as e:
                self.error_signal.emit(f"Error copying {src}: {e}")

        self.status_signal.emit("completed")

    def update_speed(self, copied_size, start_time):
        elapsed_time = time.time() - start_time
        speed = copied_size / (elapsed_time * 1024 * 1024)  # Speed in MB/s
        self.speed_signal.emit(f"Speed: {speed:.2f} MB/s")


class FileTransferTool(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.copy_thread = None
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self.update_animation)
        self.animation_text = ""
        self.animation_index = 0

    def initUI(self):
        self.setWindowTitle("Local File Transfer Tool")
        self.setGeometry(100, 100, 800, 400)

        self.setDarkMode()

        layout = QHBoxLayout()

        self.source_panel = QVBoxLayout()
        self.source_label = QLabel("Source: Not Selected")
        self.select_source_btn = QPushButton("Choose Files/Folders")
        self.file_list = QListWidget()
        self.remove_selected_btn = QPushButton("Remove Selected")
        self.clear_btn = QPushButton("Clear All")

        self.select_source_btn.clicked.connect(self.select_source)
        self.remove_selected_btn.clicked.connect(self.remove_selected)
        self.clear_btn.clicked.connect(self.clear_selection)

        self.source_panel.addWidget(self.source_label)
        self.source_panel.addWidget(self.select_source_btn)
        self.source_panel.addWidget(self.file_list)
        self.source_panel.addWidget(self.remove_selected_btn)
        self.source_panel.addWidget(self.clear_btn)

        self.dest_panel = QVBoxLayout()
        self.dest_label = QLabel("Destination: Not Selected")
        self.select_dest_btn = QPushButton("Select Destination Folder")
        self.progress = QProgressBar()
        self.speed_label = QLabel("Speed: 0.00 MB/s")
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red;")

        self.start_transfer_btn = QPushButton("Start Transfer")
        self.pause_btn = QPushButton("Pause")
        self.resume_btn = QPushButton("Resume")
        self.cancel_btn = QPushButton("Cancel")
        self.animation_label = QLabel("")

        self.update_button_style(self.start_transfer_btn, "green")
        self.update_button_style(self.pause_btn, "orange")
        self.update_button_style(self.resume_btn, "blue")
        self.update_button_style(self.cancel_btn, "red")

        self.select_dest_btn.clicked.connect(self.select_destination)
        self.start_transfer_btn.clicked.connect(self.start_transfer)
        self.pause_btn.clicked.connect(self.pause_transfer)
        self.resume_btn.clicked.connect(self.resume_transfer)
        self.cancel_btn.clicked.connect(self.cancel_transfer)

        self.dest_panel.addWidget(self.dest_label)
        self.dest_panel.addWidget(self.select_dest_btn)
        self.dest_panel.addWidget(self.progress)
        self.dest_panel.addWidget(self.speed_label)
        self.dest_panel.addWidget(self.error_label)
        self.dest_panel.addWidget(self.start_transfer_btn)
        self.dest_panel.addWidget(self.pause_btn)
        self.dest_panel.addWidget(self.resume_btn)
        self.dest_panel.addWidget(self.cancel_btn)
        self.dest_panel.addWidget(self.animation_label)

        layout.addLayout(self.source_panel)
        layout.addLayout(self.dest_panel)

        self.setLayout(layout)

        self.source_files = []
        self.dest_folder = ""

    def setDarkMode(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(45, 45, 45))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Button, QColor(70, 70, 70))
        palette.setColor(QPalette.ButtonText, Qt.white)
        self.setPalette(palette)

    def select_source(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self, "Select Files", options=options)
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")

        if files:
            self.source_files.extend(files)
        if folder:
            self.source_files.append(folder)

        self.source_label.setText("Source: Selected")
        self.load_files()

    def remove_selected(self):
        selected_items = self.file_list.selectedItems()
        for item in selected_items:
            self.source_files.remove(item.text())
            self.file_list.takeItem(self.file_list.row(item))

    def clear_selection(self):
        self.source_files.clear()
        self.file_list.clear()
        self.source_label.setText("Source: Not Selected")

    def select_destination(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Destination Folder")
        if folder:
            self.dest_folder = folder
            self.dest_label.setText(f"Destination: {folder}")

    def load_files(self):
        self.file_list.clear()
        for file in self.source_files:
            self.file_list.addItem(file)

    def start_transfer(self):
        if not self.source_files or not self.dest_folder:
            QMessageBox.warning(self, "Error", "Please select both source files and destination folder")
            return

        self.update_button_style(self.start_transfer_btn, "darkgreen")
        self.animation_timer.start(500)  # Start animation
        self.animation_text = "Copying"
        self.animation_label.setText("Copying...")

        self.copy_thread = FileCopyThread(self.source_files, self.dest_folder)
        self.copy_thread.progress_signal.connect(self.progress.setValue)
        self.copy_thread.status_signal.connect(self.transfer_completed)
        self.copy_thread.speed_signal.connect(self.speed_label.setText)
        self.copy_thread.error_signal.connect(self.error_label.setText)
        self.copy_thread.start()

    def pause_transfer(self):
        if self.copy_thread:
            self.copy_thread.paused = True
            self.update_button_style(self.pause_btn, "darkorange")
            self.animation_timer.stop()  # Stop the animation
            self.animation_label.setText("Paused")

    def resume_transfer(self):
        if self.copy_thread:
            self.copy_thread.paused = False
            self.update_button_style(self.resume_btn, "darkblue")
            self.animation_timer.start(500)  # Restart the animation
            self.animation_text = "Copying"
            self.animation_label.setText("Copying...")

    def cancel_transfer(self):
        if self.copy_thread:
            self.copy_thread.stop_transfer = True
            self.copy_thread.wait()
            self.copy_thread = None
            self.progress.setValue(0)
            self.animation_label.setText("Transfer Cancelled")
            self.animation_timer.stop()

    def transfer_completed(self, status):
        self.animation_timer.stop()
        self.animation_label.setText("")
        QMessageBox.information(self, "Success", "File transfer completed!")

    def update_animation(self):
        if self.animation_text == "Copying":
            animation_frames = ["Copying   ", "Copying.  ", "Copying.. ", "Copying..."]
            self.animation_label.setText(animation_frames[self.animation_index])
            self.animation_index = (self.animation_index + 1) % len(animation_frames)

    def update_button_style(self, button, color):
        button.setStyleSheet(f"background-color: {color}; color: white;")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileTransferTool()
    window.show()
    sys.exit(app.exec_())