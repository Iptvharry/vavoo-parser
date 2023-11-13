import requests, random, sys, os, json, urllib3, time, re, urllib, base64, codecs, threading, gzip, ssl, signal
from base64 import b64encode, b64decode
from time import sleep
from datetime import date, datetime
from unidecode import unidecode
from urllib.parse import urlencode, urlparse, parse_qsl, quote_plus
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from multiprocessing import Process, Queue

from utils.common import get_ip_address as ip
from utils.common import Logger as Logger
import utils.common as com
import resolveurl as resolver

unicode = str
urllib3.disable_warnings()
session = requests.session()
BASEURL = "https://www2.vavoo.to/ccapi/"

cachepath = com.cp
con = com.con
_path = com.lp


def getAuthSignature():
    key = com.get_setting('signkey')
    if key:
        ip = com.get_public_ip()
        now = int(time.time())*1000
        jkey = json.loads(json.loads(base64.b64decode(key.encode('utf-8')).decode('utf-8'))['data'])
        if 'ips' in jkey:
            key_ip = jkey['ips'][0]
        if 'app' in jkey and 'ok' in jkey['app']:
            key_ok = jkey['app']['ok']
        if 'validUntil' in jkey:
            valid = int(jkey['validUntil'])
        if ip == key_ip and key_ok == True and valid > now: return key
    veclist = com.get_cache('veclist')
    if not veclist:
        veclist=requests.get("https://raw.githubusercontent.com/michaz1988/michaz1988.github.io/master/data.json").json()
        com.set_cache('veclist', veclist)
    sig = None
    i = 0
    while (not sig and i < 50):
        i+=1
        vec = {"vec": random.choice(veclist)}
        req = requests.post('https://www.vavoo.tv/api/box/ping2', data=vec).json()
        if req.get('signed'):
            sig = req['signed']
        elif req.get('data', {}).get('signed'):
            sig = req['data']['signed']
        elif req.get('response', {}).get('signed'):
            sig = req['response']['signed']
    com.set_setting('signkey', sig)
    return sig


def callApi(action, params, method="GET", headers=None, **kwargs):
    if not headers: headers = dict()
    headers["auth-token"] = getAuthSignature()
    resp = session.request(method, (BASEURL + action), params=params, headers=headers, **kwargs)
    if resp:
        resp.raise_for_status()
        data = resp.json()
        return data
    else: return


def callApi2(action, params):
    res = callApi(action, params, verify=False)
    while True:
        if type(res) is not dict or "id" not in res or "data" not in res:
            return res
        data = res["data"]
        if type(data) is dict and data.get("type") == "fetch":
            params = data["params"]
            body = params.get("body")
            headers = params.get("headers")
            try: resp = session.request(params.get("method", "GET").upper(), data["url"], headers={k:v[0] if type(v) in (list, tuple) else v for k, v in headers.items()} if headers else None, data=body.decode("base64") if body else None, allow_redirects=params.get("redirect", "follow") == "follow")
            except: return
            headers = dict(resp.headers)
            resData = {"status": resp.status_code, "url": resp.url, "headers": headers, "data": b64encode(resp.content).decode("utf-8").replace("\n", "") if data["body"] else None}
            log(json.dumps(resData))
            log(resp.text)
            res = callApi("res", {"id": res["id"]}, method="POST", json=resData, verify=False)
        elif type(data) is dict and data.get("error"):
            log(data.get("error"))
            return
        else: return data


def getStream(url):
    link = None
    link = resolver.resolve(url)
    return link


def getLinks(action, params):
    data = callApi2(action, params)
    if data:
        arr = {}
        arr["1"] = []
        arr["2"] = []
        arr["3"] = []
        for d in data:
            if d["language"] == "de":
                if "1080p" in d["name"]: arr["1"].append(d["url"])
                elif "720p" in d["name"]: arr["2"].append(d["url"])
                else: arr["3"].append(d["url"])
        urls = []
        if len(arr["1"]) > 0:
            for u in arr["1"]:
                urls.append(u)
        if len(arr["2"]) > 0:
            for u in arr["2"]:
                urls.append(u)
        if len(arr["3"]) > 0:
            for u in arr["3"]:
                urls.append(u)
        if len(urls) > 0:
            return urls
            #for url in urls:
                #try:
                    #sLink = resolver.resolve(url)
                    #return sLink
                #except:
                    #return


