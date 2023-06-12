from xml.dom import minidom

from PySide6.QtWidgets import QWidget, QGraphicsPixmapItem, QGraphicsView, QGraphicsScene, QGraphicsSceneMouseEvent,\
    QVBoxLayout, QGraphicsRectItem, QHBoxLayout, QGridLayout, QPushButton, QSizePolicy, QLayout, QLabel
from PySide6.QtCore import QTimer, Qt, QSize, QRect, QEvent
from PySide6.QtGui import QKeyEvent, QPixmap, QBrush, QColor, QKeyEvent, QTransform, QIcon, QPalette, QPainter
import networkx as nx
import numpy as np
import random
import resources_rc
from bomberman_objects import PlayerPixmapItem, UnbreakableWall, OneBombWall, TwoBombWall, BombPixmapItem, \
    StaticEnemy, PatrollingEnemy, FollowingEnemy, EnemyPixmapItem, WallPixmapItem,\
    BackgroundPixmapItem, Board, ExplosionPixmapItem
from utils import print_graph_to_stdo
import json
import sqlite3
import xml.etree.ElementTree as ET
import pandas as pd
import datetime
import random
random.seed(0)


class GameWidget(QWidget):
    def __init__(self, board_width: int, board_height: int, unbreakable_wall_density: float,
                 one_bomb_wall_density: float,
                 two_bomb_wall_density: float):
        """
        Widget displaying the proper game. Left side of this widget is reserved for the
        GameView, and on the right side the user can choose from a number of powerups that strengthen
        the player.
        :param board_width: Width of the board
        :param board_height: Height of the board
        """
        super().__init__()
        self.showMaximized()
        self.setWindowTitle("Endless Mode")
        self.board_width: int = board_width
        self.board_height: int = board_height

        self.game_layout: QHBoxLayout = QHBoxLayout()

        self.view: GameView = GameView(self.board_width, self.board_height, unbreakable_wall_density,
                                       one_bomb_wall_density, two_bomb_wall_density)
        self.view.setMinimumWidth(self.board_width*16)
        # self.view.setMinimumWidth((1280))

        self.game_layout.addWidget(self.view)

        self.powerup_widget: QWidget = QWidget()
        self.powerup_widget.setMaximumWidth(640)
        self.powerup_layout: QGridLayout = QGridLayout()
        self.powerup_widget.setLayout(self.powerup_layout)

        powerup_images = [
            ":/sprites/bombs_sprite.png",
            ":/sprites/flames_sprite.png",
            ":/sprites/speed_sprite.png",
            ":/sprites/wallpass_sprite.png",
            ":/sprites/detonator_sprite.png",
            ":/sprites/bombpass_sprite.png",
            ":/sprites/flamepass_sprite.png",
            ":/sprites/mystery_sprite.png",
        ]

        # Construct the clickable powerups, unfortunately QPushButton would not work no matter what
        # so a workaround using QLabel had to be implemented
        for i in range(4):
            for j in range(2):
                pixmap = QPixmap(powerup_images[i * 2 + j]).scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                powerup_label = PowerupLabel(pixmap)
                powerup_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                powerup_label.mousePressEvent = lambda event, i_=i, j_=j: self.on_powerup_click(i_, j_)

                self.powerup_layout.addWidget(powerup_label, i, j)

        self.powerup_layout.setHorizontalSpacing(0)
        self.powerup_layout.setVerticalSpacing(0)
        self.powerup_layout.setContentsMargins(0, 0, 0, 0)
        self.powerup_layout.setSizeConstraint(QLayout.SetMinimumSize)

        self.game_layout.addWidget(self.powerup_widget)

        self.setLayout(self.game_layout)
        self.show()

    def on_powerup_click(self, row: int, col: int) -> None:
        """
         Activates the powerup based on which powerup has been clicked
        :param row: Row ID in the QGridLayout of the chosen powerup
        :param col: Column ID in the QGridLayout of the chosen powerup
        :return:
        """
        match row * 2 + col:
            case 0:
                # bombs powerup, increments the number of bombs the player can hold by 1
                self.view.scene.player.num_of_bombs += 1
            case 1:
                # flames powerup, extends the range of the bomb by 1 in every direction
                self.view.scene.player.bomb_range += 1
            case 2:
                # speed powerup, raises the player's speed
                self.view.scene.player.speed += 4
            case 3:
                # wallpass, allows the player to move through walls
                self.view.scene.player.active_powerups.append("wallpass")
            case 4:
                # detonator, instead of bombs exploding after given time, they can be manually
                # activated by clicking 'd' Qt.Key_D
                self.view.scene.player.active_powerups.append("detonator")
            case 5:
                # bombpass, allows the player to pass through bombs
                self.view.scene.player.active_powerups.append("bombpass")
            case 6:
                # flamepass, allows the player to move through explosions (gives immunity to them)
                self.view.scene.player.active_powerups.append("flamepass")
            case 7:
                # mystery, gives invicibility from everything, basically it is bombpass and flamepass bundled together
                self.view.scene.player.active_powerups.append("flamepass")
                self.view.scene.player.active_powerups.append("bombpass")


