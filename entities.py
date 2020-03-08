import pygame
import os


pygame.init()
STAT_FONT = pygame.font.SysFont("comicsans", 30)
GAME_OVER_FONT = pygame.font.SysFont("comicsans", 100)

#change these to change the game window sizing
WIN_WIDTH = 500 
WIN_HEIGHT = 600


class Entity:
    """
    Class to represent objects in the game
    """
    def __init__(self, x, y, image_surface, speed):
        self.x = x
        self.y = y
        self.img = image_surface
        self.active = False #for bullet only
        self.move_right = True #only use in alien object
        self.speed = speed

    def draw(self, pygame_window):
        pygame_window.blit(self.img, (self.x, self.y))
    
    def get_mask(self):
        return pygame.mask.from_surface(self.img)


class Alien(Entity):
    """
    Extends entity class to represent an alien
    """
    def move(self, win_width):
        if self.move_right:
            self.x += self.speed

        else:
            self.x -= self.speed
        
    def update(self, pygame_window, win_width):
        self.move(win_width)
        self.draw(pygame_window)
    
    def collide_bullet(self, bullet):
        alien_mask = self.get_mask()
        offset = (-1*(round(self.x)-bullet.x), -1*(round(self.y)- bullet.y))
        point = alien_mask.overlap(bullet.get_mask(), offset)
        if point:
            bullet.y = -20
        return point
    

class Bullet(Entity):
    """
    Extends bullet class to represent the bullet in the game
    """
    def set_pos(self, x, y):
        self.x = x
        self.y = y

    def move(self):
        if self.y < WIN_HEIGHT and self.y > 0:
            self.active = True
        else:
            self.active = False
        self.y -= self.speed
        
    def draw(self, window):
        self.move()
        if self.active:
            window.blit(self.img, (self.x, self.y))
        


class Game:
    """
    A game of space invaders
    """

    ALIEN_IMG = pygame.transform.scale(pygame.image.load(os.path.join('images', 'alien.png')), (35,25))
    PLAYER_IMG = pygame.transform.scale(pygame.image.load(os.path.join('images', 'player.png')), (42, 26))
    BULLET_IMG = pygame.transform.scale(pygame.image.load(os.path.join('images', 'bullet.png')), (6, 12))
    FPS = 60

    def __init__(self, win_width, win_height):
        
        self.win_width = win_width
        self.alien_speed = 0.5
        self.window = pygame.display.set_mode((win_width, win_height))
        self.game_over = False     
        self.player = Entity(win_width//2, win_height-50, self.PLAYER_IMG, 2)
        self.aliens = self.add_aliens()
        self.clock = pygame.time.Clock()
        self.bullet = Bullet(0,-1000, self.BULLET_IMG, 5)
        self.score = 0  
        

    def add_aliens(self):
        aliens = []
        y = 0
        for j in range(0,5):
            x = 0
            for i in range(0,9):
                aliens.append(Alien(x,y,self.ALIEN_IMG, self.alien_speed))
                x += 50
            y += 40
        return aliens  

    def alien_handling(self):
        for alien in self.aliens:    
            hit = alien.collide_bullet(self.bullet)
            if hit:
                self.aliens.remove(alien)
                self.score += 10
            alien.update(self.window, self.win_width)
            if alien.y >= self.player.y:
                self.game_over = True

        for alien in self.aliens:
            if alien.x < 0:
                for alien in self.aliens:
                    alien.move_right = True
                    alien.y += 8
                break
            elif alien.x > self.win_width-35:
                for alien in self.aliens:
                    alien.move_right = False
                break
        if len(self.aliens) == 0:
            self.alien_speed += 0.5
            self.aliens = self.add_aliens()
        

    def draw(self):
        self.window.fill((0,0,0))
        score_text = STAT_FONT.render("Score: " + str(self.score), 1, (255,255,255))
        self.window.blit(score_text, (self.win_width-10-score_text.get_width(), WIN_HEIGHT-20))
        self.player.draw(self.window)
        self.bullet.draw(self.window)
        self.alien_handling()
        pygame.display.update()


    def input_handling(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if not self.bullet.active:
                self.bullet.set_pos(self.player.x+21, self.player.y)
        if keys[pygame.K_LEFT]:
            self.player.x -= self.player.speed
        elif keys[pygame.K_RIGHT]:
            self.player.x += self.player.speed
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True

    def game_over_screen(self):
        self.window.fill((0,0,0))
        text = GAME_OVER_FONT.render("GAME OVER", 1, (255, 255, 255))
        self.window.blit(text, (((WIN_WIDTH-text.get_width())//2, WIN_HEIGHT//2+10)))  
        pygame.display.update()
    

    def run(self):
        while not self.game_over:
            self.input_handling()
            self.draw()
            self.clock.tick(self.FPS)
        while self.game_over:
            self.game_over_screen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    
    
        
                 
