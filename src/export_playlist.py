import JellyfinAPI


def select_artist(track):
    if 'AlbumArtist' in track and len(track["AlbumArtist"]) > 0:
        return track['AlbumArtist']
    elif 'AlbumArtists' in track and len(track["AlbumArtists"]) > 0:
        return track['AlbumArtists']
    elif 'Artists' in track and len(track["Artists"]) > 0 and \
            len(track["Artists"][0]) > 0:
        return ' '.join(track["Artists"])
    else:
        return 'None'


def main():
    config = JellyfinAPI.load_config()

    server = JellyfinAPI.ServerConnection(config.get('jellyfin', 'url'),
                                          config.get('jellyfin', 'username'),
                                          config.get('jellyfin', 'password'))

    server.login()

    playlist_id = server.get_playlist_id_from_name(
        config.get('jellyfin', 'playlist name'))

    items = server.get_playlist_items(playlist_id)

    with open(config.get('jellyfin', 'playlist name') + '.txt', 'w') as f:
        for i, track in enumerate(items):
            artist = select_artist(track)
            f.write('{:.0f} - {} - {} - {}\n'
                    .format(i, artist, track['Album'],
                            track['Name']))


if __name__ == '__main__':
    main()
