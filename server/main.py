from constants import NetworkEvents
from network import ServerNetwork

available_ids = set([0, 1, 2, 3, 4])
used_ids = {}


def should_connect(network, client):
    global available_ids

    if not len(available_ids):
        event = NetworkEvents.SHIP_ID.value
        network.enc_and_send_data(event, client)
        return False
    return True


def on_connect(network, client):
    global available_ids, used_ids

    ship_id = available_ids.pop()
    used_ids[client] = ship_id

    event = NetworkEvents.SHIP_ID.value
    event["value"] = ship_id
    network.enc_and_send_data(event, client)

    event = NetworkEvents.NEW_SHIP.value
    event["value"] = ship_id
    network.enc_and_broadcast_data(event, [client])


def on_disconnect(network, client):
    global available_ids, used_ids

    ship_id = used_ids[client]
    available_ids.add(ship_id)
    del used_ids[client]

    event = NetworkEvents.REMOVE_SHIP.value
    event["value"] = ship_id
    network.enc_and_broadcast_data(event, [client])


def start_server():
    network = ServerNetwork(
        should_connect=should_connect,
        on_connect=on_connect,
        on_disconnect=on_disconnect,
    )
    network.create_server()

    print(
        f"[LISTENING] Server is listening on {network.server_ip}:{network.server_port}"
    )

    while True:
        data, client = network.wait_for_data()
        network.broadcast_data(data, [client])


if __name__ == "__main__":
    start_server()
