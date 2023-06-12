"""
Main GUI of the game, MainWindow, Widget for setting options before game and instructions/options
Starting a game will be a completely isolated QWidget and scene from the non-game GUI's
"""
from PySide6.QtWidgets import QMainWindow, QWidget, QPushButton, QApplication, QHBoxLayout, QVBoxLayout, QSizePolicy, \
    QGraphicsPixmapItem, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QLineEdit, QSpacerItem, QGroupBox, QLabel,\
    QFormLayout, QRadioButton
from PySide6.QtGui import QPixmap, Qt
# from bomberman_game import GameWidget  # , EndlessModeGame
from bomberman_game import GameWidget, PlaybackWidget
from bomberman_game_ai import ReplayWidget
import json
import sys
import resources_rc


class MainMenuWindow(QMainWindow):
    def __init__(self):
        """
        Main window of the game, inheriting from QMainWindow.
        """
        super().__init__()
        self.setWindowTitle("Bomberman Dymanowski")
        self.showMaximized()
        self.setStyleSheet(f"QMainWindow {{ border-image: url({':/sprites/title_screen_sprite.png'}); }}")

        self.endless_options_widget: EndlessOptionsWidget
        self.init_ui()

    def init_ui(self) -> None:
        """
        Initializes the User Interface layout of the main window of the game.
        :return:
        """
        self.main_layout = QHBoxLayout()

        # Add spacer to push QVBoxLayout to the right
        self.main_layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.menu_layout: QVBoxLayout = QVBoxLayout()
        self.menu_layout.setAlignment(Qt.AlignCenter)

        self.menu_layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.endless_mode_button: QPushButton = QPushButton("Start endless mode!")
        self.endless_mode_button.setMinimumSize(360, 120)
        self.endless_mode_button.clicked.connect(self.start_endless_mode)

        self.options_instructions_button: QPushButton = QPushButton("Instructions")
        self.options_instructions_button.setMinimumSize(360, 120)
        self.options_instructions_button.clicked.connect(self.open_options_instructions)

        self.menu_layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))
        # Add buttons to the main layout
        self.menu_layout.addWidget(self.endless_mode_button)
        self.menu_layout.addWidget(self.options_instructions_button)

        self.main_layout.addLayout(self.menu_layout)
        main_widget: QWidget = QWidget()
        main_widget.setLayout(self.main_layout)
        self.setCentralWidget(main_widget)

    def start_endless_mode(self) ->None:
        """
        First step for starting the game.Opens the widget containing options for
        customizing the game's Board.
        :return:
        """
        self.endless_options_widget = EndlessOptionsWidget()

    def start_playback_mode(self) -> None:
        """
        Start the playback mode, opens the playback widget and allows you to choose from xml, json or sqlite
        :return:
        """
        self.playback_options_widget = PlaybackOptionsWidget()

    def open_options_instructions(self) -> None:
        """ Slot function, opens the instruction widget"""
        self.instructions_widget = InstructionsWidget()
        self.instructions_widget.show()


