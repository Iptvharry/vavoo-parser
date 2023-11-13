# -*- coding: utf-8 -*-
import platform, sys, json, os, time, inquirer, re
from multiprocessing import Process
import utils.common as com
from unidecode import unidecode

from utils.common import get_ip_address as ip
from utils.common import Logger as Logger
import resolveurl as resolver
from helper import sites
from helper.tmdb import cTMDB
import services

cachepath = com.cp
listpath = com.lp
con = com.con
jobs = services.jobs

unicode = str


def updateDB(loads):
    con.text_factory = lambda x: unicode(x, errors='ignore')
    cur = con.cursor()
    i = s = n = m = 0
    site = None

    for load in loads:
        if "entries" in load:
            if not load['entries'] == None:
                for entry in load['entries']:
                    if "site" in entry: site = entry["site"]
                    if "meta" in entry: meta = entry["meta"]
                    else: meta = []
                    if "tmdb_id" in meta: tmdb = meta["tmdb_id"]
                    else: tmdb = ''
                    if entry["mediatype"] == 'movie' or entry["mediatype"] == 'tvshow':
                        media_type = entry["mediatype"]
                        name = entry["name"].replace("\\\"", "").replace("'", "").replace("\"", "")
                        cur.execute('SELECT * FROM info WHERE name="' + str(name) + '" AND site="' + str(entry["site"]) + '" AND media_type="' + str(media_type) + '"')
                        row = cur.fetchone()
                        if not row:
                            cur.execute('SELECT * FROM categories WHERE category_name="' + str(entry["site"]) + '" AND media_type="' + str(media_type) + '"')
                            cat = cur.fetchone()
                            if cat: cid = cat['category_id']
                            else: cid = 0
                            if "originaltitle" in meta: originalName = meta["originaltitle"].replace("\\\"", "").replace("'", "").replace("\"", "")
                            else: originalName = ''
                            if "premiered" in meta: releaseDate = meta["premiered"].replace("\\\"", "").replace("'", "").replace("\"", "")
                            elif "year" in entry: releaseDate = entry["year"]
                            else: releaseDate = ''
                            if "genre" in meta: genres = meta["genre"].replace("\\\"", "").replace("'", "").replace("\"", "")
                            else: genres = ''
                            if "plot" in meta: description = meta["plot"].replace("\u201e", "").replace("\u201c", "").replace("\\\"", "").replace("'", "").replace("\"", "")
                            elif "desc" in entry: description = entry["desc"].replace("\u201e", "").replace("\u201c", "").replace("\\\"", "").replace("'", "").replace("\"", "")
                            else: description = ''
                            if "country" in meta: countries = meta["country"].replace("\\\"", "").replace("'", "").replace("\"", "")
                            else: countries = ''
                            if "rating" in meta: rating = meta["rating"]
                            elif "rating" in entry: rating = entry["rating"]
                            else: rating = ''
                            if "votes" in meta: votes = meta["votes"]
                            elif "votes" in entry: votes = entry["votes"]
                            else: votes = ''
                            if "duration" in entry: duration = entry["duration"]
                            else: duration = ''
                            if "cover_url" in meta: poster = meta["cover_url"]
                            elif "thumb" in entry: poster = entry["thumb"]
                            else: poster = ''
                            if "backdrop_url" in meta: backdrop = meta["backdrop_url"]
                            elif "backdrop" in entry: backdrop = entry["backdrop"]
                            else: backdrop = ''
                            if "quality" in entry: quality = entry["quality"]
                            else: quality = ''
                            cur.execute('INSERT INTO info VALUES (NULL,"'+str(entry["site"])+'","'+str(cid)+'","'+str(tmdb)+'","'+str(media_type)+'","'+str(name)+'","'+str(originalName)+'","'+str(releaseDate)+'","'+str(genres)+'","'+str(description)+'","'+str(countries)+'","'+str(rating)+'","'+str(votes)+'","'+str(duration)+'","'+str(poster)+'","'+str(backdrop)+'","'+str(quality)+'")')
                            i += 1
                            cur.execute('SELECT * FROM info WHERE name="' + str(name) + '" AND site="' + str(entry["site"]) + '" AND media_type="' + str(media_type) + '"')
                            row = cur.fetchone()
                        else: n += 1
                        sid = row['id']
                    if entry["key"] == 'showHosters' or entry["key"] == 'showEpisodeHosters':
                        cur.execute('SELECT * FROM streams WHERE sid="' + str(sid) + '"')
                        row = cur.fetchone()
                        if not row:
                            if "p2" in entry: p2 = entry["p2"]
                            else: p2 = ''
                            if "thumb" in entry: thumb = entry["thumb"]
                            else: thumb = ''
                            cur.execute('INSERT INTO streams VALUES (NULL,"'+str(sid)+'","'+str(entry["site"])+'","'+str(entry["key"])+'","'+str(p2)+'","'+str(media_type)+'",NULL,NULL,"'+str(name)+'","'+str(entry["url"])+'","'+str(thumb)+'")')
                            s += 1
                        else: m += 1
                    if entry["key"] == 'showSeasons' and "entries" in entry:
                        if not entry['entries'] == None:
                            y = 0
                            for season in entry['entries']:
                                y += 1
                                if season["key"] == "showEpisodes" and "entries" in season:
                                    if not season['entries'] == None:
                                        z = 0
                                        for episode in season['entries']:
                                            z += 1
                                            if "s" in season: se = season["s"]
                                            elif "s" in episode: se = episode["s"]
                                            elif "s" in entry: se = entry["s"]
                                            else: se = y
                                            if "e" in episode: ep = episode["e"]
                                            elif "e" in season: ep = season["e"]
                                            elif "e" in entry: ep = entry["e"]
                                            else: ep = z
                                            cur.execute('SELECT * FROM streams WHERE sid="' + str(sid) + '" AND season="' + str(se) + '" AND episode="' + str(ep) + '"')
                                            row = cur.fetchone()
                                            if not row:
                                                if "p2" in episode: p2 = episode["p2"]
                                                else: p2 = ''
                                                if "thumb" in episode: thumb = episode["thumb"]
                                                elif "thumb" in season: thumb = season["thumb"]
                                                elif "thumb" in entry: thumb = entry["thumb"]
                                                else: thumb = ''
                                                cur.execute('INSERT INTO streams VALUES (NULL,"'+str(sid)+'","'+str(entry["site"])+'","'+str(episode["key"])+'","'+str(p2)+'","'+str(media_type)+'","'+str(se)+'","'+str(ep)+'","'+str(name)+'","'+str(episode["url"])+'","'+str(thumb)+'")')
                                                s += 1
                                            else: m += 1
                    if entry["key"] == 'showEpisodes' and "entries" in entry:
                        if not entry['entries'] == None:
                            x = 0
                            for episode in entry['entries']:
                                x += 1
                                if "s" in episode: se = episode["s"]
                                elif "s" in entry: se = entry["s"]
                                else: se = 0
                                if "e" in episode: ep = episode["e"]
                                elif "e" in entry: ep = entry["e"]
                                else: ep = x
                                cur.execute('SELECT * FROM streams WHERE sid="' + str(sid) + '" AND season="' + str(se) + '" AND episode="' + str(ep) + '"')
                                row = cur.fetchone()
                                if not row:
                                    if "p2" in episode: p2 = episode["p2"]
                                    else: p2 = ''
                                    if "thumb" in episode: thumb = episode["thumb"]
                                    elif "thumb" in entry: thumb = entry["thumb"]
                                    else: thumb = ''
                                    cur.execute('INSERT INTO streams VALUES (NULL,"'+str(sid)+'","'+str(entry["site"])+'","'+str(episode["key"])+'","'+str(p2)+'","'+str(media_type)+'","'+str(se)+'","'+str(ep)+'","'+str(name)+'","'+str(episode["url"])+'","'+str(thumb)+'")')
                                    s += 1
                                else: m += 1                        
        con.commit()
    if site == None:
        if "site" in loads[0]: site = loads[0]["site"]
        elif "entries" in loads[0]:
            if "site" in loads[0]["entries"][0]: site = loads[0]["entries"][0]["site"]
    if site == None: site = 'Unknown'
    Logger(1, 'Database update successful! (%s Site)' % site)
    Logger(1, 'Infos: %s + Streams: %s (duplicated: Infos: %s + Streams: %s)' %(str(i), str(s), str(n), str(m)))
    return True


