import random

from PySide6.QtWidgets import QGraphicsPixmapItem, QGraphicsItem
from PySide6.QtCore import QTimer, Qt, QPointF
from PySide6.QtGui import QPixmap, QKeyEvent, QTransform
import networkx as nx
import numpy as np
import math
import resources_rc


class Powerup:
    def __init__(self):
        ...


class Board:
    def __init__(self, board_width: int, board_height: int):
        """
        Board is the logic layer behind the GameScene, it's most important property is the underlying graph,
        a grid_2d_graph from the networkx library that allows the player and the enemies to perform pathfinding
        tasks
        :param board_width: Width of the board
        :param board_height: Height of the board
        """
        super().__init__()
        self.board_width = board_width
        self.board_height = board_height
        self.underlying_graph = nx.grid_2d_graph(self.board_width, self.board_height)

    def add_wall(self, row_num: int,
                 col_num: int) -> None:  # Related to the scene rows are y positions and columns are x position
        """
        Removes all edges of a given node, meaning a wall has been placed in the given coordinates (the path to that
        coordinate is unreachable)
        :param row_num: Row number of the node to remove edges from
        :param col_num: Column number of the node to remove edges from
        :return:
        """
        wall_coordinates: tuple[int, int] = (row_num, col_num)
        neighbors = list(self.underlying_graph.neighbors(wall_coordinates))
        for neighbor in neighbors:
            self.underlying_graph.remove_edge(neighbor, wall_coordinates)

    def remove_wall(self, row_num: int, col_num: int) -> None:
        """
        Add edges to neighbouring nodes for a given node, meaning a wall has been destroyed in the given coordinates
        (The coordinates are now traversable)
        :param row_num: Row number of the node to add edges to
        :param col_num: Column number of the node to add edges to
        :return:
        """
        wall_coordinates: tuple[int, int] = (row_num, col_num)
        neighbors = list(self.underlying_graph.neighbors(wall_coordinates))
        edges = [(wall_coordinates, neighbor) for neighbor in neighbors]
        self.underlying_graph.add_edges_from(edges)


