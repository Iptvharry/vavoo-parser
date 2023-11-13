import time, re, os, base64
from datetime import datetime, timedelta
from xml.dom import minidom

import utils.common as common

cachepath = common.cp
con = common.con
server_ip = common.get_ip_address()
port = int(common.get_setting('server_port', 'Main'))
temp = os.path.join(cachepath, 'xmltv.xml')

unicode = str


def get_m3u8(user, pw, out, typ):
    return
    cur = con.cursor()
    tf = open(os.path.join(cachepath, 'streams.%s' % typ), "w")
    tf.write("#EXTM3U")
    for d in cur.execute('SELECT * FROM streams ORDER BY id'):
        if typ == "m3u":
            ret = '\n#EXTINF:-1,%s' % d['name']
            if d['season'] != "":
                ret += ' S0'+d['key'] if (int(d['key']) < 10) else ' S'+d['key']
                ret += 'E0'+d['p2'] if (int(d['p2']) < 10) else 'E'+d['p2']
                if d['media_type'] != "": ret += d['media_type']
                tf.write(ret)
                tf.write('\nhttp://%s:%s/series/%s/%s/%s.%s' %(server_ip, port, user, pw, d['id'], out))
            else:
                tf.write(ret)
                tf.write('\nhttp://%s:%s/movie/%s/%s/%s.%s' %(server_ip, port, user, pw, d['id'], out))
        else:
            if d['key'] != "":
                ret = '\n#EXTINF:-1 tvg-id="%s" tvg-name="%s" group-title="%s",' %(re.sub("movie.|series.|\..*", "", d['sid']), d['media_type'], d['media_type'])
                ret += 'S0'+d['key'] if (int(d['key']) < 10) else ' S'+d['key']
                ret += 'E0'+d['p2'] if (int(d['p2']) < 10) else 'E'+d['p2']
                if d['media_type'] != "": ret += ' '+d['media_type']
                tf.write(ret)
                tf.write('\nhttp://%s:%s/series/%s/%s/%s.%s' %(server_ip, port, user, pw, d['id'], out))
            else:
                tf.write('\n#EXTINF:-1 tvg-id="%s" tvg-name="%s" group-title="%s",%s' %(re.sub("movie.|series.|\..*", "", d['sid']), d['media_type'], 'Filme', d['media_type']))
                tf.write('\nhttp://%s:%s/movie/%s/%s/%s.%s' %(server_ip, port, user, pw, d['id'], out))
    tf.close()
    return True


def get_all_channels():
    cur = con.cursor()
    epg_logos = common.get_setting('epg_logos')
    epg_rytec = common.get_setting('epg_rytec')
    m3u8_name = common.get_setting('m3u8_name')
    epg_provider = common.get_setting('epg_provider')
    dub = {}
    num = 0
    num2 = 0
    for d in cur.execute('SELECT * FROM info WHERE media_type="' + str('movie') + '" ORDER BY releaseDate DESC'):
        num += 1
        dub[str(num)] = {
            "num": int(num),
            "name": d['name'],
            "stream_type": "movie",
            "type_name": "Movies",
            "stream_id": str(d['id']),
            "stream_icon": d['poster'],
            "epg_channel_id": None,
            "added": None,
            "category_name": d['site'],
            "category_id": str(d['category_id']),
            "series_no": None,
            "live": "0",
            "container_extension": "mp4",
            "tv_archive": 0,
            "direct_source": "",
            "tv_archive_duration": 0
        }
    cur.execute('SELECT * FROM channel ORDER BY id')
    dat = cur.fetchall()
    for d in dat:
        tid = ''
        name = ''
        logo = ''
        if not str(d['tid']) == '':
            cur.execute('SELECT * FROM epgs WHERE id="' + d['tid'] + '"')
            eat = cur.fetchone()
            if epg_rytec == '1': tid = eat['rid']
            elif epg_provider == 'm':
                if not eat['mn'] == None: tid = eat['mn']
            elif epg_provider == 't':
                if not eat['tn'] == None: tid = eat['tn']
            if epg_logos == 'p':
                if epg_provider == 'm':
                    if not eat['ml'] == None: logo = eat['ml']
                elif epg_provider == 't':
                    if not eat['tl'] == None: logo = eat['tl']
            elif epg_logos == 'o':
                if not eat['ol'] == None: logo = eat['ol']
            if m3u8_name == '1':
                if not eat['display'] == None: name = eat['display']
                else: name = d['display']
            else: name = d['name']
        else:
            if m3u8_name == '1': name = d['display']
            else: name = d['name']
            if not str(d['logo']) == '': logo = d['logo']
        num += 1
        num2 += 1
        dub[str(num)] = {
            "num": int(num2),
            "name": name,
            "stream_type": "live",
            "type_name": "Live Streams",
            "stream_id": str(d['id']),
            "stream_icon": logo,
            "epg_channel_id": tid,
            "added": None,
            "category_name": d['category_id'],
            "category_id": str(d['cid']),
            "series_no": None,
            "live": "1",
            "container_extension": "mp4",
            "tv_archive": 0,
            "direct_source": "",
            "tv_archive_duration": 0
        }
    return dub


