# Bomberman Game
On start a main menu opens, there is endless mode, story mode and instructions/options.
Starting a new game (in either mode) opens a GameWidget (inheriting from QWidget) with a QGraphicsView in it.
  
Full documentation of each class and method is available in the Pydoc generated .html files in the documentation subdirectoy.


## Installation
To install the required dependencies run.
```pip install -r requirements.txt```  
The entry point of the game is 'main.py' running it while inside a virtual environment with the installed requirements
starts the game


## QGraphicsScene, QGraphicsItem
The game contains GameView, GameScene that inherit from QGraphicsView and QGraphicsScene and numerous
objects that inherit from QGraphicsPixmapItem (Some walls and enemies inherit from EnemyPixmapItem and WallPixmapItem
to have less repeating code).

### Powerups
The user can choose from 8 different powerups, that can be found in the
original game.

### Keyboard movement
The GameScene overrides 'keyPressEvent' method which handles player's movement and bomb placing.

### Mouse movement
The GameScene overrides 'mousePressEvent' method which handles user's mouse input. When the player clicks on an empty
field in the game, the shortest path from the current position to that field is calculated and the player starts
walking there. If there is no path available between the two locations nothing happens.

### .rc Files graphics
All the sprites are loaded from the resources_rc module, which was 
compiled using the following command:  
``` pyside6-rcc resources.qrc -o resources_rc.py```  

Sprites (16x16 png, except for the title screen sprite) come from this site:
https://www.spriters-resource.com/nes/bomberman/

### Enemies
There are 7 types of enemies:
- Static
- Patrolling horizontally or vertically with variable speed (1-3)
- Following the player with variable speed (1-3)  

The patrolling enemies walk into a certain direction until they hit a wall, after  
which they start going the other direction.

The following enemies move towards the player, thanks to an underlying graph which add another
layer of logic to the game.


### Customizable board
Before the game starts, user is prompted to enter the desired board's width and height, as well as how densely with
walls should it be populated. When the player makes a move that would put him outside the GameScene, instead he is
'teleported' to the other side of the board (if there aren't any walls in that area).

### Player animation
Player movements animation are implemented through swapping the current player's Pixmap based on the direction 
he is going and current cycle of the animation. There are 3 sprites for player for every direction, as in the original
NES Bomberman  


Fun fact:  
The original NES Bomberman game from 1985 was written in the 6502 assembly language.
