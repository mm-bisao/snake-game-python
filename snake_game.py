import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
from kivy.clock import Clock
import random

kivy.require('2.0.0')  # Verifica a versão do Kivy

# Definindo as cores
WHITE = [1, 1, 1]
GREEN = [0, 1, 0]
RED = [1, 0, 0]
BLACK = [0, 0, 0]

class SnakeGame(Widget):
    def __init__(self, **kwargs):
        super(SnakeGame, self).__init__(**kwargs)
        self.snake = [(0, 0)]  # Lista para armazenar as posições da cobra
        self.snake_direction = (1, 0)  # Direção inicial: para a direita
        self.food = None
        self.score = 0
        self.speed = 0.1  # Velocidade de movimento da cobra
        self._spawn_food()
        Clock.schedule_interval(self.update, self.speed)

    def update(self, dt):
        # Movimentando a cobra
        head_x, head_y = self.snake[0]
        new_head = (head_x + self.snake_direction[0], head_y + self.snake_direction[1])

        # Verifica se a cobra colidiu com a parede ou com ela mesma
        if new_head in self.snake or not (-300 < new_head[0] < 300) or not (-300 < new_head[1] < 300):
            self.reset_game()
            return

        self.snake.insert(0, new_head)

        # Verifica se a cobra comeu a comida
        if new_head == self.food:
            self.score += 1
            self._spawn_food()
        else:
            self.snake.pop()

        self.canvas.clear()
        self._draw_snake()
        self._draw_food()

    def on_touch_move(self, touch):
        # Atualiza a direção da cobra com base no toque
        if abs(touch.x - self.center_x) > abs(touch.y - self.center_y):
            if touch.x > self.center_x and self.snake_direction != (-1, 0):
                self.snake_direction = (1, 0)
            elif touch.x < self.center_x and self.snake_direction != (1, 0):
                self.snake_direction = (-1, 0)
        else:
            if touch.y > self.center_y and self.snake_direction != (0, -1):
                self.snake_direction = (0, 1)
            elif touch.y < self.center_y and self.snake_direction != (0, 1):
                self.snake_direction = (0, -1)

    def _draw_snake(self):
        with self.canvas:
            Color(*GREEN)
            for segment in self.snake:
                Rectangle(pos=(segment[0], segment[1]), size=(20, 20))

    def _draw_food(self):
        with self.canvas:
            Color(*RED)
            Rectangle(pos=(self.food[0], self.food[1]), size=(20, 20))

    def _spawn_food(self):
        # Gera uma nova posição aleatória para a comida
        self.food = (random.randint(-290, 290), random.randint(-290, 290))

    def reset_game(self):
        # Reseta o jogo
        self.snake = [(0, 0)]
        self.snake_direction = (1, 0)
        self.score = 0
        self._spawn_food()

class SnakeApp(App):
    def build(self):
        game = SnakeGame()
        return game

if __name__ == '__main__':
    SnakeApp().run()
