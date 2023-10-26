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
    elif ('Artists' in track and len(track["Artists"]) > 0 and
          len(track["Artists"][0]) > 0):
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

            if len(line_data) == 4:
                artist = line_data[1].strip()
                album = line_data[2].strip()
                track = line_data[3].strip()
            elif len(line_data) == 5:
                artist = line_data[1].strip()
                album = line_data[2].strip() + ' - ' + line_data[3].strip()
                track = line_data[4].strip()
            elif len(line_data) == 6:
                artist = line_data[1].strip()
                album = line_data[2].strip() + ' - ' + line_data[3].strip()
                track = line_data[4].strip() + ' - ' + line_data[5].strip()

            track_data = track.split("'")
            if len(track_data) > 1:
                track = track_data[0]

            playlist_data.append(PlaylistItem(artist, album, track))

    no_matches = []
    low_scores = []

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
            no_matches.append(entry)
            continue

        match = items[0]

        if match['Score'] <= 150:
            low_scores.append((entry, match))
            print('Low score for match "{:s} - {:s} - {:s}" to query '
                  '"{:s} - {:s} - {:s}" with score {:.0f}'
                  .format(select_artist(match), match['Album'],
                          match['Name'], entry.artist, entry.album,
                          entry.track, match['Score']))
            continue

        print('Matching "{:s} - {:s} - {:s}" to query "{:s} - {:s} - {:s}" '
              'with score {:.0f}'.format(select_artist(match),
                                         match['Album'],
                                         match['Name'], entry.artist,
                                         entry.album, entry.track,
                                         match['Score']))

        server.add_item_to_playlist(playlist_id, match['Id'])

    with open('match issues.txt', 'w') as f:
        f.write('No Matches:\n')

        for entry in no_matches:
            string = f'{entry.artist} - {entry.album} - {entry.track}'
            f.write(string + '\n')

        f.write('\nLow Scores:\n')

        for (entry, match) in low_scores:
            string = ('Query: "{:s} - {:s} - {:s}", '
                      'Match: "{:s} - {:s} - {:s}", '
                      'Score: {:.0f}\n').format(
                entry.artist, entry.album, entry.track,
                select_artist(match), match['Album'], match['Name'],
                match['Score'])
            f.write(string)


if __name__ == '__main__':
    main()
