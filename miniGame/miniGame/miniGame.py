
#!/bin/env python
import pygame
import random

# """ Some constants """

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
YELLOW = (255, 255, 0)

class GameState:
    """ Holding game state relevant data """

    def __init__(self):
        """ default constructor """

        self.key_store = {}
        self.running = True
        self.screen = None
        self.size = [800, 600]
        pygame.direction = [0, 1]
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()
        self.figures = []
        self.font = myfont = pygame.font.SysFont('Comic Sans MS', 30)


class Drawable:
    """ a drawable base class """

    def __init__(self, game_state, color, direction, position):
        self._game_state = game_state
        self.color = color
        self.direction = direction
        self.position = position
        self.size = 10
        self._rect = pygame.Rect(position[0],
                                 position[1],
                                 self.size,
                                 self.size)

    def draw(self):
        """ draw the bot """
        pygame.draw.rect(self._game_state.screen, self.color, self._rect)
        self._rect = self._rect.move(self.direction)
        self.move()

    def move(self):
        """ not implemented """

    def collided(self, other):
        """ check for collision """
        return self._rect.colliderect(other._rect)


class Bot(Drawable):
    """ a single bot """
    def move(self):
        """ move method """
        if self._rect.left < 0 or self._rect.right > self._game_state.size[0]:
            self.direction[0] = -self.direction[0]

        if self._rect.top < 0 or self._rect.bottom > self._game_state.size[1]:
            self.direction[1] = -self.direction[1]


class Human(Drawable):
    """ a human """
    player_count = 0
    def __init__(self, game_state, color, direction, position, keys):
        """ constructor """
        Drawable.__init__(self, game_state, color, direction, position)
        self._keys = keys
        self.score = 0
        self._player_number = Human.player_count
        Human.player_count += 1

    def move(self):
        """ move method """
        pressed = pygame.key.get_pressed()

        if pressed[self._keys[0]]:
            self._rect = self._rect.move((-1, 0))

        if pressed[self._keys[1]]:
            self._rect = self._rect.move((1, 0))

        if pressed[self._keys[2]]:
            self._rect = self._rect.move((0, -1))

        if pressed[self._keys[3]]:
            self._rect = self._rect.move((0, 1))

        while self._rect.left < 0:
            self._rect = self._rect.move(1, 0)

        while self._rect.right > self._game_state.size[0]:
            self._rect = self._rect.move(-1, 0)

        while self._rect.top < 0:
            self._rect = self._rect.move(0, 1)

        while self._rect.bottom > self._game_state.size[1]:
            self._rect = self._rect.move(0, -1)

    def draw(self):
        Drawable.draw(self)
        text = self._game_state.font.render("Player %d: %d" % (self._player_number, self.score),
                                            False, WHITE)
        position = (text.get_height(), text.get_height()*self._player_number*1.2)
        self._game_state.screen.blit(text, position)

def init():
    """ All initialisation stuff goes in here """
    game_state_initial = GameState()

    return game_state_initial


def handle_events(game_state):
    """ handle the events """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

        if event.type == pygame.KEYDOWN:
            # handle keypressed
            if event.key == pygame.K_ESCAPE:
                return False
    return True


def check_collision(game_state):
    """ check for colision between figures """
    to_del = []
    for figure1 in game_state.figures:
        if isinstance(figure1, Bot):
            continue
        for figure2 in game_state.figures:
            if isinstance(figure2, Human):
                continue
            if figure1 == figure2:
                continue
            if figure1.collided(figure2):
                to_del.append(figure2)
                figure1.score += 1

    for to_be_removed in to_del:
        game_state.figures.remove(to_be_removed)


def loop(game_state):
    """ main loop in here """
    game_state.figures = [
        Bot(game_state, GREEN, [1, 1], (game_state.size[0]/3, game_state.size[1]/3)),
        Bot(game_state, RED, [-1, -1], (game_state.size[0]/3*2, game_state.size[1]/3*2)),
        Human(game_state, GRAY, [0, 0], (game_state.size[0]/3, game_state.size[1]/2),
              (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_SPACE)),
        Human(game_state, YELLOW, [0, 0], (game_state.size[0]/3*2, game_state.size[1]/2),
              (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_RETURN)),
        ]
    while handle_events(game_state):
        blank_screen(game_state)
        for figure in game_state.figures:
            figure.draw()

        check_collision(game_state)

        bots = 0
        for figure in game_state.figures:
            if isinstance(figure, Bot):
                bots += 1

        if bots == 0:
            colors = [GREEN, RED]
            speeds = [-1, 1]

            color = colors[random.randint(0, 1)]
            speed = [speeds[random.randint(0, 1)], speeds[random.randint(0, 1)]]
            position = (random.randint(10, game_state.size[0]-10),
                        random.randint(10, game_state.size[1]-10))

            game_state.figures.append(
                Bot(game_state,
                    color,
                    speed,
                    position))

        pygame.display.flip()
        game_state.clock.tick(160)


def blank_screen(game_state):
    """ Blank screen here something like a background image could be handled """
    game_state.screen.fill(BLACK)


def main():
    """ Main function """

    game_state = init()

    loop(game_state)


if __name__ == "__main__":
    main()
