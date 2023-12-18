import pygame
from bullet import Bullet
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, NetworkEvents
from network import ClientNetwork
from spaceship import Spaceship

# Initialize Pygame
pygame.init()

# Screen dimensions
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Multiplayer Shooter Game")

ship = Spaceship(0)
other_ships = {}
other_bullets = []


def handle_ship_id(data):
    global ship

    ship_id = data["value"]
    ship = Spaceship(ship_id)


def handle_new_ships(data):
    global other_ships

    ship_id = data["value"]
    new_ship = Spaceship(ship_id)
    other_ships[ship_id] = new_ship


def handle_ship_position_change(data):
    global other_ships

    value = data["value"]
    ship_id = value["ship_id"]
    other_ship = other_ships[ship_id]
    other_ship.set_health(value["health"])
    other_ship.set_position(value["x"], value["y"])


def handle_create_bullet(data):
    global other_bullets

    value = data["value"]
    bullet = Bullet(
        ship_id=value["ship_id"],
        x=value["x"],
        y=value["y"],
        direction=value["direction"],
    )
    other_bullets.append(bullet)


def parse_game_events(data):
    global ship

    print("Got data :: ", data)
    if data["type"] == NetworkEvents.SHIP_ID.value["type"]:
        handle_ship_id(data)

    if data["type"] == NetworkEvents.NEW_SHIP.value["type"]:
        handle_new_ships(data)

    if data["type"] == NetworkEvents.CHANGE_POSITION.value["type"]:
        handle_ship_position_change(data)

    if data["type"] == NetworkEvents.CREATE_BULLET.value["type"]:
        handle_create_bullet(data)


# Networking setup for UDP
network = ClientNetwork()
network.create_connection()
network.receive_data(parse_game_events)


def main():
    global last_bullet_time, last_position
    clock = pygame.time.Clock()

    running = True

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

        if keys[pygame.K_SPACE] and current_time - last_bullet_time > 500:
            bullet = ship.create_bullet()
            bullets.append(bullet)
            last_bullet_time = current_time

            data = bullet.create_bullet_network_event()
            network.send_data(data)

        # Send data to the server only if there's movement or shooting
        if movement:
            data = ship.change_position_network_event()
            network.send_data(data)
            last_position = (ship.x, ship.y)

        win.fill((173, 216, 230))  # Light blue background
        ship.draw(win)
        for bullet in bullets:
            bullet.move()
            bullet.draw(win)
            if bullet.off_screen(SCREEN_WIDTH, SCREEN_HEIGHT):
                bullets.remove(bullet)

        for bullet in other_bullets:
            bullet.move()
            bullet.draw(win)
            if bullet.off_screen(SCREEN_WIDTH, SCREEN_HEIGHT):
                other_bullets.remove(bullet)

        for other_ship in other_ships.values():
            other_ship.draw(win)

        pygame.display.update()

    pygame.quit()
    network.close()


if __name__ == "__main__":
    main()
