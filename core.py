import pygame
from pygame import *
from pygame import mixer
from . import obj
import time


class Engine:
    screen: pygame.Surface
    gameLoop: callable
    running: bool
    _keys: dict
    _ExitOnEsc: bool
    _font: pygame.font.Font
    _objects: list[obj.Node]

    def __init__(self, width: int, height: int, title: str) -> None:
        """
        Initializes pygame and mixer, and sets up the window.

        Args:
            width (int): The width of the window.
            height (int): The height of the window.
            title (str): The title of the window.

        Returns:
            None
        """
        try:
            pygame.init()
            mixer.init()
            self.screen = pygame.display.set_mode((width, height))
            pygame.display.set_caption(title)
        except pygame.error as e:
            print(f"An error occurred while initializing Pygame: {e}")
            exit(1)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            exit(1)

        pygame.font.init()
        self._font = pygame.font.Font(None, 24)

        self._keys = {}
        self.gameLoop = None
        self.running = False
        self._ExitOnEsc = False
        self._objects = []

    def get_node_list_by_name(self,name: str) -> list[obj.Node]:
        nodes = []
        for node in self._objects:
            if node.name == name:
                nodes.append(node)
        return nodes

    def get_node_by_name(self,name: str) -> obj.Node:
        for node in self._objects:
            if node.name == name:
                return node

        raise Exception(f"unable to find node '{name}'")

    def drawText(self, text: str, x: int, y: int, size: int, color: pygame.Color):
        """
        Draws text on the screen.

        Args:
            text (str): The text to draw.
            x (int): The x-coordinate of the text.
            y (int): The y-coordinate of the text.
            size (int): The size of the text.
            color (pygame.Color): The color of the text.
        """
        textSurface = self._font.render(text, True, (0, 0, 0))
        self.screen.blit(textSurface, (x + 2, y + 2))
        textSurface = self._font.render(text, True, color)
        self.screen.blit(textSurface, (x, y))

    def new_node(self, x: int, y: int, width: int, height: int, color: pygame.Color, script: str | None = None, name: str | None=None) -> obj.Node:
        """
        Creates a new node.

        Args:
            x (int): The x-coordinate of the node.
            y (int): The y-coordinate of the node.
            width (int): The width of the node.
            height (int): The height of the node.
            color (pygame.Color): The color of the node.
            script (str|None): Optional script to give this a behaviour.

        Returns:
            obj.Node: The created node.
        """
        node = obj.Node(x, y, width, height, color, script,self, name)
        self._objects.append(node)
        return node

    def drawRect(self, x: int, y: int, width: int, height: int, color: pygame.Color) -> None:
        """
        Draws a rectangle on the screen.

        Args:
            x (int): The x-coordinate of the rectangle.
            y (int): The y-coordinate of the rectangle.
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            color (pygame.Color): The color of the rectangle.

        Returns:
            None
        """
        pygame.draw.rect(self.screen, color, (x, y, width, height))

    def isKeyPressed(self, key: str) -> bool:
        """
        Checks if a key is pressed.

        Args:
            key (str): The key to check.

        Returns:
            bool: True if the key is pressed, False otherwise.
        """
        return self._keys.get(key, False)

    def setGameLoop(self, gameLoop: callable) -> None:
        """
        Sets the game loop function.

        Args:
            gameLoop (callable): The function to call each frame with delta time.

        Returns:
            None
        """
        self.gameLoop = gameLoop

    def mainLoop(self) -> None:
        """
        Runs the game loop.
        """
        if self.gameLoop is None:
            print("Game loop function not set. Call setGameLoop() before mainLoop().")
            return

        self.running = True
        lastTime = time.time()
        while self.running:
            dt = time.time() - lastTime
            lastTime = time.time()
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE and self._ExitOnEsc:
                        self.running = False
                        return
                    self._keys[event.unicode] = True
                elif event.type == KEYUP:
                    self._keys[event.unicode] = False

            self.gameLoop(dt)

            self.updateNodes(dt)
            self.drawNodes()

            self.show()

    def clearBg(self, color: tuple[int, int, int]) -> None:
        """
        Clears the background with the given color.

        Args:
            color (tuple[int, int, int]): The color to fill the background with.

        Returns:
            None
        """
        self.screen.fill(color)

    def exit_on_esc(self, enable: bool) -> None:
        """
        Enables or disables the exit on ESC key.

        Args:
            enable (bool): True to enable, False to disable.

        Returns:
            None
        """
        self._ExitOnEsc = enable

    def show(self) -> None:
        """
        Updates the display.

        Returns:
            None
        """
        pygame.display.flip()

    def updateNodes(self, dt: float) -> None:
        """
        Updates all nodes.

        Args:
            dt (float): Delta time since the last frame.

        Returns:
            None
        """
        for node in self._objects:
            node.update(dt)

    def drawNodes(self) -> None:
        """
        Draws all nodes.
        """
        for node in self._objects:
            node.draw(self.drawRect)
