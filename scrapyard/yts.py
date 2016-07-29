import exceptions
import network
import requests
import scraper
import urllib

YTS_URL = 'http://yts.ag'

################################################################################
def movie(movie_info):
    magnet_infos = []

    try:
        json_data = network.json_get(YTS_URL + '/api/v2/list_movies.json', params={ 'query_term': movie_info['imdb_id'] })
        if 'data' in json_data:
            if 'movies' in json_data['data']:
                for movie_item in json_data['data']['movies']:
                    if 'imdb_code' in movie_item and movie_item['imdb_code'] == movie_info['imdb_id'] and 'torrents' in movie_item:
                        for torrent_item in movie_item['torrents']:
                            magnet_title = u'{0} ({1}) {2} - YIFY'.format(movie_item['title'], movie_item['year'], torrent_item['quality'])
                            magnet_url   = u'magnet:?xt=urn:btih:{0}&dn={1}&tr=http://track.one:1234/announce&tr=udp://track.two:80&tr=udp://open.demonii.com:1337/announce&tr=udp://tracker.openbittorrent.com:80&tr=udp://tracker.coppersurfer.tk:6969&tr=udp://glotorrents.pw:6969/announce&tr=udp://tracker.opentrackr.org:1337/announce&tr=udp://torrent.gresille.org:80/announce&tr=udp://p4p.arenabg.com:1337&tr=udp://tracker.leechers-paradise.org:6969'.format(torrent_item['hash'], urllib.quote(magnet_title.encode('utf8')))
                            magnet_infos.append(scraper.Magnet(magnet_url, magnet_title, torrent_item['seeds'], torrent_item['peers'], torrent_item['size_bytes']))
    except requests.exceptions.HTTPError as exception:
        if exception.response.status_code in (404, 503):
            pass
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        pass
    except exceptions.JSONError:
        pass

    return magnet_infos
