import sys, pygame

from time import sleep


from explosion import Explosion
from settings import Settings
from ship import Ship
from bullet import Bullet, AlienBullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

class AlienInvasion:
    """Overall class to manage game assets and behavior."""
    def __init__(self):
        """Initialize the game and create game resources."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        
        pygame.display.set_caption("Alien Invasion")
        
        # Create an instance to store game stats and create a scoreboard
        self.stats = GameStats(self)   
        self.sb = Scoreboard(self) 

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self.alien_bullets = pygame.sprite.Group()

        self._create_fleet()

        

        # Make the Play button.
        self.play_button = Button(self, "Play")

        # Make difficulty level buttons.
        self._make_difficulty_buttons()  

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                self._update_alien_bullets()
                self.explosions.update()
            
            self._update_screen()

    def _start_game(self):
        # Reset the game settings.
        self.settings.initialize_dynamic_settings()

        # Reset statistics
        self.stats.reset_stats()
        self.stats.game_active = True
        self.stats.boss_beaten = False

        self.alien_shoot = pygame.USEREVENT + 0

        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ships()

        # Get rid of any remaining aliens and bullets.
        self.aliens.empty()
        self.bullets.empty()
        self.alien_bullets.empty()

        # Create a new fleet and center the ship
        self._create_fleet()
        self.ship.center_ship()

        # Play the game music
        self.game_music = pygame.mixer.music.load('Sounds\game_music.mp3')
        pygame.mixer.music.play(-1)         

        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)

        # Pause for the music countdown
        sleep(2.0)             

    def _make_difficulty_buttons(self):
        """Make buttons that allow player to select difficulty level."""
        self.rookie_button =  Button(self, "Rookie")
        self.hero_button = Button(self, "Hero")
        self.veteran_button = Button(self, "Veteran")
 
        # Position buttons so they are inline and under the play button.
        self.rookie_button.rect.right = (
            self.hero_button.rect.left - 0.5 * self.play_button.rect.width)
        self.rookie_button.rect.top = (
            self.play_button.rect.bottom + 0.5 * self.play_button.rect.height)
        self.rookie_button._update_msg_position()

        self.hero_button.rect.top = (
            self.play_button.rect.bottom + 0.5 * self.rookie_button.rect.height)
        self.hero_button._update_msg_position()

        self.veteran_button.rect.left = (
            self.hero_button.rect.right + 0.5 * self.hero_button.rect.width)
        self.veteran_button.rect.top = (
            self.play_button.rect.bottom + 0.5 * self.hero_button.rect.height)
        self.veteran_button._update_msg_position()

   
    
    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                self._check_difficulty_buttons(mouse_pos) 
            
            elif self.stats.game_active == True:
                if event.type == self.alien_shoot:
                    self._fire_alien_bullet()

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self._start_game()

    def _check_difficulty_buttons(self, mouse_pos):
        """
        Set difficulty based on user selection and highlight 
        the selected difficulty button.
        """
        rookie_button_clicked = self.rookie_button.rect.collidepoint(
            mouse_pos)
        hero_button_clicked = self.hero_button.rect.collidepoint(
            mouse_pos)
        veteran_button_clicked = self.veteran_button.rect.collidepoint(
            mouse_pos)

        if rookie_button_clicked:
            self.settings.difficulty_level = 'rookie'
            self.hero_button._reset_button_color()
            self.veteran_button._reset_button_color()
            self.rookie_button._change_button_color()
         

        elif hero_button_clicked:
            self.settings.difficulty_level = 'hero'
            self.rookie_button._reset_button_color()
            self.veteran_button._reset_button_color()
            self.hero_button._change_button_color()

        elif veteran_button_clicked:
            self.settings.difficulty_level = 'veteran' 
            self.rookie_button._reset_button_color()
            self.hero_button._reset_button_color()
            self.veteran_button._change_button_color()        
    
    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
                self._exit_game()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()     

    def _check_keyup_events(self, event):
        """Respond to key releases"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        
    def _fire_alien_bullet(self):
        """Create a new bullet and add it  to the bullet group."""
        for alien in self.aliens.sprites():
            if len(self.alien_bullets) < self.settings.alien_bullets_allowed:
                new_bullet = AlienBullet(alien.rect.centerx, alien.rect.centery)
                self.alien_bullets.add(new_bullet)
            
    def _update_alien_bullets(self):
        """Update the position of bullets  and remove old bullets."""
        # Update bullet positions.
        self.alien_bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.alien_bullets.copy():
            if bullet.rect.bottom >= self.settings.screen_bottom:
                self.alien_bullets.remove(bullet)

        self._check_bullet_ship_collisions()
    
    def _fire_bullet(self):
        """Create a new bullet and add it  to the bullet group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            
    def _update_bullets(self):
        """Update the position of bullets  and remove old bullets."""
        # Update bullet positions.
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()
        
    def _check_bullet_ship_collisions(self):
        """Respond to bullet_ship collisions."""
        # Sound for when an alien ship is hit by a lazer
        self.ship_hit = pygame.mixer.Sound('Sounds/alien_explode.wav')
        self.ship_crash = pygame.mixer.Sound('Sounds/ship_crash.wav')
                   
        # If more than one ship left and ship health > 1 lower ship health by 
        # one. Else, lower ships_left by one and prep a new ship.
        if self.stats.ships_left >= 1:
            if self.settings.ship_health > 1:
              
                collisions = pygame.sprite.spritecollide(
                    self.ship, self.alien_bullets, True, 
                    pygame.sprite.collide_mask)
                if collisions:
                    self.ship_hit.play()
                    self.settings.ship_health -= 1
                    exp = Explosion(self.ship.rect.centerx, self.ship.rect.centery, 1)
                    self.explosions.add(exp) 
            else:
                # Decrement ships left, update scoreboard.
                collisions = pygame.sprite.spritecollide(
                    self.ship, self.alien_bullets, True, 
                    pygame.sprite.collide_mask)
                if collisions:
                    exp = Explosion(self.ship.rect.centerx, self.ship.rect.centery, 3)
                    self.explosions.add(exp) 
                    self.ship_hit.play()
                    self.stats.ships_left -= 1
                    self.ship_crash.play()
                    self.sb.prep_ships()
                    self.settings.ship_health = 5
        else:
            if self.settings.ship_health > 1: 
              
                collisions = pygame.sprite.spritecollide(
                    self.ship, self.alien_bullets, True, 
                    pygame.sprite.collide_mask)
                if collisions:
                    self.ship_hit.play()
                    self.settings.ship_health -= 1
                    exp = Explosion(self.ship.rect.centerx, self.ship.rect.centery, 1)
                    self.explosions.add(exp) 
            else:
                # for bullet in self.alien_bullets:
                collisions = pygame.sprite.spritecollide(
                    self.ship, self.alien_bullets, True, 
                    pygame.sprite.collide_mask)
                if collisions:
                    self.ship_crash.play()
                    exp = Explosion(self.ship.rect.centerx, self.ship.rect.centery, 3)
                    self.explosions.add(exp)                    
                    self.stats.boss_beaten = False
                    self.settings.alien_health = 1
                    pygame.time.set_timer(self.alien_shoot, 0)
                    pygame.mixer.music.stop()
                    self.game_over = pygame.mixer.Sound('Sounds/game_over.wav')
                    self.game_over.play()

                    # Check/update high score, and set game_active to false
                    self.stats._check_high_score()
                    self.stats.game_active = False
                    pygame.mouse.set_visible(True)
   
    def _check_bullet_alien_collisions(self):
        """Respond to bullet_alien collisions."""
        # Sound for when an alien ship is hit by a lazer
        self.alien_hit = pygame.mixer.Sound('Sounds/alien_explode.wav')

        # If the alien's health is greater than one, add score and lower alien 
        # health by 1 but do not kill the sprite
        if self.settings.alien_health > 1:    
            collisions = pygame.sprite.groupcollide(
                self.bullets, self.aliens, True, False, 
                pygame.sprite.collide_mask)
            if collisions:
                for aliens in collisions.values():
                    self.stats.score += self.settings.alien_points * len(aliens)
                self.alien_hit.play()
                self.sb.prep_score()
                self.sb.check_high_score()
                self.settings.alien_health -= 1
        # If alien health is lower than one, kill the sprite and add score.
        else: 
            # If the alien is a regular alien, play the smaller explosion
            if self.stats.boss_beaten == False:
                for bullet in self.bullets:
                    if pygame.sprite.spritecollide(bullet, self.aliens, True):
                        bullet.kill()
                        exp = Explosion(bullet.rect.centerx, bullet.rect.centery, 2)
                        self.explosions.add(exp)
                        self._score_alien()       
            # If the alien is the boss, play the larger explosion
            if self.stats.boss_beaten == True:
                for bullet in self.bullets:
                    if pygame.sprite.spritecollide(bullet, self.aliens, True):
                        bullet.kill()
                        exp = Explosion(bullet.rect.centerx, bullet.rect.centery, 3)
                        self.explosions.add(exp)
                        self._score_alien()
        # When aliens sprite group is empty the game spawns the boss if 
        # boss_beaten flag is false. Once boss is beaten, boss_beaten flag is 
        # set to true and the next level begins
        if not self.aliens: 
            if not self.stats.boss_beaten:
                self._start_boss_fight()
            if self.stats.boss_beaten and not self.explosions:
                self._start_next_level()  

    def _score_alien(self):
        """
        Increase the score for each alien shot, check the high score, 
        and reset the alien's health
        """
        self.stats.score += self.settings.alien_points * 1
        self.alien_hit.play()
        self.sb.prep_score()
        self.sb.check_high_score()
        self.settings.alien_health = 0

    def _start_next_level(self):
        """
        Method that empties bullets, creates a new fleet, increases speed, 
        resets the boss_beaten flag, and increments the level indicators
        """
        # Empty sprite groups and wait one second before starting the next level
        self.aliens.empty()
        self.bullets.empty()
        self.alien_bullets.empty()
        sleep(1)
        self._create_fleet()
        self.settings.increase_speed()

        #Increase level.
        self.stats.level += 1
        self.sb.prep_level()
        self.stats.boss_beaten = False

    def _start_boss_fight(self):
        """Method that creates the boss preps/starts the boss fight"""
        # Empty sprite groups, prep the boss health, and create the boss.
        self.stats.boss_beaten = True  
        if self.stats.game_active and self.stats.boss_beaten:
            pygame.time.set_timer(self.alien_shoot, 2000)
            self.aliens.empty()
            self.bullets.empty()
            self._create_boss_alien()
            self.settings.alien_health = 5
             

    def _update_aliens(self):
        """
        Check if the fleet is at an edge, 
        then update the position of all aliens in the fleet.
        """
        self._check_fleet_edges()
        self.aliens.update()
        
        
        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0:
            # Play Ship Collision sound
            self.ship_crash = pygame.mixer.Sound('Sounds/ship_crash.wav')
            self.ship_crash.play()
            # Decrement ships left, update scoreboard.
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Pause.
            sleep(0.5)
        else:
            # Stop the game music and play 'ship crash' and 'game over' sound
            self.stats.boss_beaten == False
            pygame.mixer.music.stop()
            self.ship_crash.play()
            self.game_over = pygame.mixer.Sound('Sounds/game_over.wav')
            self.game_over.play()

            # Check/update high score, and set game_active to false
            self.stats._check_high_score()
            self.stats.game_active = False
            pygame.mouse.set_visible(True)


    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break

    def _create_fleet(self):
        """Create a fleet of aliens."""   
       
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Determine the number of aliens that fit on the screen.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - 
                                (2 * alien_height) - ship_height)
        number_rows = available_space_y // (4 * alien_height)

        # Create the full fleet of aliens.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):    
                self._create_alien(alien_number, row_number)        
    
    def _create_alien(self, alien_number, row_number):
        """Create an alien and place it in a row."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.y = alien_height + 2 * alien_height * row_number
        alien.rect.x = alien.x
        alien.rect.y = alien.y  
        self.aliens.add(alien)
        
    def _create_boss_alien(self):
        """Create a boss alien"""
        self.boss = Alien(self)
        self.boss._change_alien_image()
        self.aliens.add(self.boss)


    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """Update images on the screen and flip to the new screen."""
        # Redraw the screenduring each pass through the loop.
        self.screen.blit(self.settings.bg, self.settings.bg_rect)
        self.ship.blitme()
        self.alien_bullets.draw(self.screen)
        self.bullets.draw(self.screen)
        self.aliens.draw(self.screen)
        self.explosions.draw(self.screen)

        # Draw score information
        self.sb.show_score()
        
        # Draw the game buttons if the game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()
            self.rookie_button.draw_button()
            self.hero_button.draw_button()
            self.veteran_button.draw_button()       

        # Make the most recently drawn screen visible.
        pygame.display.flip()

    def _exit_game(self):
        """Save the high score and exit the game using sys.exit()."""
        self.stats._check_high_score()
        sys.exit()


if __name__ == '__main__':
    # Make a game instance and run the game. 
    ai = AlienInvasion()
    ai.run_game()