def get_vod_categories():
    cur = con.cursor()
    cats = []
    for cat in cur.execute('SELECT * FROM categories WHERE media_type="' + str('movie') + '" ORDER BY category_id'):
        cats.append({
            "category_id": cat['category_id'], 
            "category_name": cat['category_name'], 
            "parent_id": 0, 
        })
    return cats


def get_vod_streams(category_id=None):
    cur = con.cursor()

    ret = []
    num = 0
    if category_id is None:
        for d in cur.execute('SELECT * FROM info WHERE media_type="' + str('movie') + '" ORDER BY releaseDate DESC'):
            num += 1
            ret.append({
                "num": int(num),
                "name": d['name'],
                "stream_type": "movie",
                "stream_id": int(d['id']),
                "stream_icon": d['poster'],
                "rating": None,
                "rating_5based": 0,
                "added": None,
                "category_id": str(d['category_id']),
                "container_extension": "mp4",
                "direct_source": ""
            })
        return ret
    else:
        for d in cur.execute('SELECT * FROM info WHERE media_type="' + str('movie') + '" AND category_id="' + str(category_id) + '" ORDER BY releaseDate DESC'):
            num += 1
            ret.append({
                "num": int(num),
                "name": d['name'],
                "stream_type": "movie",
                "stream_id": int(d['id']),
                "stream_icon": d['poster'],
                "rating": None,
                "rating_5based": 0,
                "added": None,
                "category_id": str(d['category_id']),
                "container_extension": "mp4",
                "direct_source": ""
            })
        return ret


def get_vod_info(vod_id):
    cur = con.cursor()
    cur.execute('SELECT * FROM info WHERE id="' + str(vod_id) + '"')
    info = cur.fetchone()
    cur.execute('SELECT * FROM streams WHERE sid="' + str(info['id']) + '"')
    data = cur.fetchone()
    return {
        "info": {
            "kinopoisk_url": "",
            "tmdb_id": info['tmdb_id'],
            "name": info['name'],
            "o_name": info['originalName'],
            "cover_big": info['poster'],
            "movie_image": info['backdrop'],
            "releasedate": info['releaseDate'],
            "episode_run_time": info['duration'],
            "youtube_trailer": "",
            "director": "",
            "actors": "",
            "cast": "",
            "description": info['description'],
            "plot": info['description'],
            "age": "",
            "mpaa_rating": "",
            "rating_count_kinopoisk": 0,
            "country": info['countries'],
            "genre": info['genres'],
            "duration_secs": 0,
            "duration": info['duration'],
            "video": [],
            "audio": [],
            "bitrate": 0,
            "rating": info['rating']
        },
        "movie_data": {
            "stream_id": int(data['id']),
            "name": info['name'],
            "added": None,
            "category_id": str(info['category_id']),
            "container_extension": "mp4",
            "direct_source": ""
        }
    }


