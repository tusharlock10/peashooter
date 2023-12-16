import socket
import threading

import pygame

from bullet import Bullet
from spaceship import Spaceship

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Multiplayer Shooter Game")

# Networking setup for UDP
server_ip = "127.0.0.1"  # Server's IP address
server_port = 5555  # Server's port
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
other_ships = {}


def receive_messages():
    while True:
        try:
            data, _ = client.recvfrom(1024)
            data = data.decode()
            update_other_ships(data)
        except Exception as e:
            print(f"Error receiving data: {e}")
            break


def update_other_ships(data):
    global other_ships
    ships = data.split("|")
    for ship_data in ships:
        ship_id, x, y = ship_data.split(",")
        other_ships[int(ship_id)] = (float(x), float(y))


# Spaceship settings
ship_color = (255, 0, 0)  # Red color
ship = Spaceship(WIDTH // 2, HEIGHT // 2, 50, 50, ship_color, WIDTH, HEIGHT)

# Bullets
bullets = []
last_bullet_time = 0
last_position = (ship.x, ship.y)

# Start listening for messages
thread = threading.Thread(target=receive_messages)
thread.start()


def main():
    global last_bullet_time, last_position
    clock = pygame.time.Clock()

    running = True
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
            data = f"{id(client)},{ship.get_data()}"
            client.sendto(data.encode(), (server_ip, server_port))
            last_position = (ship.x, ship.y)

        win.fill((173, 216, 230))  # Light blue background
        ship.draw(win)
        for bullet in bullets[:]:
            bullet.move()
            bullet.draw(win)
            if bullet.off_screen(WIDTH, HEIGHT):
                bullets.remove(bullet)

        # Draw other ships
        for ship_id, (x, y) in other_ships.items():
            if ship_id != id(client):  # Don't draw own ship
                pygame.draw.rect(win, (0, 255, 0), (x, y, 50, 50))

        pygame.display.update()

    pygame.quit()
    client.close()


if __name__ == "__main__":
    main()
