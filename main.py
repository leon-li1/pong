import pygame

pygame.display.set_caption("Pong")
pygame.init()

# Constants
WIDTH, HEIGHT = 700, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 7
SCORE_FONT = pygame.font.SysFont("comicsans", 50)
WINNING_SCORE = 5

class Paddle:
    COLOR = WHITE
    VEL = 5

    def __init__(self, x, y, width, height):
        self.x = self.orig_x = x
        self.y = self.orig_y = y
        self.width = width
        self.height = height

    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

    def move(self, up):
        if up and self.y - self.VEL > 0:
            self.y -= self.VEL
        elif not up and self.y + self.height + self.VEL < HEIGHT:
            self.y += self.VEL

    def reset(self):
        self.x = self.orig_x
        self.y = self.orig_y

class Ball:
    MAXVEL = 10
    COLOR = WHITE

    def __init__(self, x, y, radius):
        self.x = self.orig_x = x
        self.y = self.orig_y = y
        self.radius = radius
        self.xvel = self.MAXVEL
        self.yvel = 0
    
    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.xvel
        self.y += self.yvel

    def reset(self):
        self.x = self.orig_x
        self.y = self.orig_y
        self.xvel *= -1
        self.yvel = 0

def draw(win, paddles, ball, left_score, right_score):
    win.fill(BLACK)

    left_score_text = SCORE_FONT.render(f"{left_score}", 1, WHITE)
    right_score_text = SCORE_FONT.render(f"{right_score}", 1, WHITE)
    win.blit(left_score_text, (WIDTH // 4 - left_score_text.get_width() // 2, 20))
    win.blit(right_score_text, (WIDTH * (3/4) - right_score_text.get_width() // 2, 20))

    for paddle in paddles:
        paddle.draw(win)

    # draw a middle line
    for i in range(10, HEIGHT, HEIGHT // 20):
        if i % 2 == 1:
            continue

        pygame.draw.rect(win, WHITE, (WIDTH // 2 - 5, i, 10, HEIGHT // 20))

    ball.draw(win)
    pygame.display.update()

def handle_keys(keys, left_paddle, right_paddle):
    if keys[pygame.K_w]:
        left_paddle.move(True)
    if keys[pygame.K_s]:
        left_paddle.move(False)

    if keys[pygame.K_UP]:
        right_paddle.move(True)
    if keys[pygame.K_DOWN]:
        right_paddle.move(False)

def handle_collision(ball, left_paddle, right_paddle):
    if ball.y + ball.radius >= HEIGHT or ball.y - ball.radius <= 0:
        ball.yvel *= -1

    if ball.xvel < 0:
        if (ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height) and \
                (ball.x - ball.radius <= left_paddle.x + left_paddle.width):
            ball.xvel *= -1

            middle_y = left_paddle.y + left_paddle.height / 2
            delta_y = middle_y - ball.y
            ratio = delta_y / (left_paddle.height / 2)
            ball.yvel = -ball.MAXVEL * ratio

    else:
        if (ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height) and \
                (ball.x + ball.radius >= right_paddle.x):
            ball.xvel *= -1

            middle_y = right_paddle.y + right_paddle.height / 2
            delta_y = middle_y - ball.y
            ratio = delta_y / (right_paddle.height / 2)
            ball.yvel = -ball.MAXVEL * ratio

def reset_game(ball, left_paddle, right_paddle):
    ball.reset()
    left_paddle.reset()
    right_paddle.reset()

def main():
    run = True
    clock = pygame.time.Clock()

    left_paddle = Paddle(10, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)

    left_score = 0
    right_score = 0

    while run:
        clock.tick(FPS)    
        draw(WIN, [left_paddle, right_paddle], ball, left_score, right_score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        handle_keys(keys, left_paddle, right_paddle)
        ball.move()
        handle_collision(ball, left_paddle, right_paddle)

        if ball.x < 0:
            right_score += 1
            reset_game(ball, left_paddle, right_paddle)
        elif ball.x > WIDTH:
            left_score += 1
            reset_game(ball, left_paddle, right_paddle)

        won = False
        if left_score >= WINNING_SCORE:
            won = True
            win_text = SCORE_FONT.render(f"Left player won!", 1, WHITE)
        elif right_score >= WINNING_SCORE:
            won = True
            win_text = SCORE_FONT.render(f"Right player won!", 1, WHITE)

        if won:
            WIN.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - win_text.get_height() // 2))
            pygame.display.update()
            pygame.time.delay(3000)
            left_score, right_score = 0, 0
            reset_game(ball, left_paddle, right_paddle)
        
    pygame.quit()

if __name__ == '__main__':
    main()