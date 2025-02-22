import JellyfinAPI
import re


def main():
    config = JellyfinAPI.load_config()

    server = JellyfinAPI.ServerConnection(config.get('jellyfin', 'url'),
                                          config.get('jellyfin', 'username'),
                                          config.get('jellyfin', 'password'))

    server.login()

    playlist_id = server.get_playlist_id_from_name(
        config.get('jellyfin', 'playlist name'))

    items = server.get_playlist_items(playlist_id)

    for item in items:
        match = re.search('remix', item['Name'], re.IGNORECASE)

        if match:
            print(item)

if __name__ == '__main__':
    main()