def jobber(site, loads):
    for load in loads:
        try:
            key = getattr(site, load['key'])
            if "p2" in load: load["entries"] = key(load['url'], load['p2'])
            else: load["entries"] = key(load['url'])
            if len(load["entries"]) > 0:
                for entry in load["entries"]:
                    if entry["mediatype"] == 'movie' or entry["mediatype"] == 'tvshow':
                        if bool(int(com.get_setting('get_tmdb', 'Main'))) == True:
                            try:
                                if "year" in entry: 
                                    meta = cTMDB().get_meta(str(entry["mediatype"]), str(entry["name"]), year=str(entry["year"]), advanced='false')
                                else: 
                                    meta = cTMDB().get_meta(str(entry["mediatype"]), str(entry["name"]), advanced='false')
                            except Exception:
                                meta = None
                        else: meta = None
                    if meta: entry["meta"] = meta
                    if not entry["key"] == 'showHosters' and not entry["key"] == 'showEpisodeHosters':
                        try:
                            key = getattr(site, entry['key'])
                            if "p2" in entry: entry["entries"] = key(entry["url"], entry["p2"])
                            else: entry["entries"] = key(entry["url"])
                            if len(entry["entries"]) > 0:
                                for entry2 in entry["entries"]:
                                    if not entry2["key"] == 'showHosters' and not entry["key"] == 'showEpisodeHosters':
                                        try:
                                            key = getattr(site, entry2['key'])
                                            if "p2" in entry2: entry2["entries"] = key(entry2["url"], entry2["p2"])
                                            else: entry2["entries"] = key(entry2["url"])
                                            if len(entry2["entries"]) > 0:
                                                for entry3 in entry2["entries"]:
                                                    if not entry3["key"] == 'showHosters' and not entry["key"] == 'showEpisodeHosters':
                                                        try:
                                                            key = getattr(site, entry3['key'])
                                                            if "p2" in entry3: entry3["entries"] = key(entry3["url"], entry3["p2"])
                                                            else: entry3["entries"] = key(entry3["url"])
                                                        except Exception:
                                                            entry3["entries"] = None
                                        except Exception:
                                            entry2["entries"] = None
                        except Exception:
                            entry["entries"] = None
        except Exception:
            load["entries"] = None

    #set_cache(site.SITE_IDENTIFIER, loads, 'sites')
    updateDB(loads)
    return True