def sky_m3u8():
    hurl = 'http://'+str(com.get_setting('server_ip', 'Main'))+':'+str(com.get_setting('server_port', 'Main'))
    Logger(1, 'Starting with URL: %s ...' % str(hurl), 'm3u8', 'process')
    #url = 'https://www2.vavoo.to/live2/index'
    matches1 = ["13TH", "AXN", "A&E", "INVESTIGATION", "TNT", "DISNEY", "SKY", "WARNER"]
    matches2 = ["BUNDESLIGA", "SPORT", "TELEKOM"]
    matches3 = ["CINE", "EAGLE", "KINO", "FILMAX", "POPCORN"]
    groups = []
    epg_logos = com.get_setting('epg_logos')
    epg_rytec = com.get_setting('epg_rytec')
    m3u8_name = com.get_setting('m3u8_name')
    epg_provider = com.get_setting('epg_provider')

    cur = con.cursor()

    ssl._create_default_https_context = ssl._create_unverified_context
    req = Request('https://www2.vavoo.to/live2/index?output=json', headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36'})
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    response = urlopen(req)
    content = response.read().decode('utf8')
    channel = json.loads(content)

    for c in channel:
        url = c['url']
        country = c['group']
        group = country
        if group not in groups:
            groups.append(group)
            cur.execute('SELECT * FROM categories WHERE category_name="' + group + '" AND media_type="' + str('live') + '"')
            test = cur.fetchone()
            if not test:
                cur.execute('INSERT INTO categories VALUES (NULL,"' + str('live') + '","' + str(group) + '",NULL)')
        if group == 'Germany':
            if any(x in c['name'] for x in matches1):
                group = 'Sky'
            if any(x in c['name'] for x in matches2):
                group = 'Sport'
            if any(x in c['name'] for x in matches3):
                group = 'Cine'
        cur.execute('SELECT * FROM categories WHERE category_name="' + group + '" AND media_type="' + str('live') + '"')
        data = cur.fetchone()
        cid = data['category_id']
        cur.execute('SELECT * FROM channel WHERE name="' + c['name'].encode('ascii', 'ignore').decode('ascii') + '" AND grp="' + group + '"')
        test = cur.fetchone()
        if not test:
            name = re.sub('( (AUSTRIA|AT|HEVC|RAW|SD|HD|FHD|UHD|H265|GERMANY|DEUTSCHLAND|1080|DE|S-ANHALT|SACHSEN|MATCH TIME))|(\\+)|( \\(BACKUP\\))|\\(BACKUP\\)|( \\([\\w ]+\\))|\\([\\d+]\\)', '', c['name'].encode('ascii', 'ignore').decode('ascii'))
            logo = c['logo']
            tid = ''
            ti = ''
            if c['group'] == 'Germany':
                cur.execute('SELECT * FROM epgs WHERE name="' + name + '" OR name1="' + name + '" OR name2="' + name + '" OR name3="' + name + '" OR name4="' + name + '" OR name5="' + name + '"')
                test = cur.fetchone()
                if test:
                    tid = str(test['id'])
            cur.execute('INSERT INTO channel VALUES(NULL,"' + c['name'].encode('ascii', 'ignore').decode('ascii') + '","' + group + '","' + logo + '","' + tid + '","' + c['url'] + '","' + name + '","' + str(country) + '","' + str(cid) + '","' + str(ti) + '")')
        else:
            cur.execute('UPDATE channel SET url="' + c['url'] + '" WHERE name="' + c['name'].encode('ascii', 'ignore').decode('ascii') + '" AND grp="' + group + '"')
    con.commit()

    for group in groups:
        if os.path.exists("%s/%s.m3u8" % (_path, re.sub(' ', '_', group))):
            os.remove("%s/%s.m3u8" % (_path, re.sub(' ', '_', group)))
        Logger(1, 'creating %s.m3u8 ...' % str(re.sub(' ', '_', group)))
        tf = open("%s/%s.m3u8" % (_path, re.sub(' ', '_', group)), "w")
        tf.write("#EXTM3U")
        tf.close()

    for c in channel:
        group = c['group']
        if c['group'] not in groups:
            groups.append(c['group'])
        if c['group'] == 'Germany':
            if any(x in c['name'] for x in matches1):
                group = 'Sky'
            if any(x in c['name'] for x in matches2):
                group = 'Sport'
            if any(x in c['name'] for x in matches3):
                group = 'Cine'

        cur.execute('SELECT * FROM channel WHERE name="' + c['name'].encode('ascii', 'ignore').decode('ascii') + '" AND grp="' + group + '"')
        row = cur.fetchone()
        if row:
            tid = None
            name = None
            logo = None
            if not str(row['tid']) == '':
                cur.execute('SELECT * FROM epgs WHERE id="' + row['tid'] + '"')
                dat = cur.fetchone()
                if epg_rytec == '1': tid = dat['rid']
                elif epg_provider == 'm':
                    if not dat['mn'] == None: tid = dat['mn']
                elif epg_provider == 't':
                    if not dat['tn'] == None: tid = dat['tn']
                if epg_logos == 'p':
                    if epg_provider == 'm':
                        if not dat['ml'] == None: logo = dat['ml']
                    elif epg_provider == 't':
                        if not dat['tl'] == None: logo = dat['tl']
                elif epg_logos == 'o':
                    if not dat['ol'] == None: logo = dat['ol']
                if m3u8_name == '1':
                    if not dat['display'] == None: name = dat['display']
                    else: name = row['display']
                else: name = row['name']
            else:
                if m3u8_name == '1': name = row['display']
                else: name = row['name']
                if not str(row['logo']) == '': logo = row['logo']

            tf = open("%s/%s.m3u8" % (_path, c['group']), "a")
            if not logo == None and not tid == None:
                tf.write('\n#EXTINF:-1 tvg-name="%s" group-title="%s" tvg-logo="%s" tvg-id="%s",%s' % (row['name'], row['grp'], logo, tid, name))
            elif not logo == None and tid == None:
                tf.write('\n#EXTINF:-1 tvg-name="%s" group-title="%s" tvg-logo="%s",%s' % (row['name'], row['grp'], logo, name))
            elif not tid == None and logo == None:
                tf.write('\n#EXTINF:-1 tvg-name="%s" group-title="%s" tvg-id="%s",%s' % (row['name'], row['grp'], tid, name))
            else:
                tf.write('\n#EXTINF:-1 tvg-name="%s" group-title="%s",%s' % (row['name'], row['grp'], name))
            tf.write('\n#EXTVLCOPT:http-user-agent=VAVOO/2.6')
            tf.write('\n%s/channel/%s' % (hurl, row['id']))
            tf.close()
        else:
            Logger(3, 'Error!', 'm3u8', 'process')
    Logger(1, 'Done!', 'm3u8', 'process')