class PlayerPixmapItem(QGraphicsPixmapItem):
    def __init__(self, x_pos: int, y_pos: int):
        """
        Player QGraphicPixmapItem, handles collisions and stores all properties of the player, such as
        number of bombs, speed, currently active powerups
        :param x_pos:
        :param y_pos:
        """
        super().__init__()
        self.player_sprites = {
            "up": [QPixmap(":/sprites/player_up1_sprite.png"), QPixmap(":/sprites/player_up2_sprite.png"),
                   QPixmap(":/sprites/player_up3_sprite.png")],
            "down": [QPixmap(":/sprites/player_down1_sprite.png"), QPixmap(":/sprites/player_down2_sprite.png"),
                     QPixmap(":/sprites/player_down3_sprite.png")],
            "left": [QPixmap(":/sprites/player_left1_sprite.png"), QPixmap(":/sprites/player_left2_sprite.png"),
                     QPixmap(":/sprites/player_left3_sprite.png")],
            "right": [QPixmap(":/sprites/player_right1_sprite.png"), QPixmap(":/sprites/player_right2_sprite.png"),
                      QPixmap(":/sprites/player_right3_sprite.png")],
        }
        self.setPixmap(self.player_sprites["right"][0])
        self.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsFocusable)  # QGraphicsItem.ItemIsSelectable |
        self.cell_size: int = 16

        self.movement_cycle: int = 0
        self.current_direction: str = "right"

        self.health_points: int = 3
        self.active_powerups: list[str] = []
        # self.speed: int = 4
        self.speed: float = 16
        self.num_of_bombs: int = 2
        self.bomb_range: int = 2

        self.autopilot: bool = False  # Flag deciding whether the player should move on mouse click or not
        # self.autopilot_path: list[tuple[int, int]] = []
        # self.distance_to_next_node: int = 0
        self.autopilot_last_visited_node = None
        self.last_direction = None
        self.destination: tuple[int, int] = None

        self.setPos(x_pos, y_pos)
        self.setZValue(4)

    def move(self, event: QKeyEvent) -> None:
        """
        Method handling player movement based on the key Pressed
        :param event: The button pressed by the user
        """
        x_translation: int = 0
        y_translation: int = 0

        match event.key():
            case Qt.Key_Left:
                x_translation = -self.speed
                self.current_direction = "left"

            case Qt.Key_Right:
                x_translation = self.speed
                self.current_direction = "right"

            case Qt.Key_Up:
                y_translation = -self.speed
                self.current_direction = "up"

            case Qt.Key_Down:
                y_translation = self.speed
                self.current_direction = "down"

        new_position = self.pos() + QPointF(x_translation, y_translation)

        if not self.collision(x_translation, y_translation):
            # Check if the player is at the edge of the scene and handle teleportation
            teleport = False
            if new_position.x() < 0:
                new_position.setX(self.scene().board_width * 16 - self.speed)
                x_translation = new_position.x() - self.pos().x()
                teleport = True
            elif new_position.x() > self.scene().board_width * 16 - self.speed:
                new_position.setX(0)
                x_translation = new_position.x() - self.pos().x()
                teleport = True

            if new_position.y() < 0:
                new_position.setY(self.scene().board_height * 16 - self.speed)
                y_translation = new_position.y() - self.pos().y()
                teleport = True
            elif new_position.y() > self.scene().board_height * 16 - self.speed:
                new_position.setY(0)
                y_translation = new_position.y() - self.pos().y()
                teleport = True

            # If teleporting, check for collisions at the new position
            if teleport:
                if self.collision(x_translation, y_translation):
                    # If there's a collision after teleportation, don't teleport
                    return
            self.setPos(new_position)

            self.movement_cycle = (self.movement_cycle + 1) % len(self.player_sprites[self.current_direction])

            self.setPixmap(self.player_sprites[self.current_direction][self.movement_cycle])
            print(self.pos())

    def collision(self, x_translation: int, y_translation: int) -> bool:
        """
        Checks for collision between the player and walls, if a wallpass powerup is active the player can pass
         through walls. If a collision occurs, the player can not move to the position given by:
         (self.pos().x() + x_translation, self.pos().y() + y_translation)
        :param x_translation: Translation in the x direction that is about to happen
        :param y_translation: Translation in the y direction that is about to happen
        :return:
        """
        bounding_rect_after_translation = self.boundingRect().translated(
            self.pos() + QPointF(x_translation, y_translation))

        colliding_items = self.scene().items(bounding_rect_after_translation)

        for item in colliding_items:
            if isinstance(item, UnbreakableWall):
                return True
            elif isinstance(item, (OneBombWall, TwoBombWall)) and "wallpass" not in self.active_powerups:
                return True
            elif "wallpass" in self.active_powerups:
                return False

        return False


class EnemyPixmapItem(QGraphicsPixmapItem):
    def __init__(self, x_pos: int, y_pos: int):
        """
        All enemies inherit from this class, functionalities and properties that apply
        to every enemy should be put here
        :param x_pos: x coordinate of GameScene position of the enemy
        :param y_pos: x coordinate of GameScene position of the enemy
        """
        super().__init__()
        self.setPos(x_pos, y_pos)
        self.setFlags(QGraphicsItem.ItemIsMovable)
        self.setZValue(2)
        self.speed = None
        self.orientation = None

    def move(self) -> None:
        """ Different enemies have different behaviors, each enemy has to have this method implemented """
        ...


class StaticEnemy(EnemyPixmapItem):
    def __init__(self, x_pos: int, y_pos: int):
        """
        Static enemy class, this enemy does not move at all
        :param x_pos: x coordinate of GameScene position of the enemy
        :param y_pos: x coordinate of GameScene position of the enemy
        """
        super().__init__(x_pos, y_pos)
        self.setPixmap(QPixmap(":/sprites/enemy_0_sprite.png"))


