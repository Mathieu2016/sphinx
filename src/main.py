import whisper
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

from interface.main_window import MainWindow


def transcribe(audio_file: str) -> dict:
    model = whisper.load_model('medium')

    return model.transcribe(audio_file)


if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec_()
