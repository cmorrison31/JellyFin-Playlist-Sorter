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

    sort_keys = []

    for i, track in enumerate(items):
        sort_keys.append((server.get_track_sort_key(track), i))

    sort_keys.sort(key=lambda x: x[0])

    for i, sort_key in enumerate(sort_keys):
        track = items[sort_key[1]]

        server.move_playlist_track(playlist_id, track['PlaylistItemId'], i)


if __name__ == '__main__':
    main()