def get_series_categories():
    cur = con.cursor()
    cats = []
    for cat in cur.execute('SELECT * FROM categories WHERE media_type="' + str('tvshow') + '" ORDER BY category_id'):
        cats.append({
            "category_id": cat['category_id'], 
            "category_name": cat['category_name'], 
            "parent_id": 0, 
        })
    return cats


def get_series(category_id=None):
    cur = con.cursor()

    ret = []
    num = 0
    if category_id is None:
        for d in cur.execute('SELECT * FROM info WHERE media_type="' + str('tvshow') + '" ORDER BY releaseDate DESC'):
            num += 1
            ret.append({
                "num": int(num),
                "name": d['name'],
                "series_id": int(d['id']),
                "cover": d['poster'],
                "plot": d['description'],
                "cast": None,
                "director": None,
                "genre": d['genres'],
                "releaseDate": d['releaseDate'],
                "last_modified": None,
                "rating": d['rating'],
                "rating_5based": 0,
                "backdrop_path": [d['backdrop']],
                "youtube_trailer": None,
                "episode_run_time": d['duration'],
                "category_id": str(d['category_id'])
            })
        return ret
    else:
        for d in cur.execute('SELECT * FROM info WHERE media_type="' + str('tvshow') + '" AND category_id="' + str(category_id) + '" ORDER BY releaseDate DESC'):
            num += 1
            ret.append({
                "num": int(num),
                "name": d['name'],
                "series_id": int(d['id']),
                "cover": d['poster'],
                "plot": d['description'],
                "cast": None,
                "director": None,
                "genre": d['genres'],
                "releaseDate": d['releaseDate'],
                "last_modified": None,
                "rating": d['rating'],
                "rating_5based": 0,
                "backdrop_path": [d['backdrop']],
                "youtube_trailer": "",
                "episode_run_time": d['duration'],
                "category_id": str(d['category_id'])
            })
        return ret


def get_series_info(series_id):
    cur = con.cursor()
    cur.execute('SELECT * FROM info WHERE id="' + str(series_id) + '"')
    info = cur.fetchone()
    eps = {}
    nums = {}
    for d in cur.execute('SELECT * FROM streams WHERE sid="' + str(info['id']) + '" ORDER BY season, episode'):
        if not d['season'] in eps:
            eps[d['season']] = []
            nums[d['season']] = 0
        nums[d['season']] += 1
        eps[d['season']].append({
            "id": str(d['id']),
            "episode_num": nums[d['season']],
            "title": d['name'],
            "container_extension": "mp4",
            "info": {
                "releasedate": info['releaseDate'],
                "plot": "",
                "duration_secs": 0,
                "duration": "00:00:00",
                "video": [],
                "audio": [],
                "bitrate": 0,
                "rating": info['rating'],
                "season": d['season'],
                "tmdb_id": info['tmdb_id']
            },
            "added": None,
            "season": int(d['season']),
            "direct_source": ""
        })
    return {
        "seasons": [],
        "info": {
            "name": info['name'],
            "cover": info['poster'],
            "plot": info['description'],
            "cast": "",
            "director": "",
            "genre": info['genres'],
            "releaseDate": info['releaseDate'],
            "last_modified": None,
            "rating": info['rating'],
            "rating_5based": 0,
            "backdrop_path": [ info['backdrop'] ],
            "youtube_trailer": "",
            "episode_run_time": "0",
            "category_id": str(info['category_id'])
        },
        "episodes": eps
    }


def get_live_categories():
    cur = con.cursor()
    cats = []
    for cat in cur.execute('SELECT * FROM categories WHERE media_type="' + str('live') + '" ORDER BY category_id'):
        cats.append({
            "category_id": cat['category_id'], 
            "category_name": cat['category_name'], 
            "parent_id": 0, 
        })
    return cats