class PatrollingEnemy(EnemyPixmapItem):
    def __init__(self, speed: int, x_pos: int, y_pos: int):
        """
        Patrolling enemy class, this enemy moves either horizontally or vertically until he
        encounters a wall, at which point he switches directions
        :param speed: Speed at which the enemy moves
        :param x_pos: x coordinate of GameScene position of the enemy
        :param y_pos: x coordinate of GameScene position of the enemy
        """
        super().__init__(x_pos, y_pos)
        self.setPixmap(QPixmap(f":/sprites/enemy_{speed}_sprite.png"))
        self.speed = speed * 4
        self.orientation: str = random.choice(["horizontal", "vertical"])

    def move(self) -> None:
        """
        This function is called at every timeout of the QTimer placed within
         the GameScene. Enemy performs one step in accordance with his speed and current position
         """
        x_translation = 0
        y_translation = 0

        if self.orientation == "horizontal":
            x_translation = self.speed
        else:
            y_translation = self.speed

        if not self.collision(x_translation, y_translation):
            self.moveBy(x_translation, y_translation)
        else:
            self.speed = -self.speed
            # self.moveBy(x_translation, y_translation)

    def collision(self, x_translation: int, y_translation: int) -> bool:
        """ Collision checker between the enemy and the walls """
        bounding_rect_after_translation = self.boundingRect().translated(
            self.pos() + QPointF(x_translation, y_translation))

        colliding_items = self.scene().items(bounding_rect_after_translation)

        for item in colliding_items:
            if isinstance(item, WallPixmapItem):
                return True

        return False


