import pygame, sys
from pygame import gfxdraw
import random

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
clock = pygame.time.Clock()

screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pong")


ball = pygame.Rect(screen_width/2 - 15, screen_height/2 - 15, 30, 30)
player = pygame.Rect(screen_width - 20, screen_height/2 - 150, 10, 140)
opponent = pygame.Rect(10, screen_height/2 - 150, 10, 140)
score_bg = pygame.Rect(screen_width/2 - 50, screen_height - 60, 100, 40)



bg_color = pygame.Color("grey12")
light_grey = (200, 200, 200)


ball_speed_x = 7
ball_speed_y = 7
player_speed = 0
opponent_speed = 7


player_score = 0
opponent_score = 0 
game_font = pygame.font.Font("freesansbold.ttf", 30)


pong_sound = pygame.mixer.Sound("pong.ogg")
score_sound = pygame.mixer.Sound("score.ogg")


game_over = False



def ball_animation():
    global ball_speed_x, ball_speed_y, player_score, opponent_score

    if ball.top <= 0 or ball.bottom >= screen_height - 80:
        pygame.mixer.Sound.play(pong_sound)
        ball_speed_y *= -1
    if ball.left <= 0:
        pygame.mixer.Sound.play(score_sound)
        player_score += 1
        ball_restart()
    elif ball.right >= screen_width:
        pygame.mixer.Sound.play(score_sound)
        opponent_score += 1
        ball_restart()

    if ball.colliderect(player) and ball_speed_x > 0:
        pygame.mixer.Sound.play(pong_sound)
        if abs(ball.right - player.left) < 10: 
            ball_speed_x *= -1
        elif abs(ball.bottom - player.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - player.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1

    if ball.colliderect(opponent) and ball_speed_x < 0:
        pygame.mixer.Sound.play(pong_sound)
        if abs(ball.left - opponent.right) < 10: 
            ball_speed_x *= -1
        elif abs(ball.bottom - opponent.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - opponent.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1

    ball.x += ball_speed_x
    ball.y += ball_speed_y


def player_animation():
    player.y += player_speed

    if player.top <= 10:
        player.top = 10
    if player.bottom >= screen_height - 90:
        player.bottom = screen_height - 90


def opponent_ai():
    if opponent.top < ball.y:
        opponent.top += opponent_speed
    if opponent.bottom > ball.y:
        opponent.bottom -= opponent_speed
    if opponent.top <= 10:
        opponent.top = 10
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height


def ball_restart():
    global ball_speed_x, ball_speed_y

    ball.center = (screen_width/2, screen_height/2)
    ball_speed_y *= random.choice((1, -1))
    ball_speed_x *= random.choice((1, -1))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif opponent_score >= 6:
            game_over = True
        elif  player_score >= 6:
            game_over = True 

        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed += 7
            if event.key == pygame.K_UP:
                player_speed -= 7

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_speed -= 7
            if event.key == pygame.K_UP:
                player_speed += 7
    

    if not game_over:

        ball_animation()
        player_animation()
        opponent_ai()


        screen.fill(bg_color)
        pygame.draw.rect(screen, light_grey, player)
        pygame.draw.rect(screen, light_grey, opponent)
        pygame.draw.ellipse(screen, light_grey, ball)
        pygame.draw.aaline(screen, light_grey, (screen_width/2, 0), (screen_width/2, screen_height - 80))
        pygame.draw.aaline(screen, light_grey, (0, screen_height - 80), (screen_width, screen_height - 80))


        pygame.draw.rect(screen, light_grey, score_bg)
        pygame.draw.aaline(screen, bg_color, (screen_width/2, screen_height - 70), (screen_width/2, screen_height))

        player_text = game_font.render(f"{player_score}", True, bg_color)
        screen.blit(player_text, (screen_width/2 + 18, screen_height - 53))
        opponent_text = game_font.render(f"{opponent_score}", True, bg_color)
        screen.blit(opponent_text, (screen_width/2 - 33, screen_height - 53))

    elif game_over:
        if player_score > opponent_score:
            text = game_font.render(f"Game Over, Player won with {player_score} scores", True, light_grey)
            text_rect = text.get_rect()
            text_x = screen.get_width() / 2 - text_rect.width / 2
            text_y = screen.get_height() / 2 - text_rect.height / 2
            screen.blit(text, [text_x, text_y])
        elif player_score < opponent_score:
            text = game_font.render(f"Game Over, AI won with {opponent_score} scores", True, light_grey)
            text_rect = text.get_rect()
            text_x = screen.get_width() / 2 - text_rect.width / 2
            text_y = screen.get_height() / 2 - text_rect.height / 2
            screen.blit(text, [text_x, text_y])
        else:
            text = game_font.render("Game Over, TIE", True, light_grey)
            text_rect = text.get_rect()
            text_x = screen.get_width() / 2 - text_rect.width / 2
            text_y = screen.get_height() / 2 - text_rect.height / 2
            screen.blit(text, [text_x, text_y])



    clock.tick(60)
    pygame.display.flip()
    