def getMovies():
    for site in sites.sites:
        if bool(int(com.get_setting(site.SITE_IDENTIFIER+'_auto', 'Xstream'))) == True:
            load = site.load()
            if load:
                job = Process(target=jobber, args=(site, load,))
                jobs.append(job)
                job.start()
    if len(jobs) > 0:
        for job in jobs:
            job.join()
    Logger(1, 'All jobs done ...', 'new', 'get')
    return True


def genLists():
    if os.path.exists(os.path.join(listpath, 'vod.m3u8')):
        os.remove(os.path.join(listpath, 'vod.m3u8'))
    tf = open(os.path.join(listpath, 'vod.m3u8'), "w")
    tf.write("#EXTM3U")
    hurl = 'http://'+str(ip())+':'+str(com.get_setting('server_port', 'Main'))
    cur = con.cursor()
    i = 0
    for row in cur.execute('SELECT * FROM streams WHERE media_type="movie" ORDER BY id'):
        if row['thumb'].startswith('http'): tf.write('\n#EXTINF:-1 group-title="%s" tvg-logo="%s" tvg-id="vod%s",%s' % (row['site'], row['thumb'], row['id'], row['name']))
        else: tf.write('\n#EXTINF:-1 group-title="%s" tvg-id="vod%s",%s' % (row['site'], row['id'], row['name']))
        tf.write('\n%s/stream/%s' % (hurl, row['id']))
        i += 1
    tf.close()
    Logger(1, 'vod.m3u8 successful created! (%s Items)' % str(i))

    if os.path.exists(os.path.join(listpath, 'series.m3u8')):
        os.remove(os.path.join(listpath, 'series.m3u8'))
    tf = open(os.path.join(listpath, 'series.m3u8'), "w")
    tf.write("#EXTM3U")
    hurl = 'http://'+str(ip())+':'+str(com.get_setting('server_port', 'Main'))
    j = 0
    for row in cur.execute('SELECT * FROM streams WHERE media_type="tvshow" ORDER BY site, name, season, episode'):
        if "Episoden" in row['episode']: ep = re.sub('Episoden ', '', row['episode'])
        else: ep = row['episode']
        if row['season'] == '' or row['season'] == 'NULL' or row['season'] == None: se = 0
        else: se = row['season']
        name = 'S'+se+'E'+ep
        if row['thumb'].startswith('http'): tf.write('\n#EXTINF:-1 group-title="%s" tvg-logo="%s" tvg-id="show%s",%s' % (row['name'], row['thumb'], row['id'], name))
        else: tf.write('\n#EXTINF:-1 group-title="%s" tvg-id="s%s",%s' % (row['name'], row['id'], name))
        tf.write('\n%s/stream/%s' % (hurl, row['id']))
        j += 1
    tf.close()
    Logger(1, 'series.m3u8 successful created! (%s Items)' % str(j))

    return True


