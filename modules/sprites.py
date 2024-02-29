import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((45, 70))
        self.image.fill('Red')
        self.rect = self.image.get_rect(midbottom=(550,400))

        self.xmap = 0
        self.smooth_cam = 5
        self.gravity = 0
        self.game_active =True

        self.wall_shift = 0
        self.wall_shift_to_left = bool



    def input_jumping(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.gravity = -20
            return True
        else:
            self.gravity = 0
            return False
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom > 800:
            self.destroy()
    def destroy(self):
        self.game_active = False
        self.kill()

    def walking(self, left, right):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and left:
            if self.rect.x -5 <= 450:
                if self.smooth_cam:
                    self.smooth_cam -= 1
                    self.xmap -= 3
                    self.rect.x -=2
                else:
                    self.xmap -= 5

            else:
                self.smooth_cam = 5
                self.rect.x -= 5
        if keys[pygame.K_RIGHT] and right:
            if self.rect.x + 5 >= 650:
                self.xmap += 5
            else:
                self.rect.x += 5

    def moving(self,collide_map):
        left, right = True, True
        if self.wall_shift:
            if self.wall_shift_to_left:
                self.rect.x -= 5
                self.wall_shift -=1
            else:
                self.rect.x += 5
                self.wall_shift -= 1
            if self.wall_shift>10:
                left,right = False,False
        else:
            if collide_map:
                if self.rect.bottom <= collide_map.get_height() + 30:
                    if self.gravity > 28:
                        self.destroy()
                    self.rect.bottom = collide_map.get_height() + 1
                    self.input_jumping()
                else:
                    if self.rect.center < collide_map.get_center():
                        right = False
                        self.gravity = 3
                        if self.input_jumping():
                            self.wall_shift = 20
                            self.rect.x -= 5
                            self.wall_shift_to_left = True
                    else:
                        left = False
                        self.gravity = 3
                        if self.input_jumping():
                            self.wall_shift = 20
                            self.rect.x += 5
                            self.wall_shift_to_left = False

        self.apply_gravity()
        self.walking(left,right)

    def update(self,collide_map):
        self.moving(collide_map)
        return (self.xmap, self.game_active)
    def get_bottom(self):
        return self.rect.bottom
    def forced_jump(self):
        # applyed when you kill an enemy
        self.gravity=-20
    def rebond(self):
        # applyed when you kill an enemy
        self.gravity=-10

class Map(pygame.sprite.Sprite):
    def __init__(self, begin_coordinate, end_coordinate, height=400):
        super().__init__()
        self.begin = begin_coordinate
        self.end = end_coordinate
        self.image = pygame.Surface((self.end - self.begin, 400))
        self.image.fill('Green')
        self.rect = self.image.get_rect(topleft=(self.begin, height))
        self.height = height

    def get_center(self):
        return self.rect.center
    def get_height(self):
        return self.height
    def update(self,xmap):
        self.rect.x = self.begin - xmap


class Enemy(pygame.sprite.Sprite):
    def __init__(self, min_x,max_x, type='big', height=400):
        super().__init__()
        if type == 'big':
            self.image = pygame.Surface((25, 50))
            self.image.fill('Blue')
        elif type == 'small':
            self.image = pygame.Surface((25, 25))
            self.image.fill('Pink')
        self.rect = self.image.get_rect(bottomleft=((min_x+max_x)//2, height))

        self.min_x = min_x
        self.max_x = max_x
        self.moving_side = 1
        self.x_map = 0
        # x_pos is the theorical position, whithout considering the map movement
        self.x_pos = (min_x+max_x)//2

    def moving(self):
        if self.rect.left< self.min_x-self.x_map:
            self.moving_side = 1
        if self.rect.right> self.max_x-self.x_map:
            self.moving_side = -1
        self.x_pos += self.moving_side* 2
        self.rect.x = self.x_pos - self.x_map
    def update(self, x_map):
        self.x_map = x_map
        self.moving()
    def get_top(self):
        return self.rect.top
