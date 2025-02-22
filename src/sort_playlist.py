import JellyfinAPI


def main():
    config = JellyfinAPI.load_config()

    server = JellyfinAPI.ServerConnection(config.get('jellyfin', 'url'),
                                          config.get('jellyfin', 'username'),
                                          config.get('jellyfin', 'password'))

    server.login()
    print('Logged in')

    playlist_id = server.get_playlist_id_from_name(
        config.get('jellyfin', 'playlist name'))
    print('Got playlist')

    items = server.get_playlist_items(playlist_id)
    print('Got items')

    sort_keys = []

    for i, track in enumerate(items):
        sort_keys.append((server.get_track_sort_key(track), i))
    print('Got sort keys')

    sort_keys.sort(key=lambda x: x[0])
    print('Sorted the sort keys')

    with open('keys.txt', 'w') as f:
        for k in sort_keys:
            f.write(k[0] + '\n')
    print('Sort keys written to keys.txt')

    print('Sorting')
    for i, sort_key in enumerate(sort_keys):
        track = items[sort_key[1]]

        server.move_playlist_track(playlist_id, track['PlaylistItemId'], i)
        print(f'{i}/{len(sort_keys)}')


if __name__ == '__main__':
    main()