def getHoster(data):
    site = getattr(sites, data['site'])
    entry = data['url']
    if data['p2'] != '': hosts = site.showHosters(entry, data['p2'])
    else: hosts = site.showHosters(entry)
    if hosts:
        return hosts
    return None


def getHosterUrl(l, s):
    site = getattr(sites, s)
    entry = l
    host = site.getHosterUrl(entry)
    if host:
        return host
    return None


def getStream(data):
    #Logger(data)
    link = resolver.resolve(data)
    if link:
        return link
    return None


def search(search):
    loads = []
    q = []
    c = []
    l = []
    e = []
    ee = {}
    E = []
    a = 0
    for site in sites.sites:
        if bool(int(com.get_setting(site.SITE_IDENTIFIER+'_search', 'Xstream'))) == True:
            load = site.search(search)
            if load:
                loads.append(load)
    if len(loads) > 0:
        for i in range(0, len(loads)):
            for x in range(0, len(loads[i])):
                c.append((loads[i][x]["name"]+' ('+loads[i][x]["site"]+')', str(a)))
                l.append(loads[i][x])
                a += 1
    q.append(inquirer.Checkbox("select", message="Select Items", choices=c))
    r = inquirer.prompt(q)
    for s in r['select']:
        select = l[int(s)]
        if not select['key'] == 'showHosters':
            site = getattr(sites, select['site'])
            key = getattr(site, select['key'])
            if 'p2' in select: select['entries'] = key(select['url'], select['p2'])
            else: select['entries'] = key(select['url'])
            if select['entries']:
                for entry in select['entries']:
                    if not entry['key'] == 'showHosters':
                        site = getattr(sites, entry['site'])
                        key = getattr(site, entry['key'])
                        if "p2" in entry: entry['entries'] = key(entry['url'], entry['p2'])
                        else: entry['entries'] = key(entry['url'])
        if "mediatype" in select:
            if select["mediatype"] == 'movie' or select["mediatype"] == 'tvshow':
                try:
                    if "year" in select: 
                        meta = cTMDB().get_meta(str(select["mediatype"]), str(select["name"]), year=str(select["year"]), advanced='false')
                    else: 
                        meta = cTMDB().get_meta(str(select["mediatype"]), str(select["name"]), advanced='false')
                except Exception:
                    meta = None
        if meta: select["meta"] = meta
        e.append(select)
    if len(e) > 0:
        ee["entries"] = e
        
        E.append(ee)
        db = updateDB(E)
        if db: return True
    return False
