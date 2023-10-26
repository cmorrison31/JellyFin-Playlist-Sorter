import JellyfinAPI


def main():
    config = JellyfinAPI.load_config()

    server = JellyfinAPI.ServerConnection(config.get('jellyfin', 'url'),
                                          config.get('jellyfin', 'username'),
                                          config.get('jellyfin', 'password'))

    server.login()

    playlist_id = server.get_playlist_id_from_name(
        config.get('jellyfin', 'playlist name'))

    items = server.get_playlist_items(playlist_id)

    items_to_delete = []
    count = 0

    last_item = None
    for item in items:
        if last_item is None:
            last_item = item
            continue

        if item['Id'] == last_item['Id']:
            items_to_delete.append(item)

        if len(items_to_delete) > 25:
            server.remove_items_from_playlist(playlist_id, items_to_delete)
            items_to_delete = []
            count += 25

        last_item = item

    if len(items_to_delete) > 0:
        server.remove_items_from_playlist(playlist_id, items_to_delete)
        count += len(items_to_delete)

    print(f'Removed {count} items')


if __name__ == '__main__':
    main()
