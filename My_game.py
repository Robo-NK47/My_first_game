import pygame
import os
import random

### GENERAL ###
FPS = 60
main_dir = os.getcwd()
SOUND_DIRECTORY = os.path.join(main_dir, 'Assets', 'Sounds')
PICTURE_DIRECTORY = os.path.join(main_dir, 'Assets', 'Pictures')
pygame.mixer.init()
pygame.font.init()
pygame.mixer.music.load(os.path.join(SOUND_DIRECTORY, 'Blue lantern.mp3'))
SCORE_FONT = pygame.font.SysFont('comicsans', 40)
FINISH_FONT = pygame.font.SysFont('comicsans', 100)
WHITE = (255, 255, 255)

### ENVIRONMENT ###
DESKTOP = pygame.image.load(os.path.join(PICTURE_DIRECTORY, 'Backround.png'))
WIDTH, HEIGHT = DESKTOP.get_width(), DESKTOP.get_height()
LOWER_FLOOR_HEIGHT = 540
HIGHER_FLOOR_HEIGHT = 400
LOWER_FLOOR = pygame.Rect(0, LOWER_FLOOR_HEIGHT + 130, WIDTH, 10)
HIGHER_FLOOR = pygame.Rect(0.5 * (WIDTH - 520), HIGHER_FLOOR_HEIGHT - 7, 570, 25)

### PLAYER ###
PLAYER_WALK = pygame.image.load(os.path.join(PICTURE_DIRECTORY, 'Nadav_walk_right.png'))
PLAYER_JUMPING = pygame.image.load(os.path.join(PICTURE_DIRECTORY, 'Nadav_jump.png'))
PLAYER_WIDTH = PLAYER_WALK.get_width()
PLAYER_HEIGHT = PLAYER_WALK.get_height()
PLAYER_JUMP = 10
PLAYER_MASS = 5
PLAYER_VELOCITY = 5
JUMP_FORCE = (PLAYER_VELOCITY ** 2 / PLAYER_MASS)
PLAYER_HIT = pygame.USEREVENT + 1
PLAYER_DAMAGED = pygame.USEREVENT + 2
DEATH_SOUND = pygame.mixer.Sound(os.path.join(SOUND_DIRECTORY, 'OOAAH.wav'))
JUMP_SOUND = pygame.mixer.Sound(os.path.join(SOUND_DIRECTORY, 'JUMP.wav'))
WIN_SOUNDS = pygame.mixer.Sound(os.path.join(SOUND_DIRECTORY, 'Dirladada RT.mp3'))

### ENEMY ###
ENEMY = pygame.image.load(os.path.join(PICTURE_DIRECTORY, 'CAT.png'))

### BULLET ###
BULLET = pygame.image.load(os.path.join(PICTURE_DIRECTORY, 'Bullet.png'))
BULLET_VELOCITY = 7
MAX_BULLETS = 3
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join(SOUND_DIRECTORY, 'Ahu.wav'))
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join(SOUND_DIRECTORY, 'P INAAL DINAK.wav'))


def draw_window(player, movement, bullets, enemy, player_score, player_health):
    WIN.blit(DESKTOP, (0, 0))
    WIN.blit(ENEMY, (enemy.x, enemy.y))

    if movement == 'right':
        WIN.blit(PLAYER_WALK, (player.x, player.y))

    if movement == 'left':
        WIN.blit(pygame.transform.flip(PLAYER_WALK, flip_x=True, flip_y=False), (player.x, player.y))

    if movement == 'jump':
        WIN.blit(PLAYER_JUMPING, (player.x, player.y - 30))

    for (bullet, movement) in bullets:
        if movement == 'right':
            WIN.blit(BULLET, bullet)

        if movement == 'left':
            WIN.blit(pygame.transform.flip(BULLET, flip_x=True, flip_y=False), bullet)

    score_text = SCORE_FONT.render(f"Score: {player_score}", 1, WHITE)
    health_text = SCORE_FONT.render(f"Life: {player_health}", 1, WHITE)

    WIN.blit(health_text, (0, 2))
    WIN.blit(score_text, (0, health_text.get_height() + 2))

    pygame.display.update()


def player_movement(keys_pressed, player):
    if keys_pressed[pygame.K_LEFT] and player.x > 0:
        player.x -= PLAYER_VELOCITY

    if keys_pressed[pygame.K_RIGHT] and (player.x + PLAYER_VELOCITY) < (WIDTH - PLAYER_WIDTH):
        player.x += PLAYER_VELOCITY

    if keys_pressed[pygame.K_UP] and (player.y - 2 * JUMP_FORCE) > 0 and \
            (player.y == LOWER_FLOOR_HEIGHT or player.y == 265):
        player.y -= 300
        JUMP_SOUND.play()

    if not keys_pressed[pygame.K_UP] and player.y < LOWER_FLOOR_HEIGHT:
        player.y += PLAYER_MASS


