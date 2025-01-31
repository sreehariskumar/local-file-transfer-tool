import sys
import os
import shutil
import threading
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QListWidget,
                             QProgressBar, QMessageBox, QHBoxLayout)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QPalette, QColor

class FileCopyThread(QThread):
    progress_signal = pyqtSignal(int)
    status_signal = pyqtSignal(str)

    def __init__(self, source_files, dest_folder):
        super().__init__()
        self.source_files = source_files
        self.dest_folder = dest_folder
        self.paused = False
        self.stop_transfer = False

    def run(self):
        total_size = sum(os.path.getsize(f) if os.path.isfile(f) else sum(os.path.getsize(os.path.join(root, file)) for root, _, files in os.walk(f) for file in files) for f in self.source_files)
        copied_size = 0

        for src in self.source_files:
            while self.paused:
                self.msleep(100)
            if self.stop_transfer:
                return
            
            dest_path = os.path.join(self.dest_folder, os.path.basename(src))
            try:
                if os.path.isdir(src):
                    shutil.copytree(src, dest_path, dirs_exist_ok=True)
                else:
                    shutil.copy2(src, dest_path)
                    copied_size += os.path.getsize(src)
            except Exception as e:
                print(f"Error copying {src}: {e}")
            
            progress = int((copied_size / total_size) * 100)
            self.progress_signal.emit(progress)
        
        self.status_signal.emit("completed")

class FileTransferTool(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.copy_thread = None
    
    def initUI(self):
        self.setWindowTitle("Local File Transfer Tool")
        self.setGeometry(100, 100, 800, 400)
        
        self.setDarkMode()
        
        layout = QHBoxLayout()
        
        self.source_panel = QVBoxLayout()
        self.source_label = QLabel("Source: Not Selected")
        self.select_source_btn = QPushButton("Select Files/Folders")
        self.file_list = QListWidget()
        self.select_source_btn.clicked.connect(self.select_source)
        self.source_panel.addWidget(self.source_label)
        self.source_panel.addWidget(self.select_source_btn)
        self.source_panel.addWidget(self.file_list)
        
        self.dest_panel = QVBoxLayout()
        self.dest_label = QLabel("Destination: Not Selected")
        self.select_dest_btn = QPushButton("Select Destination Folder")
        self.progress = QProgressBar()
        
        self.start_transfer_btn = QPushButton("Start Transfer")
        self.pause_btn = QPushButton("Pause")
        self.resume_btn = QPushButton("Resume")
        
        self.update_button_style(self.start_transfer_btn, "green")
        self.update_button_style(self.pause_btn, "orange")
        self.update_button_style(self.resume_btn, "blue")
        
        self.select_dest_btn.clicked.connect(self.select_destination)
        self.start_transfer_btn.clicked.connect(self.start_transfer)
        self.pause_btn.clicked.connect(self.pause_transfer)
        self.resume_btn.clicked.connect(self.resume_transfer)
        
        self.dest_panel.addWidget(self.dest_label)
        self.dest_panel.addWidget(self.select_dest_btn)
        self.dest_panel.addWidget(self.progress)
        self.dest_panel.addWidget(self.start_transfer_btn)
        self.dest_panel.addWidget(self.pause_btn)
        self.dest_panel.addWidget(self.resume_btn)
        
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
        
        self.copy_thread = FileCopyThread(self.source_files, self.dest_folder)
        self.copy_thread.progress_signal.connect(self.progress.setValue)
        self.copy_thread.status_signal.connect(lambda status: QMessageBox.information(self, "Success", "File transfer completed!"))
        self.copy_thread.start()
    
    def pause_transfer(self):
        if self.copy_thread:
            self.copy_thread.paused = True
            self.update_button_style(self.pause_btn, "darkorange")
    
    def resume_transfer(self):
        if self.copy_thread:
            self.copy_thread.paused = False
            self.update_button_style(self.resume_btn, "darkblue")
    
    def update_button_style(self, button, color):
        button.setStyleSheet(f"background-color: {color}; color: white;")
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileTransferTool()
    window.show()
    sys.exit(app.exec_())
