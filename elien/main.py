import sys
import pygame
from setting import Setting
from ship import ship
from bullet import bullet
from alien import alien

class ai:

    def __init__(self):
        pygame.init()
        self.setting=Setting()
        self.screen=pygame.display.set_mode((self.setting.screen_width,self.setting.screen_height))
        pygame.display.set_caption("Alien Invasion")
        self.ship=ship(self)
        self.bullets=pygame.sprite.Group()
        self.aliens=pygame.sprite.Group()
        self._creat_fleet()

    def run_game(self):
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullet()
            self._update_aliens()
            self._update_screen()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type==pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type==pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self,event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        if event.key == pygame.K_q:
            sys.exit()
        if event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self,event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y+=self.setting.fleet_drop_speed
        self.setting.fleet_direction*=-1

    def _fire_bullet(self):
        new_bullet=bullet(self)
        self.bullets.add(new_bullet)

    def _update_bullet(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        collision=pygame.sprite.groupcollide(self.bullets,self.aliens,True,True)
        if not self.aliens:
            self.bullets.empty()
            self._creat_fleet()

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            print("Game Over!!!")

    def _creat_fleet(self):
        Alien=alien(self)
        Alien_width=Alien.rect.width
        Alien_height=Alien.rect.height
        avail_space_x=self.setting.screen_width-(2*Alien_width)
        number_alien_x=avail_space_x //(2*Alien_width)
        ship_height=self.ship.rect.height
        avail_space_y=(self.setting.screen_height-3*Alien_height-ship_height)
        number_rows=avail_space_y//(2*Alien_height)
        for row_number in range(number_rows):
            for alien_number in range(number_alien_x):
                self._creat_alien(alien_number,row_number)

    def _creat_alien(self,alien_number,row_number):
        Alien = alien(self)
        Alien_width,Alien_height=Alien.rect.size
        alien.x = Alien_width + 2 * Alien_width * alien_number
        Alien.rect.x = alien.x
        Alien.rect.y=Alien.rect.height+2*Alien.rect.height*row_number
        self.aliens.add(Alien)

    def _update_screen(self):
        self.screen.fill(self.setting.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        pygame.display.flip()

if __name__=='__main__':
    ai=ai()
    ai.run_game()
