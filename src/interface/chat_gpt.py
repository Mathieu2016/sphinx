import pyaudio
import wave

from gtts import gTTS
from playsound import playsound

from PyQt5.QtCore import Qt, QEasingCurve
from PyQt5.QtCore import pyqtSignal, QThread
from PyQt5.QtWidgets import QWidget, QTextEdit, QGridLayout, QFrame, QPushButton, QLabel

from qfluentwidgets import (PrimaryPushButton, FluentIcon, StateToolTip, TextEdit, LineEdit, InfoBar, InfoBarPosition,
                            FlowLayout, ScrollArea, ComboBox)

from ai.oa_whisper import transcribe
from ai.oa_chat_gpt import ChatGptThread


class ChatGpt(QWidget):
    complete_record = pyqtSignal(bool)
    send_gpt_message = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.state_tooltip = None
        self.transcribe_thread = None
        self.record_thread = RecordThread('voice.wav')
        self.chat_gpt_thread = ChatGptThread()
        self.chat_gpt_thread.start()

        self.default_model = 'tiny'

        self.model_select_label = QLabel('请选择Whisper模型:')
        self.model_combo_box = ComboBox()
        self.chat_display_text = ChatDisplayWidget(self)
        self.chat_input_text = TextEdit(self)
        self.chat_layout = QGridLayout(self)
        self.send_push_button = PrimaryPushButton('发送', self, FluentIcon.SEND)
        self.voice_push_button = PrimaryPushButton('语音', self, FluentIcon.MICROPHONE)

        self.recording = False

        self.init_layout()
        self.init_actions()

    def init_layout(self) -> None:
        self.model_combo_box.addItems(['tiny', 'base', 'small', 'medium'])
        self.model_combo_box.setCurrentIndex(0)
        self.model_combo_box.setMinimumWidth(200)

        self.chat_layout.addWidget(self.model_select_label, 0, 0, 1, 1)
        self.chat_layout.addWidget(self.model_combo_box, 0, 1, 1, 1)
        self.chat_layout.addWidget(self.chat_display_text, 1, 0, 5, 8)
        self.chat_layout.addWidget(self.chat_input_text, 7, 0, 3, 8)
        self.chat_layout.addWidget(self.voice_push_button, 10, 6, 1, 1)
        self.chat_layout.addWidget(self.send_push_button, 10, 7, 1, 1)

        self.setLayout(self.chat_layout)

    def init_actions(self) -> None:
        self.voice_push_button.clicked.connect(self.control_record)
        self.complete_record.connect(self.record_thread.stop_record)
        self.send_gpt_message.connect(self.chat_gpt_thread.handle_session)
        self.chat_gpt_thread.session_response.connect(self.handle_chatgpt_response)
        self.send_push_button.clicked.connect(self.start_session)
        self.model_combo_box.currentTextChanged.connect(self.change_model)
        # self.voice_push_button.released.connect(self.handle_record_completed)

    def control_record(self) -> None:
        if not self.recording:
            self.state_tooltip = StateToolTip(
                self.tr('录音中...'), self.tr(''), self.window()
            )
            self.record_thread.start()
            self.state_tooltip.move(self.state_tooltip.getSuitablePos())
            self.state_tooltip.show()
            self.voice_push_button.setText('停止录音')
            self.recording = True
        else:
            self.voice_push_button.setText('开始录音')
            self.handle_record_completed()
            self.recording = False
        self.complete_record.emit(self.recording)

    def handle_record_completed(self) -> None:
        self.transcribe_thread = TranscribeThread('voice.wav', self.default_model)
        self.transcribe_thread.append_text.connect(self.handle_after_transcribe)
        self.state_tooltip.setTitle(self.tr('语音识别中...'))
        self.state_tooltip.setContent(self.tr(''))
        self.transcribe_thread.start()
        # self.chat_input_text.append(transcribe('temp/data_vally.m4a'))

    def handle_after_transcribe(self, text: str) -> None:
        self.chat_input_text.append(text)
        self.state_tooltip.setState(True)
        self.state_tooltip = None

    def start_session(self) -> None:
        self.chat_display_text.layout.addWidget(
            InfoBar(
                icon=FluentIcon.GITHUB,
                title=self.tr('Me'),
                content=self.chat_input_text.toPlainText(),
                orient=Qt.Horizontal,
                isClosable=True,
                duration=-1,
                position=InfoBarPosition.TOP_RIGHT,
                parent=self.chat_display_text
            )
        )
        self.state_tooltip = StateToolTip(
            self.tr('等待ChatGPT响应中...'), self.tr(''), self.window()
        )
        self.state_tooltip.move(self.state_tooltip.getSuitablePos())
        self.state_tooltip.show()
        self.send_gpt_message.emit(self.chat_input_text.toPlainText())
        self.chat_input_text.clear()

    def handle_chatgpt_response(self, response: str) -> None:
        self.state_tooltip.setState(True)
        self.state_tooltip = None
        self.chat_display_text.layout.addWidget(
            InfoBar(
                icon=FluentIcon.FEEDBACK,
                title=self.tr('ChatGPT'),
                content=self.tr(response),
                orient=Qt.Horizontal,
                isClosable=True,
                duration=-1,
                position=InfoBarPosition.NONE,
                parent=self.chat_display_text
            )
        )
        # self.chat_display_text.adjustSize()
        # mp3_fp = BytesIO()
        tts = gTTS(response, lang='zh-CN')
        tts.save('tts.mp3')
        playsound('tts.mp3')
        # tts.write_to_fp(mp3_fp)

    def change_model(self, model: str):
        self.default_model = model


class ChatDisplayWidget(TextEdit):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.layout = FlowLayout(self, needAni=True)
        self.layout.setAnimation(250, QEasingCurve.OutQuad)
        self.layout.setContentsMargins(30, 30, 30, 30)
        self.layout.setVerticalSpacing(20)
        self.layout.setHorizontalSpacing(10)


class TranscribeThread(QThread):
    append_text = pyqtSignal(str)

    def __init__(self, record_file: str, model: str):
        super().__init__()
        self.record_file = record_file
        self.model = model

    def run(self) -> None:
        result = transcribe(self.record_file, self.model)
        self.append_text.emit(result)


class RecordThread(QThread):
    def __init__(self, record_file: str):
        super().__init__()
        self.recording = True
        self.record_file = record_file

    def run(self) -> None:
        frames = []
        truck = 1024
        channels = 1
        formate = pyaudio.paInt16
        rate = 16000

        recorder = pyaudio.PyAudio()
        stream = recorder.open(
            format=formate,
            channels=channels,
            rate=rate,
            input=True,
            frames_per_buffer=truck
        )
        while self.recording:
            frames.append(stream.read(truck))
        stream.stop_stream()
        stream.close()
        recorder.terminate()

        with wave.open(self.record_file, 'wb') as fp:
            fp.setnchannels(channels)
            fp.setsampwidth(recorder.get_sample_size(formate))
            fp.setframerate(rate)
            fp.writeframes(b''.join(frames))

    def stop_record(self, state: bool):
        self.recording = state
