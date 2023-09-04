import JellyfinAPI
from thefuzz import fuzz


class PlaylistItem:
    def __init__(self, artist, album, track):
        self.artist = artist
        self.album = album
        self.track = track


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

    playlist_data = []

    with open(config.get('jellyfin', 'playlist name') + '.txt', 'r') as f:
        for line in f:
            line_data = line.strip().split('-')

            playlist_data.append(PlaylistItem(line_data[1].strip(),
                                              line_data[2].strip(),
                                              line_data[3].strip()))

    with open('no_match.txt', 'w') as f:
        for entry in playlist_data:
            items = server.search_for_music_track_by_name(entry.track)

            for item in items:
                artist = select_artist(item)

                artist_score = fuzz.ratio(artist, entry.artist)
                album_score = fuzz.ratio(item['Album'], entry.album)
                track_score = fuzz.ratio(item['Name'], entry.track)

                score = artist_score + album_score + track_score

                item['Score'] = score

            items = sorted(items, key=lambda x: x['Score'], reverse=True)

            if len(items) == 0:
                string = (f'No matches found for {entry.artist} - '
                          f'{entry.album} - {entry.track}')
                print(string)
                f.write(string + '\n')
                continue

            match = items[0]

            print('Matching "{:s} - {:s} - {:s}" to query "{:s} - {:s} - {:s}" '
                  'with score {:.0f}'
                  .format(select_artist(match), match['Album'], match['Name'],
                          entry.artist, entry.album, entry.track, match['Score']))

            server.add_item_to_playlist(playlist_id, match['Id'])


if __name__ == '__main__':
    main()