class EndlessOptionsWidget(QWidget):
    def __init__(self):
        """
        Widget handling the game options before the game is started.
        """
        super().__init__()
        self.layout = QVBoxLayout()
        self.setWindowTitle("Options")
        self.setFixedSize(800, 600)
        self.board_width: int = 20
        self.board_height: int = 20
        self.one_bomb_wall_density: float = 0.15
        self.two_bomb_wall_density: float = 0.15
        self.unbreakable_wall_density: float = 0.05

        # Board size input and button
        self.board_width_input = QLineEdit()
        self.board_height_input = QLineEdit()
        self.size_button = QPushButton("Confirm the board size")
        self.size_button.clicked.connect(self.set_board_size)

        # Density input for wall types
        self.one_bomb_wall_density_input = QLineEdit()
        self.two_bomb_wall_density_input = QLineEdit()
        self.unbreakable_wall_density_input = QLineEdit()
        self.density_button = QPushButton("Confirm wall densities")
        self.density_button.clicked.connect(self.set_wall_densities)

        # Start game button
        self.start_button = QPushButton("Start game")
        self.load_config_button = QPushButton("Load config")
        self.save_config_button = QPushButton("Save config")
        self.start_button.clicked.connect(self.start_game)
        self.load_config_button.clicked.connect(self.load_config)
        self.save_config_button.clicked.connect(self.save_config)

        # Radio button with 3 options
        self.single_player_checkbox = QRadioButton("Single Player")
        self.two_players_checkbox = QRadioButton("Two players")
        self.ai_player_checkbox = QRadioButton("AI player")
        self.ai_player_checkbox.setChecked(True)
        # Two QLineEdit's
        self.ip_line_edit = QLineEdit()
        self.ip_line_edit.setInputMask("000.000.000.000;_")
        self.ip_mask_line_edit = QLineEdit()
        self.ip_mask_line_edit.setInputMask("00000;_")

        # Layout for board size
        board_size_group = QGroupBox("Board size")
        board_size_layout = QFormLayout()
        board_size_layout.addRow("Height:", self.board_width_input)
        board_size_layout.addRow("Width:", self.board_height_input)
        board_size_layout.addWidget(self.size_button)
        board_size_group.setLayout(board_size_layout)

        # Layout for wall densities
        wall_density_group = QGroupBox("Wall densities (in %, please enter a number from 0 to 100)")
        wall_density_layout = QFormLayout()
        wall_density_layout.addRow("One-bomb wall density:", self.one_bomb_wall_density_input)
        wall_density_layout.addRow("Two-bomb wall density:", self.two_bomb_wall_density_input)
        wall_density_layout.addRow("Unbreakable wall density:", self.unbreakable_wall_density_input)
        wall_density_layout.addWidget(self.density_button)
        wall_density_group.setLayout(wall_density_layout)

        # Layout for radio buttons and line edits
        radio_lineedit_group = QGroupBox("Radio Buttons and Line Edits")
        radio_lineedit_layout = QVBoxLayout()
        radio_button_layout = QHBoxLayout()
        radio_button_layout.addWidget(self.single_player_checkbox)
        radio_button_layout.addWidget(self.two_players_checkbox)
        radio_button_layout.addWidget(self.ai_player_checkbox)
        radio_lineedit_layout.addLayout(radio_button_layout)
        radio_lineedit_layout.addWidget(self.ip_line_edit)
        radio_lineedit_layout.addWidget(self.ip_mask_line_edit)
        radio_lineedit_group.setLayout(radio_lineedit_layout)

        # Current settings label
        self.current_settings_label = QLabel()
        self.update_current_settings()

        # Main layout
        self.layout.addWidget(board_size_group)
        self.layout.addWidget(wall_density_group)
        self.layout.addWidget(radio_lineedit_group)
        self.layout.addWidget(self.current_settings_label)
        self.layout.addWidget(self.start_button)
        self.layout.addWidget(self.load_config_button)
        self.layout.addWidget(self.save_config_button)

        self.setLayout(self.layout)
        self.show()

    def set_board_size(self) -> None:
        """
        Confirms the board dimension as inputted by the user.
        :return:
        """
        self.board_height = int(self.board_height_input.text())
        self.board_width = int(self.board_width_input.text())
        self.update_current_settings()

    def set_wall_densities(self) -> None:
        """
        Confirms the wall densities as inputted by the user.
        :return:
        """
        self.one_bomb_wall_density = float(self.one_bomb_wall_density_input.text()) / 100
        self.two_bomb_wall_density = float(self.two_bomb_wall_density_input.text()) / 100
        self.unbreakable_wall_density = float(self.unbreakable_wall_density_input.text()) / 100
        self.update_current_settings()

    def update_current_settings(self) -> None:
        """
         Function displaying the currently chosen setting by the user
        :return:
        """
        current_settings = f"Current settings:\nBoard size: {self.board_width}x{self.board_height} (H x W)\n" \
                           f"One-bomb wall density: {getattr(self, 'one_bomb_wall_density', 'Not set')}\n" \
                           f"Two-bomb wall density: {getattr(self, 'two_bomb_wall_density', 'Not set')}\n" \
                           f"Unbreakable wall density: {getattr(self, 'unbreakable_wall_density', 'Not set')}"
        self.current_settings_label.setText(current_settings)

    def start_game(self) -> None:
        """
         Slot function that starts the proper gameplay
        :return:
        """
        if self.single_player_checkbox.isChecked():
            self.game_widget = GameWidget(self.board_width, self.board_height,
                                          self.unbreakable_wall_density,
                                          self.one_bomb_wall_density,
                                          self.two_bomb_wall_density)
        elif self.ai_player_checkbox.isChecked():
            self.replay_widget = ReplayWidget(self.board_width, self.board_height,
                                              self.unbreakable_wall_density,
                                              self.one_bomb_wall_density,
                                              self.two_bomb_wall_density)

    def load_config(self) -> None:
        with open("config.json", 'r') as f:
            config_dict = json.load(f)

        self.board_width = config_dict["board_width"]
        self.board_height = config_dict["board_height"]
        self.unbreakable_wall_density = config_dict["unbreakable_wall_density"]
        self.one_bomb_wall_density = config_dict["one_bomb_wall_density"]
        self.two_bomb_wall_density = config_dict["two_bomb_wall_density"]
        self.update_current_settings()

    def save_config(self) -> None:
        config_dict: dict = {
            "board_width": self.board_width,
            "board_height": self.board_height,
            "unbreakable_wall_density": self.unbreakable_wall_density,
            "one_bomb_wall_density": self.one_bomb_wall_density,
            "two_bomb_wall_density": self.two_bomb_wall_density
        }

        with open("config.json", 'w') as f:
            json.dump(config_dict, f)


class PlaybackOptionsWidget(QWidget):
    def __init__(self):
        super().__init__()

    def start_playback(self) -> None:
        self.playback_widget = PlaybackWidget()


class InstructionsWidget(QWidget):
    def __init__(self):
        """
        Widget displaying brief information about the game.
        """
        super().__init__()
        self.setWindowTitle("Options and Instructions")
        self.setFixedSize(800, 600)

        self.layout = QVBoxLayout()

        self.instructions_label = QLabel("Welcome to my NES Bomberman (1985) knock-off written in Python!\n\n"
                                         "After pressing 'Start Endless Mode!' an option window will open"
                                         "in which you can customize the boards width, height and densities of"
                                         "each type of wall in the game.\n\n")
        self.instructions_label.setWordWrap(True)
        self.instructions_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.close)

        self.layout.addWidget(self.instructions_label)
        self.layout.addWidget(self.close_button, alignment=Qt.AlignRight)

        self.setLayout(self.layout)