class FollowingEnemy(EnemyPixmapItem):
    def __init__(self, board: Board, player: PlayerPixmapItem, speed: int, x_pos: int, y_pos: int):
        """
        Following enemy class, utilizing the underlying graph of the board the enemy can actively
        seek out the player.
        :param board: Current board's state needed for pathfinding
        :param player: Reference to the player so that the enemy can calculate his position at all times
        :param speed: Speed at which the enemy moves
        :param x_pos: x coordinate of GameScene position of the enemy
        :param y_pos: x coordinate of GameScene position of the enemy
        """
        super().__init__(x_pos, y_pos)
        self.setPixmap(QPixmap(f":/sprites/enemy_{speed + 4}_sprite.png"))
        self.speed = speed * 4
        self.player = player
        self.board = board
        self.starting_node = None
        self.last_direction = None

    def move(self) -> None:
        """
        Moving the enemy one step closer to the player.
        If the enemy is not in position's divisible by 16, he is in between cells. To prevent him
        from going through middle of the walls, instead of going to the next node he moves along the
        last direction until he reaches the next full position.
        """
        current_position = (self.pos().x(), self.pos().y())

        if (current_position[0] % 16) != 0 or (current_position[1] % 16) != 0:
            if self.starting_node is not None and self.last_direction is not None:
                self.moveBy(self.last_direction[0], self.last_direction[1])
            return

        player_position_x, player_position_y = self.player.pos().x(), self.player.pos().y()
        player_current_node = (int(player_position_y // 16), int(player_position_x // 16))

        current_node = (int(self.pos().y() // 16), int(self.pos().x() // 16))

        try:
            shortest_path = nx.shortest_path(self.board.underlying_graph, source=current_node,
                                             target=player_current_node)
            next_node = shortest_path[1]

            target_position = (next_node[1] * 16, next_node[0] * 16)

            direction = np.array(target_position) - np.array(current_position)

            if abs(direction[0]) > abs(direction[1]):
                move_by = (np.sign(direction[0]) * self.speed, 0)
            else:
                move_by = (0, np.sign(direction[1]) * self.speed)

            self.starting_node = current_node
            self.last_direction = move_by

            self.moveBy(move_by[0], move_by[1])

        except nx.NetworkXNoPath:
            return

        except IndexError:
            return

    def collision(self, x_translation: int, y_translation: int) -> bool:
        """ Checks for collision between the enemy and walls """
        bounding_rect_after_translation = self.boundingRect().translated(
            self.pos() + QPointF(x_translation, y_translation))

        colliding_items = self.scene().items(bounding_rect_after_translation)

        for item in colliding_items:
            if isinstance(item, WallPixmapItem):
                return True

        return False


class BackgroundPixmapItem(QGraphicsPixmapItem):
    def __init__(self, x_pos: int, y_pos: int):
        """
        Background of the board, this item does not come into interaction with any other item
        :param x_pos: x coordinate of GameScene position of the item
        :param y_pos: x coordinate of GameScene position of the item
        """
        super().__init__()
        self.setPixmap(QPixmap(":/sprites/background_sprite.png"))
        self.setPos(x_pos, y_pos)


class WallPixmapItem(QGraphicsPixmapItem):
    def __init__(self, x_pos: int, y_pos: int):
        """
        Parent class for wall types, all functionalities and properties adhering to all
         the walls should be put here.
        :param x_pos: x coordinate of GameScene position of the item
        :param y_pos: x coordinate of GameScene position of the item
        """
        super().__init__()
        self.setPos(x_pos, y_pos)
        self.is_breakable: bool = True


class UnbreakableWall(WallPixmapItem):
    def __init__(self, x_pos: int, y_pos: int):
        """
        Unbreakable wall, can be moved through if the player has the wallpass powerup
        :param x_pos: x coordinate of GameScene position of the item
        :param y_pos: x coordinate of GameScene position of the item
        """
        super().__init__(x_pos, y_pos)
        self.setPixmap(QPixmap(":/sprites/unbreakable_wall_sprite.png"))


class OneBombWall(WallPixmapItem):
    def __init__(self, x_pos: int, y_pos: int):
        """
        Wall taking one bomb to destroy
        :param x_pos: x coordinate of GameScene position of the item
        :param y_pos: x coordinate of GameScene position of the item
        """
        super().__init__(x_pos, y_pos)
        self.setPixmap(QPixmap(":/sprites/one_bomb_wall_sprite.png"))


class TwoBombWall(WallPixmapItem):
    def __init__(self, x_pos: int, y_pos: int):
        """
        Wall taking two bombs to destroy, after it's been hit with one bomb it's sprite
        changed to that of a one-bomb wall and its HP decrements
        :param x_pos: x coordinate of GameScene position of the item
        :param y_pos: x coordinate of GameScene position of the item
        """
        super().__init__(x_pos, y_pos)
        self.setPixmap(QPixmap(":/sprites/two_bomb_wall_sprite.png"))
        self.wall_hp: int = 2


class BombPixmapItem(QGraphicsPixmapItem):
    def __init__(self, player: PlayerPixmapItem, x_pos: int, y_pos: int):
        """
        Bomb item, the player places it on the scene after pressing 'space'
        :param player: Reference to the current's game player, needed to operate on powerups
        :param x_pos: x coordinate of GameScene position of the item
        :param y_pos: x coordinate of GameScene position of the item
        """
        super().__init__()
        self.setPixmap(QPixmap(":/sprites/bomb_sprite.png"))
        self.setZValue(3)
        self.cell_size: int = 16
        self.setPos(x_pos, y_pos)
        self.player = player
        self.range: int = self.player.bomb_range


class ExplosionPixmapItem(QGraphicsPixmapItem):
    def __init__(self, x_pos: int, y_pos: int):
        """
        Explosion item, displayed after the bomb explodes and quickly disappears
        :param x_pos: x coordinate of GameScene position of the item
        :param y_pos: x coordinate of GameScene position of the item
        """
        super().__init__()
        self.setPixmap(QPixmap(":/sprites/explosion_sprite.png"))
        self.setPos(x_pos, y_pos)
        self.setZValue(3)
