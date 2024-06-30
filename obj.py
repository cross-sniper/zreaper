import pygame
class Obj:
    def __init__(self, x,y):
        self.x=x
        self.y=y

class Node:
    def __init__(self, x, y, width, height, color, script, engineInstance, name):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.script = script
        if name:
            self.name = name
        self.context = {"dt": 0, "self": self, "engine": engineInstance}  # Context for the script
        # Initialize script if provided
        if self.script:
            try:
                exec(self.script, self.context)
                if 'init' in self.context:
                    self.context['init']()
            except Exception as e:
                print(f"Error in script initialization: {e}")
                exit(1)

    def update(self, dt):
        self.context['dt'] = dt
        # Update node using script if provided
        if self.script:
            try:
                if 'update' in self.context:
                    self.context['update'](dt)
            except Exception as e:
                print(f"Error in script update: {e}")
                exit(1)

    def draw(self, drawRect):
        drawRect(self.x, self.y, self.width, self.height, self.color)