def generate_enemy_movement(amount_of_moves):
    moves = []
    directions = ['up', 'down', 'left', 'right', 'still']
    random_move = random.randint(0, len(directions) - 1)

    for _ in range(amount_of_moves):
        moves.append(directions[random_move])

    return moves


def enemy_movement(enemy, enemy_moves):
    for move in enemy_moves:
        if move == 'up' and enemy.y > 0:
            enemy.y -= 1

        if move == 'down' and enemy.y < HEIGHT - 100:
            enemy.y += 1

        if move == 'left' and enemy.x > 0:
            enemy.x -= 1

        if move == 'right' and enemy.x < WIDTH - 30:
            enemy.x += 1

        if move == 'still':
            pass




def get_player_movement(keys_pressed, player):
    if keys_pressed[pygame.K_LEFT] and player.x > 0:
        return 'left'

    if keys_pressed[pygame.K_RIGHT] and (player.x + PLAYER_VELOCITY) < (WIDTH - PLAYER_WIDTH):
        return 'right'

    if keys_pressed[pygame.K_UP] and (player.y - 2 * JUMP_FORCE) > 0:
        return 'jump'

    if not keys_pressed[pygame.K_UP] and player.y < LOWER_FLOOR_HEIGHT:
        return 'jump'


def handle_bullets(bullets, player, enemy):
    for (bullet, movement) in bullets:
        if movement == 'right':
            bullet.x += BULLET_VELOCITY

        if movement == 'left':
            bullet.x -= BULLET_VELOCITY

        if enemy.collidepoint(bullet.x, bullet.y):
            bullets.remove((bullet, movement))
            pygame.event.post(pygame.event.Event(PLAYER_HIT))

        if bullet.x < 0 or bullet.x > WIDTH + 20:
            bullets.remove((bullet, movement))


def write_result(text):
    to_draw = FINISH_FONT.render(text, 1, WHITE)
    WIN.blit(to_draw, (WIDTH // 2 - to_draw.get_width() // 2, HEIGHT // 2 - to_draw.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(5000)


def player_got_hit(player, enemy):
    if enemy.collidepoint(player.x, player.y):
        pygame.event.post(pygame.event.Event(PLAYER_DAMAGED))
        BULLET_HIT_SOUND.play()


def main():
    player = pygame.Rect(100, LOWER_FLOOR_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    enemy = pygame.Rect(600, LOWER_FLOOR_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)

    bullets = []
    player_score = 0
    player_health = 1

    pygame.mixer.music.play(loops=1000)
    clock = pygame.time.Clock()
    run = True
    movement = 'right'
    while run:
        WIN_SOUNDS.stop()
        clock.tick(FPS)
        keys_pressed = pygame.key.get_pressed()
        player_movement(keys_pressed, player)
        new_movement = get_player_movement(keys_pressed, player)

        enemy_move_amount = random.randint(1, 50)
        enemy_moves = generate_enemy_movement(enemy_move_amount)
        enemy_movement(enemy, enemy_moves)

        player_got_hit(player, enemy)
        if new_movement is not None:
            movement = new_movement

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if keys_pressed[pygame.K_SPACE] and len(bullets) < MAX_BULLETS:
                BULLET_FIRE_SOUND.play()
                if movement == 'left':
                    bullet = pygame.Rect(player.x - player.width // 2,
                                         player.y + player.height // 2 - 0.5 * BULLET.get_height(),
                                         BULLET.get_width(), BULLET.get_height())
                    bullets.append((bullet, movement))

                if movement == 'right':
                    bullet = pygame.Rect(player.x + player.width // 2,
                                         player.y + player.height // 2 - 0.5 * BULLET.get_height(),
                                         BULLET.get_width(), BULLET.get_height())
                    bullets.append((bullet, movement))

            if event.type == PLAYER_HIT:
                player_score += 1

            if event.type == PLAYER_DAMAGED:
                player_health -= 1

        text = ''
        if player_score >= 6:
            text = 'WINNER!!!'
            pygame.mixer.music.stop()
            WIN_SOUNDS.play()

        if player_health <= 0:
            text = 'LOL, you lose...'

        if text != '':
            write_result(text)
            break

        handle_bullets(bullets, player, enemy)

        draw_window(player, movement, bullets, enemy, player_score, player_health)

    main()


if __name__ == '__main__':
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("NK's desktop game :-) ")
    main()
