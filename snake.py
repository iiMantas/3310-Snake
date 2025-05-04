import pygame
import sys
import random
from pygame.math import Vector2

pygame.init()

title_font = pygame.font.Font(None, 60)
score_font = pygame.font.Font(None, 40)

GREEN = (113, 128, 39)
DARK_GREEN = (43, 51, 24)

cell_size = 30
number_of_cells = 25
OFFSET = 75


def save_score(score):
    """Išsaugome žaidimo taškus į failą"""
    with open("game_results.txt", "a") as file:
        file.write(f"Score: {score}\n")


def load_scores():
    """Krauname taškus iš failo"""
    try:
        with open("game_results.txt", "r") as file:
            scores = file.readlines()
            scores = [int(score.strip().split(":")[1]) for score in scores]
        return scores
    except FileNotFoundError:
        return []


class GameObject:
    def __init__(self, position):
        self.position = position

    def draw(self, screen):
        raise NotImplementedError("Subklasės turi implementuoti šį metodą")


class Food(GameObject):
    def __init__(self, snake_body):
        self.position = self.generate_random_pos(snake_body)

    def generate_random_pos(self, snake_body):
        position = self.generate_random_cell()
        while position in snake_body:
            position = self.generate_random_cell()
        return position

    def draw(self, screen):
        food_rect = pygame.Rect(OFFSET + self.position.x * cell_size,
                                OFFSET + self.position.y * cell_size,
                                cell_size, cell_size)
        screen.blit(food_surface, food_rect)

    def generate_random_cell(self):
        x = random.randint(0, number_of_cells - 1)
        y = random.randint(0, number_of_cells - 1)
        return Vector2(x, y)


class Snake(GameObject):
    def __init__(self):
        super().__init__(Vector2(6, 9))
        self.body = [Vector2(6, 9), Vector2(5, 9), Vector2(4, 9)]
        self.direction = Vector2(1, 0)
        self.eat_sound = pygame.mixer.Sound("Garsai/kramtymas.mp3")
        self.wall_hit = pygame.mixer.Sound("Garsai/atsitrenkimas.mp3")

    def draw(self, screen):
        for segment in self.body:
            segment_rect = (OFFSET + segment.x * cell_size,
                            OFFSET + segment.y * cell_size,
                            cell_size, cell_size)
            pygame.draw.rect(screen, DARK_GREEN, segment_rect, 0, 7)

    def move(self, grow=False):
        """Peršnaudo naują galvą. Jei grow=True – tail neištrinamas."""
        new_head = self.body[0] + self.direction
        self.body.insert(0, new_head)
        if not grow:
            self.body.pop()  # jei nesivysto, pašaliname paskutinį segmentą

    def update(self):
        """Atnaujiname gyvatės poziciją ir patikriname, kad ji nesikerta su savo kūnu"""
        new_head = self.body[0] + self.direction
        if new_head in self.body:  # Jei galva susikerta su kūnu
            raise Exception("Snake collided with itself")
        self.move()  # Atlikti judėjimą

    def reset(self):
        """Atstatome gyvatės pradinę būseną."""
        self.body = [Vector2(6, 9), Vector2(5, 9), Vector2(4, 9)]
        self.direction = Vector2(1, 0)


class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.state = "RUNNING"
        self.score = 0
        self.best_score = max(load_scores(), default=0)

    def update(self):
        if self.state == "RUNNING":
            # Skaičiuojame naują galvės poziciją
            new_head = self.snake.body[0] + self.snake.direction
            # Jei nauja pozicija sutampa su maistu – augaime nedelsdami
            if new_head == self.food.position:
                self.snake.move(grow=True)
                self.food.position = self.food.generate_random_pos(self.snake.body)
                self.score += 1
                self.snake.eat_sound.play()
            else:
                self.snake.move(grow=False)

            self.check_collision_with_edges()
            self.check_collision_with_tail()

    def draw(self, screen):
        self.food.draw(screen)
        self.snake.draw(screen)
        best_score_surface = score_font.render(f"Best Score: {self.best_score}", True, DARK_GREEN)
        screen.blit(best_score_surface, (OFFSET - 5, OFFSET + cell_size * number_of_cells + 50))

    def check_collision_with_edges(self):
        head = self.snake.body[0]
        if head.x >= number_of_cells or head.x < 0 or head.y >= number_of_cells or head.y < 0:
            self.game_over()

    def check_collision_with_tail(self):
        head = self.snake.body[0]
        if head in self.snake.body[1:]:
            self.game_over()

    def game_over(self):
        save_score(self.score)
        self.best_score = max(self.best_score, self.score)
        self.snake.reset()
        self.food.position = self.food.generate_random_pos(self.snake.body)
        self.state = "STOPPED"
        self.score = 0
        self.snake.wall_hit.play()


if __name__ == "__main__":
    screen = pygame.display.set_mode((2 * OFFSET + cell_size * number_of_cells,
                                      2 * OFFSET + cell_size * number_of_cells))
    pygame.display.set_caption("3310 Snake")
    clock = pygame.time.Clock()
    global food_surface
    food_surface = pygame.image.load("Grafikos/food.png")
    SNAKE_UPDATE = pygame.USEREVENT
    pygame.time.set_timer(SNAKE_UPDATE, 150)

    game = Game()

    while True:
        for event in pygame.event.get():
            if event.type == SNAKE_UPDATE:
                game.update()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if game.state == "STOPPED":
                    game.state = "RUNNING"
                if event.key == pygame.K_UP and game.snake.direction != Vector2(0, 1):
                    game.snake.direction = Vector2(0, -1)
                if event.key == pygame.K_DOWN and game.snake.direction != Vector2(0, -1):
                    game.snake.direction = Vector2(0, 1)
                if event.key == pygame.K_LEFT and game.snake.direction != Vector2(1, 0):
                    game.snake.direction = Vector2(-1, 0)
                if event.key == pygame.K_RIGHT and game.snake.direction != Vector2(-1, 0):
                    game.snake.direction = Vector2(1, 0)

        screen.fill(GREEN)
        pygame.draw.rect(screen, DARK_GREEN, (OFFSET - 5, OFFSET - 5,
                                                cell_size * number_of_cells + 10,
                                                cell_size * number_of_cells + 10), 5)
        game.draw(screen)
        title_surface = title_font.render("3310 SNAKE", True, DARK_GREEN)
        score_surface = score_font.render(str(game.score), True, DARK_GREEN)
        screen.blit(title_surface, (OFFSET - 5, 20))
        screen.blit(score_surface, (OFFSET - 5, OFFSET + cell_size * number_of_cells + 10))
        pygame.display.update()
        clock.tick(60)
