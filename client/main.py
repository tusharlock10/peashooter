import pygame
from bullet import Bullet
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from network import ClientNetwork
from spaceship import Spaceship

# Initialize Pygame
pygame.init()

# Screen dimensions
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Multiplayer Shooter Game")


def parse_game_events(data):
    print("Got data :: ", data)


# Networking setup for UDP
network = ClientNetwork()
network.create_connection()
network.receive_data(parse_game_events)


def main():
    global last_bullet_time, last_position
    clock = pygame.time.Clock()

    running = True

    # Spaceship
    ship = Spaceship(0)

    # Bullets
    bullets = []
    last_bullet_time = 0
    last_position = (ship.x, ship.y)

    while running:
        clock.tick(45)  # 45 frames per second
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        ship.move(keys)

        movement = (ship.x, ship.y) != last_position
        shooting = False

        if keys[pygame.K_SPACE] and current_time - last_bullet_time > 500:
            x, y = ship.get_position()
            x += ship.width // 2
            y += ship.height // 2
            bullet_direction = [0, -1]  # Default up
            bullet_color = ship.get_darker_color()
            bullets.append(Bullet(x, y, 7, bullet_color, bullet_direction))
            last_bullet_time = current_time
            shooting = True

        # Send data to the server only if there's movement or shooting
        if movement or shooting:
            data = f"{network.client_id},{ship.get_data()}"
            network.send_data(data)
            last_position = (ship.x, ship.y)

        win.fill((173, 216, 230))  # Light blue background
        ship.draw(win)
        for bullet in bullets[:]:
            bullet.move()
            bullet.draw(win)
            if bullet.off_screen(SCREEN_WIDTH, SCREEN_HEIGHT):
                bullets.remove(bullet)

        pygame.display.update()

    pygame.quit()
    network.close()


if __name__ == "__main__":
    main()
