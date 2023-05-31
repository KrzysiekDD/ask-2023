import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QLineEdit, QPushButton, QHBoxLayout, QBoxLayout,\
    QGridLayout, QLabel, QSizePolicy
from PySide6.QtGui import QPixmap, QPainter, QColor
from PySide6.QtCore import QTimer
from PySide6.QtCore import Qt
import random
import numpy as np


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login to monitoring system")
        self.setGeometry(0, 0, 800, 600)
        self.init_ui()

    def init_ui(self):
        self.main_layout = QGridLayout()

        self.username_label = QLabel("Please enter your operators' username:")
        self.password_label = QLabel("Please enter your operators' password:")
        self.start_label = QLabel("Start the system. Attention: you will be prompted \nfor presence while the system is"
                                  " working!")

        self.credentials_username_input = QLineEdit()
        self.credentials_password_input = QLineEdit()
        self.credentials_password_input.setEchoMode(QLineEdit.Password)
        self.start_system_button = QPushButton("Start Monitoring System")
        self.start_system_button.clicked.connect(self.start_monitoring_system)


        self.main_layout.addWidget(self.username_label, 0, 0)
        self.main_layout.addWidget(self.password_label, 1, 0)
        self.main_layout.addWidget(self.start_label, 2, 0)
        self.main_layout.addWidget(self.credentials_username_input, 0, 1)
        self.main_layout.addWidget(self.credentials_password_input, 1, 1)
        self.main_layout.addWidget(self.start_system_button, 2, 1)


        self.main_widget = QWidget()
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

    def start_monitoring_system(self):
        self.monitoring_system = MonitoringWidget((str(self.credentials_username_input.text()),
                                                   str(self.credentials_password_input.text())))
        self.monitoring_system.show()


class MonitoringWidget(QWidget):
    def __init__(self, operator_credentials: tuple[str, str]):
        super().__init__()
        self.setWindowTitle("Monitoring system")
        self.showMaximized()
        self.operator_credentials = operator_credentials
        self.temperature_change = random.random() * 3.
        self.current_ph = 4.8
        self.process_info = f"<b>Last temperature change</b>: {self.temperature_change}<br>" \
                            f"<b>Current pH level</b>: {self.current_ph}"
        self.temperature = 66.5
        self.current_kind = "Pale Ale"
        self.beer_kind_characteristics = {
            "Pale Ale": "A well-balanced beer with moderate hop bitterness, fruity esters, and a clean malt profile.",
            "India Pale Ale": "An IPA with pronounced hop bitterness, intense hop aroma, and a dry finish.",
            "Pilsner": "A clean and crisp beer with a pale color, mild hop bitterness, and a smooth malt character.",
            "Weissbier": "A refreshing wheat beer with banana and clove esters, often exhibiting fruity and spicy notes.",
            "Grodziskie": "A light-bodied, highly carbonated beer with a pronounced smoky flavor."
        }
        self.information = f"<b>Current temperature</b>: <u>{self.temperature}</u><br><br>"\
                           f"<b>Current kind of beer</b>: <i>{self.current_kind}</i><br><br>"\
                           f"<b>Characteristics</b>: {self.beer_kind_characteristics[self.current_kind]}"
        self.brew_color_r = 134
        self.brew_color_g = 134
        self.brew_color_b = 0
        self.brew_color = QColor(self.brew_color_r, self.brew_color_g, self.brew_color_b)
        self.init_ui()

        self.repainting_timer = QTimer()
        self.repainting_timer.timeout.connect(self.update_process)
        self.repainting_timer.start(1000)

        self.attention_timer = QTimer()
        self.attention_timer.timeout.connect(self.attention_check)
        self.attention_timer.start(random.randint(15, 20)*1000)

    def init_ui(self):
        self.main_layout = QGridLayout()

        self.operator_credentials_label = QLabel(f"Today's operator: {self.operator_credentials[0]}")
        self.operator_credentials_label.setWordWrap(True)
        self.title_label = QLabel("Welcome to Krzysztof and Krzysztof Brewery!")
        font = self.title_label.font()
        font.setPointSize(19)
        font.setBold(True)
        self.title_label.setFont(font)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.process_label = QLabel(self.process_info)
        self.process_label.setWordWrap(True)
        self.control_button_one = QPushButton("Control button 1")
        self.control_button_two = QPushButton("Control button 2")
        self.control_button_one.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.control_button_two.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.instructions_label = QLabel("Control button 1 ups the temperature of the brewing process, while the"
                                         " Control button 2 lowers the temperature. Current temperature (in Celsius)"
                                         ", kind of beer being brewed as well as it's characteristics are displayed"
                                         "under the brewing container.")
        self.instructions_label.setWordWrap(True)

        self.pixmap_label = QLabel()
        self.pixmap = QPixmap("cylinder.png")
        self.pixmap_label.setPixmap(self.pixmap)

        self.information_label = QLabel(self.information)
        self.information_label.setWordWrap(True)

        self.main_layout.addWidget(self.operator_credentials_label, 0, 0)
        self.main_layout.addWidget(self.title_label, 0, 1)
        self.main_layout.addWidget(self.process_label, 0, 2)
        self.main_layout.addWidget(self.control_button_one, 1, 0)
        self.main_layout.addWidget(self.control_button_two, 1, 1)
        self.main_layout.addWidget(self.instructions_label, 2, 0, 1, 2)
        self.main_layout.addWidget(self.pixmap_label, 1, 2)
        self.main_layout.addWidget(self.information_label, 2, 2)

        self.control_button_one.clicked.connect(self.up_temperature)
        self.control_button_two.clicked.connect(self.lower_temperature)

        self.setLayout(self.main_layout)
        self.show()

    def up_temperature(self):
        self.temperature += 0.7

    def lower_temperature(self):
        self.temperature -= 0.7

    def update_process(self):
        pixmap_copy = self.pixmap.copy()
        painter = QPainter(pixmap_copy)

        subset_x = 79
        subset_y = 158
        subset_width = 382
        subset_height = 407

        inner_x = 233
        inner_y = 326
        inner_width = 80
        inner_height = 32

        for y in range(subset_y, subset_y + subset_height):
            for x in range(subset_x, subset_x + subset_width):
                if inner_x <= x < inner_x + inner_width and inner_y <= y < inner_y + inner_height:
                    continue

                painter.setPen(self.brew_color)
                painter.drawPoint(x, y)

        painter.end()

        self.pixmap_label.setPixmap(pixmap_copy)
        self.update_temperature()
        self.check_for_error()
        self.update_info()

    def update_info(self):
        process_parameters = f"<b>Last temperature change</b>: {self.temperature_change}<br>" \
                            f"<b>Current pH level</b>: {self.current_ph}"

        information = f"<b>Current temperature</b>: <u>{self.temperature}</u><br><br>"\
                       f"<b>Current kind of beer</b>: <i>{self.current_kind}</i><br><br>"\
                       f"<b>Characteristics</b>: {self.beer_kind_characteristics[self.current_kind]}"

        self.process_label.setText(process_parameters)
        self.information_label.setText(information)

    def update_temperature(self):
        noise = np.random.normal(0, 1)
        if self.temperature > 65.:
            temperature_change = (100 - self.temperature)/20. + noise
        else:
            temperature_change = (self.temperature - 65)/24. + noise

        ph_change = 0.05 * temperature_change

        self.brew_color_r = 134 + 121 * self.temperature / 100.
        self.brew_color_g = 134 + 121 * self.temperature / 100.
        self.brew_color_b = 0 + 121 * self.temperature / 100.
        self.brew_color = QColor(int(self.brew_color_r), int(self.brew_color_g), int(self.brew_color_b))

        self.temperature_change = temperature_change
        self.temperature += temperature_change
        self.current_ph += ph_change

        if 64. < self.temperature < 70. and 4.8 < self.current_ph < 5.8:
            self.current_kind = "Grodziskie"
        elif 40. < self.temperature < 100. and 4.0 < self.current_ph < 4.8:
            self.current_kind = "Weissbier"
        elif 70. < self.temperature < 100. and 4.8 < self.current_ph < 5.8:
            self.current_kind = "Pale Ale"
        elif 40. < self.temperature < 64. and 4.0 < self.current_ph < 4.8:
            self.current_kind = "India Pale Ale"
        elif 70. < self.temperature < 100. and 2.4 < self.current_ph < 4.0:
            self.current_kind = "Pilsner"

    def attention_check(self):
        self.attention_widget = AttentionWidget()
        self.attention_widget.show()

    def check_for_error(self):
        if self.temperature < 0. or self.temperature > 100.:
            self.repainting_timer.stop()
            self.attention_timer.stop()
            self.error_widget = ErrorWidget(self.temperature, self.current_ph, True)
            self.error_widget.show()
        if self.current_ph < 2.4 or self.current_ph > 5.8:
            self.repainting_timer.stop()
            self.attention_timer.stop()
            self.error_widget = ErrorWidget(self.temperature, self.current_ph, False)
            self.error_widget.show()


class AttentionWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(int((1920 - 400) / 2), int((1080 - 300) / 2), 400, 300)
        self.random_key = chr(65 + random.randint(0, 24))
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("background-color: yellow;")
        self.main_layout = QHBoxLayout()

        self.attention_label = QLabel(f"<html><body><p style='font-size: 20px; text-align: center;'>"
                                      f"<b>ATTENTION ATTENTION ATTENTION</b><br>"
                                      f"This is a routine attention check. Please enter '{self.random_key}' to return "
                                      f"to the brewery!"
                                      "</p></body></html>")
        self.attention_label.setAlignment(Qt.AlignCenter)

        self.main_layout.addWidget(self.attention_label)
        self.setLayout(self.main_layout)
        self.show()

    def keyPressEvent(self, event):
        key = event.key()
        key_str = event.text().upper()
        if key_str == self.random_key:
            self.close()


class ErrorWidget(QWidget):
    def __init__(self, temperature, ph, from_temperature):
        super().__init__()
        self.setGeometry(int((1920 - 800) / 2), int((1080 - 600) / 2), 800, 600)
        self.temperature = temperature
        self.ph = ph
        self.from_temperature = from_temperature
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("background-color: red;")
        self.main_layout = QHBoxLayout()
        if self.from_temperature:
            self.disclaimer_label = QLabel(f"<html><body><p style='font-size: 20px; text-align: center;'>"
                                           f"<b>Critical temperature exceeded! ({self.temperature} Celsius)</b><br>"
                                           f"The factory has to shut down. Good luck with repairing the brewery ;)<br>"
                                           f"(Press any key to close the simulation)"
                                           "</p></body></html>")
        else:
            self.disclaimer_label = QLabel(f"<html><body><p style='font-size: 20px; text-align: center;'>"
                                           f"<b>Critical ph level exceeded! ({self.ph} Celsius)</b><br>"
                                           f"Your beer tastes bad and your name is ruined! You have to start over.<br>"
                                           f"(Press any key to close the simulation)"
                                           "</p></body></html>")
        self.disclaimer_label.setAlignment(Qt.AlignCenter)

        self.main_layout.addWidget(self.disclaimer_label)
        self.setLayout(self.main_layout)
        self.show()

    def keyPressEvent(self, event):
        self.close()

    def closeEvent(self, event):
        QApplication.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())