def get_live_streams(category_id=None):
    cur = con.cursor()
    epg_logos = common.get_setting('epg_logos')
    epg_rytec = common.get_setting('epg_rytec')
    m3u8_name = common.get_setting('m3u8_name')
    epg_provider = common.get_setting('epg_provider')

    ret = []
    num = 0
    if category_id is None:
        cur.execute('SELECT * FROM channel ORDER BY id')
        dat = cur.fetchall()
        for d in dat:
            tid = ''
            name = ''
            logo = ''
            if not str(d['tid']) == '':
                cur.execute('SELECT * FROM epgs WHERE id="' + d['tid'] + '"')
                eat = cur.fetchone()
                if epg_rytec == '1': tid = eat['rid']
                elif epg_provider == 'm':
                    if not eat['mn'] == None: tid = eat['mn']
                elif epg_provider == 't':
                    if not eat['tn'] == None: tid = eat['tn']
                if epg_logos == 'p':
                    if epg_provider == 'm':
                        if not eat['ml'] == None: logo = eat['ml']
                    elif epg_provider == 't':
                        if not eat['tl'] == None: logo = eat['tl']
                elif epg_logos == 'o':
                    if not eat['ol'] == None: logo = eat['ol']
                if m3u8_name == '1':
                    if not eat['display'] == None: name = eat['display']
                    else: name = d['display']
                else: name = d['name']
            else:
                if m3u8_name == '1': name = d['display']
                else: name = d['name']
                if not str(d['logo']) == '': logo = d['logo']
            num += 1
            ret.append({
                "num": int(num),
                "name": name,
                "stream_type": "live",
                "stream_id": int(d['id']),
                "stream_icon": logo,
                "epg_channel_id": tid,
                "added": None,
                "category_id": str(d['cid']),
                "custom_sid": "",
                "tv_archive": 0,
                "direct_source": "",
                "tv_archive_duration": 0
            })
        return ret
    else:
        cur.execute('SELECT * FROM categories WHERE category_id="' + str(category_id) + '"')
        cat = cur.fetchone()
        cur.execute('SELECT * FROM channel WHERE grp="' + str(cat['category_name']) + '" ORDER BY id')
        dat = cur.fetchall()
        for d in dat:
            tid = ''
            name = ''
            logo = ''
            if not str(d['tid']) == '':
                cur.execute('SELECT * FROM epgs WHERE id="' + d['tid'] + '"')
                eat = cur.fetchone()
                if epg_rytec == '1': tid = eat['rid']
                elif epg_provider == 'm':
                    if not eat['mn'] == None: tid = eat['mn']
                elif epg_provider == 't':
                    if not eat['tn'] == None: tid = eat['tn']
                if epg_logos == 'p':
                    if epg_provider == 'm':
                        if not eat['ml'] == None: logo = eat['ml']
                    elif epg_provider == 't':
                        if not eat['tl'] == None: logo = eat['tl']
                elif epg_logos == 'o':
                    if not eat['ol'] == None: logo = eat['ol']
                if m3u8_name == '1':
                    if not eat['display'] == None: name = eat['display']
                    else: name = d['display']
                else: name = d['name']
            else:
                if m3u8_name == '1': name = d['display']
                else: name = d['name']
                if not str(d['logo']) == '': logo = d['logo']
            num += 1
            ret.append({
                "num": int(num),
                "name": name,
                "stream_type": "live",
                "stream_id": int(d['id']),
                "stream_icon": logo,
                "epg_channel_id": tid,
                "added": None,
                "category_id": str(category_id),
                "custom_sid": "",
                "tv_archive": 0,
                "direct_source": "",
                "tv_archive_duration": 0
            })
        return ret


