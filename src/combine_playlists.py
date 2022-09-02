import JellyfinAPI


def main():
    config = JellyfinAPI.load_config()

    server = JellyfinAPI.ServerConnection(config.get('jellyfin', 'url'),
                                          config.get('jellyfin', 'username'),
                                          config.get('jellyfin', 'password'))

    server.login()

    playlist_id = server.get_playlist_id_from_name(
        config.get('jellyfin', 'playlist name'))

    if playlist_id is None:
        playlist_id = server.create_playlist(
            config.get('jellyfin', 'playlist name'))

    playlists = [tmp for tmp in
                 config.get('jellyfin', 'playlists to combine').split(', ')]

    items = []

    for playlist in playlists:
        local_playlist_id = server.get_playlist_id_from_name(playlist)

        playlist_items = server.get_playlist_items(local_playlist_id)

        for item in playlist_items:
            items.append(item)

    for i, item in enumerate(items):
        if i % 10 == 0:
            print('{}/{}'.format(i, len(items)))

        status = server.add_item_to_playlist(playlist_id, item['Id'])

        if status != 204:
            print(f'Status code: {status}')


if __name__ == '__main__':
    main()
