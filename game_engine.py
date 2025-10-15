import pygame
from .paddle import Paddle
from .ball import Ball

WHITE = (255, 255, 255)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 30)

        # --- ADDED: Game state and winning logic ---
        self.WINNING_SCORE = 5
        self.game_over = False
        self.winner_text = ""
        self.game_over_font = pygame.font.SysFont("Arial", 50)
        
        # Load sound files
        self.collision_sound = pygame.mixer.Sound("sounds/paddle_hit.wav")
        self.win_sound = pygame.mixer.Sound("sounds/score.wav")
        self.wall_sound = pygame.mixer.Sound("sounds/wall_bounce.wav")
        
    def handle_input(self):
        # Only allow paddle movement if the game is not over
        if not self.game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                self.player.move(-self.player.speed, self.height)
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                self.player.move(self.player.speed, self.height)

    # --- THIS IS THE MISSING FUNCTION ---
    # It handles single events like restarting the game
    def handle_event(self, event):
        if self.game_over and event.type == pygame.KEYDOWN:
           if event.key == pygame.K_SPACE:
            # Show replay menu
               self.replay_menu(pygame.display.get_surface())


    def update(self):
        # Only update game objects if the game is not over
        if not self.game_over:
            self.ball.move()
            
            if self.ball.check_collision(self.player, self.ai):
                self.collision_sound.play()

            if self.ball.x + self.ball.width <= 0:
                self.ai_score += 1
                self.ball.reset()
                self.wall_sound.play()
                self.check_for_winner()
                
            elif self.ball.x >= self.width:
                self.player_score += 1
                self.ball.reset()
                self.win_sound.play()
                self.check_for_winner()

            self.ai.auto_track(self.ball, self.height)

    # --- ADDED: Checks for a winner ---
    def check_for_winner(self):
        if self.player_score >= self.WINNING_SCORE:
            self.winner_text = "Player Wins!"
            self.game_over = True
        elif self.ai_score >= self.WINNING_SCORE:
            self.winner_text = "AI Wins!"
            self.game_over = True
    
    # --- ADDED: Resets the game to its initial state ---
    def reset_game(self):
        self.player_score = 0
        self.ai_score = 0
        self.ball.reset()
        self.game_over = False
        self.winner_text = ""

    def render(self, screen):
        # Always render the paddles, ball, and scores
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width//4 - player_text.get_width()//2, 20))
        screen.blit(ai_text, (self.width * 3//4 - ai_text.get_width()//2, 20))

        # Render the game over screen if the game has ended
        if self.game_over:
            winner_render = self.game_over_font.render(self.winner_text, True, WHITE)
            screen.blit(winner_render, (self.width//2 - winner_render.get_width()//2, self.height//2 - 50))
            
            prompt_render = self.font.render("Press SPACE to Play Again", True, WHITE)
            screen.blit(prompt_render, (self.width//2 - prompt_render.get_width()//2, self.height//2 + 20))

    def replay_menu(self, screen):
        menu_font = pygame.font.SysFont("Arial", 40)
        prompt_font = pygame.font.SysFont("Arial", 30)
        options = ["3: Best of 3", "5: Best of 5", "7: Best of 7", "ESC: Exit"]
        screen.fill((0, 0, 0))
        for i, option in enumerate(options):
            text = menu_font.render(option, True, (255, 255, 255))
            screen.blit(text, (self.width//2 - text.get_width()//2, 150 + i * 60))
        prompt = prompt_font.render("Press the corresponding key to select", True, (255, 255, 255))
        screen.blit(prompt, (self.width//2 - prompt.get_width()//2, 100))
    
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                   pygame.quit()
                   exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_3:
                       self.WINNING_SCORE = 3
                       waiting = False
                    elif event.key == pygame.K_5:
                       self.WINNING_SCORE = 5
                       waiting = False
                    elif event.key == pygame.K_7:
                       self.WINNING_SCORE = 7
                       waiting = False
                    elif event.key == pygame.K_ESCAPE:
                       pygame.quit()
                       exit()
    
    # Reset the game after choosing
        self.reset_game()
