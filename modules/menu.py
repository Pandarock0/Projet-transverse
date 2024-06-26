import pygame
from modules import mapAndEnemies as me

WIDTH = 1100
LENGTH = 600

def Menu():
    button_group = pygame.sprite.Group()
    deco_group = pygame.sprite.Group()
    width, height = 250, 70
    center = WIDTH // 2
    button_group.add(Button("Tutorial", center, 250, width, height))
    button_group.add(Button("Level 1", center, 350, width, height))
    button_group.add(Button("Level 2", center, 450, width, height))
    button_group.add(Button("Level 3", center, 550, width, height))

    deco_group.add(me.Decoration( 150, 'owl_pres', 350))
    deco_group.add(me.Decoration(800, 'ordi', 290))
    deco_group.add(me.Decoration(50, 'endPoint', 50))
    return button_group, deco_group


class Button(pygame.sprite.Sprite):
    def __init__(self, display_txt: str, x, y, width, height, text_color='red'):
        super().__init__()
        self.display_txt = display_txt

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))

        pygame.draw.rect(self.image, (255, 255, 255), (0, 0, width, height), border_radius=25)

        self.font = pygame.font.Font('font/SuperMario256.ttf', 40)
        self.text_surface = self.font.render(display_txt, True, text_color)
        self.text_rect = self.text_surface.get_rect(center=(x,y+6))

    def update(self, screen):
        # Draw the background rectangle
        screen.blit(self.image, self.rect)

        # Draw the text on top of the background rectangle
        screen.blit(self.text_surface, self.text_rect)
        if self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            match self.display_txt:
                case 'Intro':
                    return 0
                case 'Level 1':
                    return 1
                case 'Level 2':
                    return 2
                case 'Level 3':
                    return 3