def get_short_epg(stream_id, limit=None):
    return
    cur = con.cursor()
    
    ret = {}
    ret["epg_listings"] = []
    num = 0
    go = False
    if limit is None:
        limit = 4
    
    cur.execute('SELECT * FROM channel WHERE id="' + str(stream_id) + '"')
    chan = cur.fetchone()
    if chan:
        cur.execute('SELECT * FROM tvs WHERE id="' + str(chan['tid']) + '"')
        cat = cur.fetchone()
        if cat:
            for e in cur.execute('SELECT * FROM epg WHERE cid="' + str(chan['tid']) + '" ORDER BY start'):
                if go == True or int(e['start']) > int(time.time()) or int(e['end']) > int(time.time()):
                    if int(num) >= int(limit):
                        break
                    go = True
                    ret["epg_listings"].append({
                        "id": str(e['id']),
                        "epg_id": str(cat['i']),
                        "title": e['title'],
                        "lang": e['lang'],
                        "start": datetime.utcfromtimestamp(e['start']).strftime('%Y-%m-%d %H:%M:%S'),
                        "end": datetime.utcfromtimestamp(e['end']).strftime('%Y-%m-%d %H:%M:%S'),
                        "description": e['desc'],
                        "channel_id": cat['cid'],
                        "start_timestamp": int(e['start']),
                        "stop_timestamp": int(e['end'])
                    })
                    num += 1
            return ret


def get_simple_data_table(stream_id):
    return
    cur = con.cursor()
    
    ret = {}
    ret["epg_listings"] = []
    num = 0
    go = False
    
    cur.execute('SELECT * FROM channel WHERE id="' + str(stream_id) + '"')
    chan = cur.fetchone()
    if chan:
        cur.execute('SELECT * FROM tvs WHERE id="' + str(chan['tid']) + '"')
        cat = cur.fetchone()
        if cat:
            for e in cur.execute('SELECT * FROM epg WHERE cid="' + str(chan['tid']) + '" ORDER BY start'):
                if go == True or int(e['start']) > int(time.time()) or int(e['end']) > int(time.time()):
                    go = True
                    ret["epg_listings"].append({
                        "id": str(e['id']),
                        "epg_id": str(cat['i']),
                        "title": e['title'],
                        "lang": e['lang'],
                        "start": datetime.utcfromtimestamp(e['start']).strftime('%Y-%m-%d %H:%M:%S'),
                        "end": datetime.utcfromtimestamp(e['end']).strftime('%Y-%m-%d %H:%M:%S'),
                        "description": e['desc'],
                        "channel_id": cat['cid'],
                        "start_timestamp": int(e['start']),
                        "stop_timestamp": int(e['end']),
                        "now_playing": 0,
                        "has_archive": 0
                    })
                    num += 1
            return ret


def get_xml():
    return
    if os.path.exists(temp):
        os.remove(temp)
    cur = con.cursor()

    go = False
    oid = None
    ret = []
    ret.append('<?xml version="1.0" encoding="utf-8" ?>')
    ret.append('<!DOCTYPE tv SYSTEM "xmltv.dtd">')
    ret.append('<tv generator-info-name="Xtream Codes" generator-info-url="%s:%s">' %(server_ip, port))
    for c in cur.execute('SELECT * FROM tvs ORDER BY i'):
        ret.append('<channel id="%s">' % str(c['id']))
        ret.append('<display-name>%s</display-name>' % str(c['name']))
        ret.append('<icon src="%s" />' % str(c['icon']))
        ret.append('</channel>')
    for e in cur.execute('SELECT * FROM epg ORDER BY cid, start'):
        if oid == None:
            oid = e['cid']
        if not oid == e['cid']:
            go = False
            oid = e['cid']
        if go == True or int(e['start']) > int(time.time()) or int(e['end']) > int(time.time()):
            go = True
            title = base64.b64decode(str(e['title']).encode('utf-8')).decode('utf-8')
            desc = base64.b64decode(str(e['desc']).encode('utf-8')).decode('utf-8')
            ret.append('<programme start="%s +0000" stop="%s +0000" channel="%s" >' %(datetime.utcfromtimestamp(e['start']).strftime('%Y%m%d%H%M%S'), datetime.utcfromtimestamp(e['end']).strftime('%Y%m%d%H%M%S'), str(e['cid'])))
            ret.append('<title>%s</title>' % title)
            ret.append('<desc>%s</desc>' % desc)
            ret.append('</programme>')
    ret.append('</tv>')
    r = ''.join(ret)
    with open(temp, 'w', encoding='utf-8') as f:
        f.write(r)
    return True