class GameView(QGraphicsView):
    def __init__(self, board_width: int, board_height: int, unbreakable_wall_density: float,
                 one_bomb_wall_density: float, two_bomb_wall_density: float):
        """
        GameView object inheriting from QGraphicsView. Contains the GameScene.
        :param board_width: Width of the board
        :param board_height: Height of the board
        :param unbreakable_wall_density: Percentage of unbreakable walls
        :param one_bomb_wall_density: Percentage of one-bomb walls
        :param two_bomb_wall_density: Percentage of two-bomb walls
        """
        super().__init__()
        self.board_width: int = board_width
        self.board_height: int = board_height
        self.scene: GameScene = GameScene(self.board_width, self.board_height, unbreakable_wall_density,
                                          one_bomb_wall_density, two_bomb_wall_density)
        self.setSceneRect(0, 0, 1280, 1280)
        self.setSceneRect(0, 0, self.board_width * 16, self.board_height * 16)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.setScene(self.scene)

        self.centerOn(0, 0)


class GameScene(QGraphicsScene):
    def __init__(self, board_width: int, board_height: int, unbreakable_wall_density: float,
                 one_bomb_wall_density: float, two_bomb_wall_density: float):
        """
        GameScene object inheriting from QGraphicsScene. Contains all the logic related to
        player's actions and enemy movement.
        :param board_width: Width of the board
        :param board_height: Height of the board
        :param unbreakable_wall_density: Percentage of unbreakable walls
        :param one_bomb_wall_density: Percentage of one-bomb walls
        :param two_bomb_wall_density: Percentage of two-bomb walls
        """
        super().__init__()
        self.board_width: int = board_width
        self.board_height: int = board_height
        self.one_bomb_wall_density: float = one_bomb_wall_density
        self.two_bomb_wall_density: float = two_bomb_wall_density
        self.unbreakable_wall_density: float = unbreakable_wall_density
        self.cell_size: int = 16
        self.setSceneRect(0, 0, 1280, 1280)

        self.board: Board = Board(self.board_width, self.board_height)

        self.occupied_pos: list[tuple[int, int]] = [(0, 0), (self.board_height - 1, 0),
                                                    (0, self.board_width - 1),
                                                    (self.board_height - 1, self.board_width - 1)]
        self.player: PlayerPixmapItem
        self.enemies: list[EnemyPixmapItem] = []
        self.unbreakable_walls: list[WallPixmapItem] = []
        self.one_bomb_walls: list[WallPixmapItem] = []
        self.two_bomb_walls: list[WallPixmapItem] = []
        self.explosion_squares: list[ExplosionPixmapItem] = []

        self.init_scene()

        self.conn = sqlite3.connect("game_history.db")
        self.cursor = self.conn.cursor()


        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_scene)
        self.timer.start(1000)  # Once every second

    def init_scene(self) -> None:
        """
         Initialize the board, add walls, enemies and the player and set their positions.
        :return:
        """
        self.player: PlayerPixmapItem = PlayerPixmapItem(0, 0)
        self.addItem(self.player)

        # Initialize the background, green 16 x 16 squares
        for x in range(self.board_height):
            for y in range(self.board_width):
                background: BackgroundPixmapItem = BackgroundPixmapItem(x * self.cell_size, y * self.cell_size)
                self.addItem(background)

        # Initialize unbreakable walls
        for i in range(int(self.board_width * self.board_height * self.unbreakable_wall_density)):
            while True:
                x_pos = random.randint(0, self.board_width - 1)
                y_pos = random.randint(0, self.board_height - 1)
                if (x_pos, y_pos) not in self.occupied_pos:
                    break

            self.occupied_pos.append((x_pos, y_pos))
            self.board.add_wall(x_pos, y_pos)
            unbreakable_wall: UnbreakableWall = UnbreakableWall(y_pos * self.cell_size, # this works, from graph to scene
                                                                                    x_pos * self.cell_size) # and from scene to graph the coords have to be swapped
            self.addItem(unbreakable_wall)
            self.unbreakable_walls.append(unbreakable_wall)

        # Initialize one-bomb walls
        for i in range(int(self.board_width * self.board_height * self.one_bomb_wall_density)):
            while True:
                x_pos = random.randint(0, self.board_width - 1)
                y_pos = random.randint(0, self.board_height - 1)
                if (x_pos, y_pos) not in self.occupied_pos:
                    break

            self.occupied_pos.append((x_pos, y_pos))
            self.board.add_wall(x_pos, y_pos)
            one_bomb_wall: OneBombWall = OneBombWall(y_pos * self.cell_size,
                                         x_pos * self.cell_size)
            self.addItem(one_bomb_wall)
            self.one_bomb_walls.append(one_bomb_wall)

        # Initialize two-bomb walls
        for i in range(int(self.board_width * self.board_height * self.two_bomb_wall_density)):
            while True:
                x_pos = random.randint(0, self.board_width - 1)
                y_pos = random.randint(0, self.board_height - 1)
                if (x_pos, y_pos) not in self.occupied_pos:
                    break

            self.occupied_pos.append((x_pos, y_pos))
            self.board.add_wall(x_pos, y_pos)
            two_bomb_wall: TwoBombWall = TwoBombWall(y_pos * self.cell_size,
                                         x_pos * self.cell_size)
            self.addItem(two_bomb_wall)
            self.one_bomb_walls.append(two_bomb_wall)

        # Initialize enemies
        num_of_walls: int = len(self.unbreakable_walls) + len(self.one_bomb_walls) + len(self.two_bomb_walls)
        # Heuristically chosen number of enemies
        num_of_enemies: int = max(1, int(round(self.board_width * self.board_height - num_of_walls - 1) /
                                         (self.board_width + self.board_height) * 2))

        for i in range(num_of_enemies):
            while True:
                x_pos = random.randint(0, self.board_width - 1)
                y_pos = random.randint(0, self.board_height - 1)
                if (x_pos, y_pos) not in self.occupied_pos:
                    break

            enemy_type: int = random.randint(0, 2)
            enemy_speed: int = random.choice([1, 2, 4])

            match enemy_type:
                case 0:
                    static_enemy = StaticEnemy(y_pos * self.cell_size,
                                         x_pos * self.cell_size)
                    self.addItem(static_enemy)
                    self.enemies.append(static_enemy)

                case 1:
                    patrolling_enemy = PatrollingEnemy(enemy_speed, y_pos * self.cell_size,
                                               x_pos * self.cell_size)
                    self.addItem(patrolling_enemy)
                    self.enemies.append(patrolling_enemy)

                case 2:
                    following_enemy = FollowingEnemy(self.board, self.player, enemy_speed, y_pos * self.cell_size,
                                                       x_pos * self.cell_size)
                    self.addItem(following_enemy)
                    self.enemies.append(following_enemy)

    def update_scene(self) -> None:
        """
        Method for handling enemy movement, called on every QTimer timeout.
        :return:
        """
        game_state: list[dict] = []

        self.cursor.execute("CREATE TABLE IF NOT EXISTS enemy (timestamp DATE, type TEXT, x_pos FLOAT, y_pos FLOAT, "
                       "speed INTEGER, orientation TEXT);")

        for enemy in self.enemies:
            enemy.move()
            enemy_dict: dict = {
                "timestamp": datetime.datetime.now(),
                "type": enemy.type(),
                "x_pos": enemy.pos().x(),
                "y_pos": enemy.pos().y(),
                "speed": enemy.speed,
                "orientation": enemy.orientation
            }
            # for key, value in vars(enemy).items():
            #     enemy_dict[key] = value
            game_state.append(enemy_dict)

        for row in game_state:
            self.cursor.execute("INSERT INTO enemy (timestamp, type, x_pos, y_pos, speed, orientation) VALUES (?, ?, ?, ?, ?, ?)",
                           (tuple(row.values())))

        self.conn.commit()

        root = ET.Element("enemy")

        for row in game_state:
            enemy = ET.SubElement(root, "enemy")
            for key, value in row.items():
                element = ET.SubElement(enemy, key)
                element.text = str(value)

        xml_string = ET.tostring(root, encoding="utf-8")
        xml_pretty = minidom.parseString(xml_string).toprettyxml(indent="  ")

        with open("game_history.xml", "w") as xml_file:
            xml_file.write(xml_pretty)

        if self.player.autopilot:
            self.player_autopilot_move()

    def obtain_state(self) -> tuple[tuple[int, int], int, bool]:
        """ Returns the current state of the game for the purpose of DQN """
        reward = -1
        is_done = False

        return self.player.pos().x()//16, self.player.pos().y()//16, reward, is_done

    def keyPressEvent(self, event: QKeyEvent) -> None:
        """
        Overriden QGraphicsScene method for handling keyboard input.
        :param event: Key event
        :return:
        """
        if event.key() in {Qt.Key_Up, Qt.Key_Down, Qt.Key_Left, Qt.Key_Right}:
            self.player.autopilot = False
            self.player.move(event)
            self.cursor.execute("INSERT INTO enemy (timestamp, type, x_pos, y_pos, speed, orientation) VALUES (?, ?, ?, ?, ?, ?)",
                           (datetime.datetime.now(), "player", self.player.pos().x(), self.player.pos().y(), self.player.speed,
                            self.player.current_direction))
        elif event.key() == Qt.Key_Space and self.player.num_of_bombs > 0:
            self.player.autopilot = False
            self.plant_bomb()

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        """
        Overriden QGraphicsScene method for handling mouse input. The player moves along the found path
        when a cell is pressed on the board.
        :param event: Mouse event
        :return:
        """
        if event.button() == Qt.LeftButton:
            position_in_scene = event.scenePos()
            x_pos, y_pos = position_in_scene.x() // 16, position_in_scene.y() // 16
            self.player.destination = (y_pos, x_pos)

            self.player.autopilot = True

    def player_autopilot_move(self) -> None:
        """
         One step in the direction of the clicked position. Utilizes pretty much the same algorithms
         as the ones used for the following enemies.
        :return:
        """
        current_position = (self.player.pos().x(), self.player.pos().y())

        if (current_position[0] % 16) != 0 or (current_position[1] % 16) != 0:
            if self.player.autopilot_last_visited_node is not None and self.player.last_direction is not None:
                self.player.moveBy(self.player.last_direction[0], self.player.last_direction[1])
                self.player.movement_cycle = (self.player.movement_cycle + 1) % (
                    len(self.player.player_sprites[self.player.current_direction]))
            return

        current_node = (int(self.player.pos().y() // 16), int(self.player.pos().x() // 16))

        try:
            shortest_path = nx.shortest_path(self.board.underlying_graph, source=current_node,
                                             target=self.player.destination)

            if len(shortest_path) == 1:
                self.player.autopilot = False
                return

            next_node = shortest_path[1]
            target_position = (next_node[1] * 16, next_node[0] * 16)
            direction = np.array(target_position) - np.array(current_position)

            if abs(direction[0]) > abs(direction[1]):
                self.player.current_direction = 'right' if direction[0] > 0 else 'left'
                move_by = (np.sign(direction[0]) * self.player.speed, 0)
            else:
                self.player.current_direction = 'down' if direction[1] > 0 else 'up'
                move_by = (0, np.sign(direction[1]) * self.player.speed)

            self.player.autopilot_last_visited_node = current_node
            self.player.last_direction = move_by
            self.player.moveBy(move_by[0], move_by[1])

            self.player.movement_cycle = (self.player.movement_cycle + 1) % (
                        len(self.player.player_sprites[self.player.current_direction]))
            print(self.player.movement_cycle)
            self.player.setPixmap(
                self.player.player_sprites[self.player.current_direction][self.player.movement_cycle])

        except (nx.NetworkXNoPath, IndexError):
            return

    def plant_bomb(self) -> None:
        """
        Method called after the user has pressed 'space'
        :return:
        """
        x_pos, y_pos = self.player.pos().x() // self.cell_size * self.cell_size, \
                       self.player.pos().y() // self.cell_size * self.cell_size
        bomb: BombPixmapItem = BombPixmapItem(self.player, x_pos, y_pos)
        self.addItem(bomb)
        self.player.num_of_bombs -= 1

        QTimer.singleShot(2500, lambda: self.explosion(bomb))

    def explosion(self, bomb: BombPixmapItem) -> None:
        """
        Method handling the bomb's existence and disappearance. Checks for directions in which
        the bomb can explode and stops the explosion if a wall is encountered
        :param bomb: Planted bomb
        :return:
        """
        x_pos, y_pos = bomb.pos().x() // self.cell_size, bomb.pos().y() // self.cell_size

        self.removeItem(bomb)
        print_graph_to_stdo(self.board.underlying_graph)
        print("\n")
        self.add_explosion_item(x_pos, y_pos)

        for direction in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            for r in range(1, bomb.range + 1):
                new_x, new_y = x_pos + direction[0] * r, y_pos + direction[1] * r
                if not self.smart_explosion(new_x, new_y):
                    break

        QTimer.singleShot(500, lambda: self.remove_explosion_items(self.explosion_squares))

        self.player.num_of_bombs += 1

    def smart_explosion(self, x, y) -> bool:
        """
        Helper function making sure the items are removed properly from the scene and the underlying
        graph is updated correctly
        :param x: X position of the explosion
        :param y: Y position of the explosion
        :return:
        """
        item = self.itemAt(x * self.cell_size, y * self.cell_size, QTransform())
        if isinstance(item, UnbreakableWall):
            return False
        elif isinstance(item, TwoBombWall):
            item.wall_hp -= 1
            if item.wall_hp == 1:
                item.setPixmap(QPixmap(":/sprites/one_bomb_wall_sprite.png"))
            else:
                self.removeItem(item)
                self.board.remove_wall(x, y)
            self.add_explosion_item(x, y)
            return False
        elif isinstance(item, OneBombWall):
            self.removeItem(item)
            self.board.remove_wall(x, y)
            self.add_explosion_item(x, y)
            return False
        elif isinstance(item, EnemyPixmapItem):
            self.removeItem(item)
            self.board.remove_wall(x, y)
            self.add_explosion_item(x, y)
            return True
        else:
            self.add_explosion_item(x, y)
            return True

    def add_explosion_item(self, x, y) -> None:
        """
        Adds an explosion item to the scene at the given position
        :param x: x coordinate on the GameScene of the item
        :param y: y coordinate on the GameScene of the item
        :return:
        """
        explosion_square = ExplosionPixmapItem(x * self.cell_size, y * self.cell_size)
        self.addItem(explosion_square)
        self.explosion_squares.append(explosion_square)

    def remove_explosion_items(self, explosion_squares) -> None:
        """
        Removes the explosion items after 0.5 seconds has passed
        :param explosion_squares: List of explosion items being displayed on the scene
        :return:
        """
        for square in explosion_squares:
            self.removeItem(square)

    def get_current_game_state(self) -> pd.DataFrame:
        """ Returns the current state of the game to be saved """
        ...

    def __del__(self) -> None:
        self.conn.close()


class PowerupLabel(QLabel):
    def __init__(self, pixmap: QPixmap):
        """
        Clickable label displaying a powerup for the user to choose.
        :param pixmap: Sprite of the powerup that will be activated after clicking this label
        """
        super().__init__()
        self.setPixmap(pixmap)
        self.setScaledContents(True)


class PlaybackWidget(QWidget):
    def __init__(self):
        super().__init__()
