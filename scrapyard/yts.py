import cache
import network
import scraper
import urllib

YTS_URL = 'http://yts.re'

################################################################################
def movie(movie_info):
    magnet_infos = []

    json_data = network.json_get_cached_optional(YTS_URL + '/api/v2/list_movies.json', expiration=cache.HOUR, params={ 'query_term': movie_info['imdb_id'] })
    if 'data' in json_data:
        if 'movies' in json_data['data']:
            for movie_item in json_data['data']['movies']:
                if 'imdb_code' in movie_item and movie_item['imdb_code'] == movie_info['imdb_id'] and 'torrents' in movie_item:
                    for torrent_item in movie_item['torrents']:
                        magnet_title = '{0} ({1}) {2} - YIFY'.format(movie_item['title'], movie_item['year'], torrent_item['quality'])
                        magnet_url   = 'magnet:?xt=urn:btih:{0}&dn={1}&tr=http://exodus.desync.com:6969/announce&tr=udp://tracker.openbittorrent.com:80/announce&tr=udp://open.demonii.com:1337/announce&tr=udp://exodus.desync.com:6969/announce&tr=udp://tracker.yify-torrents.com/announce'.format(torrent_item['hash'], urllib.quote(magnet_title))
                        magnet_infos.append(scraper.Magnet(magnet_url, None, torrent_item['seeds'], torrent_item['peers']))

    return magnet_infos