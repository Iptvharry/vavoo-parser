# -*- coding: utf-8 -*-
# Python 3
# Always pay attention to the translations in the menu!
# HTML LangzeitCache hinzugefügt
    #showGenre:     48 Stunden
    #showEntries:    6 Stunden
    #showSeasons:    6 Stunden
    #showEpisodes:   4 Stunden

import base64
import binascii
import random
import string

from helper.requestHandler import cRequestHandler
from helper.tools import cParser, cUtil

from resources.lib import jsunpacker
from itertools import zip_longest as ziplist

SITE_IDENTIFIER = 'kinoger'
SITE_NAME = 'Kinoger'
SITE_ICON = 'kinoger.png'

# Domain Abfrage
URL_MAIN = 'https://kinoger.com' # + cConfig().getSetting('plugin_kinoger.domain')
URL_SERIES = URL_MAIN + '/stream/serie/'


def load():
    ret = []
    ret.append({"site": SITE_IDENTIFIER, "url": URL_MAIN, "typ": 1, "key": "showEntries", "title": "New"})
    ret.append({"site": SITE_IDENTIFIER, "url": URL_SERIES, "typ": 2, "key": "showEntries", "title": "Series"})
    return ret


def showEntries(entryUrl=False, sSearchText=False):
    folder = []
    if not entryUrl: return
    oRequest = cRequestHandler(entryUrl, ignoreErrors=True)
    oRequest.cacheTime = 60 * 60 * 24  # 6 Stunden
    if sSearchText:
        oRequest.addParameters('story', sSearchText)
        oRequest.addParameters('do', 'search')
        oRequest.addParameters('subaction', 'search')
        oRequest.addParameters('x', '0')
        oRequest.addParameters('y', '0')
        oRequest.addParameters('titleonly', '3')
        oRequest.addParameters('submit', 'submit')
    else:
        oRequest.addParameters('dlenewssortby', 'date')
        oRequest.addParameters('dledirection', 'desc')
        oRequest.addParameters('set_new_sort', 'dle_sort_main')
        oRequest.addParameters('set_direction_sort', 'dle_direction_main')
    sHtmlContent = oRequest.request()
    pattern = 'class="title".*?' # container start
    pattern += 'href="([^"]+)' # url
    pattern += '">([^<]+).*?' # name
    pattern += 'src="([^"]+)' # thumb
    pattern += '(.*?)</span>' # dummy
    isMatch, aResult = cParser().parse(sHtmlContent, pattern)
    if not isMatch: return

    total = len(aResult)
    for sUrl, sName, sThumbnail, sDummy in aResult:
        if sSearchText and not cParser().search(sSearchText, sName):
            continue
        isTvshow = True if 'staffel' in sName.lower() or 'serie' in entryUrl or ';">S0' in sDummy else False
        isYear, sYear = cParser.parse(sName, '(.*?)\((\d*)\)') # Jahr und Name trennen
        for name, year in sYear:
            sName = name
            sYear = year
            break
        isDesc, sDesc = cParser.parseSingleResult(sDummy, '</b>([^<]+)') # Beschreibung
        isDuration, sDuration = cParser.parseSingleResult(sDummy, '(?:Laufzeit|Spielzeit).*?([\d]+)') # Laufzeit
        oGuiElement = {}
        oGuiElement["name"] = sName
        oGuiElement["site"] = SITE_IDENTIFIER
        oGuiElement["key"] = 'showSeasons' if isTvshow else 'showHosters'
        oGuiElement["thumb"] = sThumbnail
        oGuiElement["url"] = sUrl
        oGuiElement["mediatype"] = 'tvshow' if isTvshow else 'movie'
        oGuiElement["total"] = total
        if isYear:
            oGuiElement["year"] = sYear
        if isDesc:
            oGuiElement["desc"] = sDesc
        if isDuration:
            oGuiElement["duration"] = sDuration
        folder.append(oGuiElement)
    return folder


def showSeasons(entryUrl=False, sThumbnail=False, sTVShowTitle=False):
    folder = []
    oRequest = cRequestHandler(entryUrl, ignoreErrors=True)
    oRequest.cacheTime = 60 * 60 * 24  # HTML Cache Zeit 6 Stunden
    sHtmlContent = oRequest.request()
    L11 = []
    isMatchsst, sstsContainer = cParser.parseSingleResult(sHtmlContent, 'sst.show.*?</script>')
    if isMatchsst:
        sstsContainer = sstsContainer.replace('[', '<').replace(']', '>')
        isMatchsst, L11 = cParser.parse(sstsContainer, "<'([^>]+)")
        if isMatchsst:
            total = len(L11)
    L22 = []
    isMatchollhd, ollhdsContainer = cParser.parseSingleResult(sHtmlContent, 'ollhd.show.*?</script>')
    if isMatchollhd:
        ollhdsContainer = ollhdsContainer.replace('[', '<').replace(']', '>')
        isMatchollhd, L22 = cParser.parse(ollhdsContainer, "<'([^>]+)")
        if isMatchollhd:
            total = len(L22)
    L33 = []
    isMatchpw, pwsContainer = cParser.parseSingleResult(sHtmlContent, 'pw.show.*?</script>')
    if isMatchpw:
        pwsContainer = pwsContainer.replace('[', '<').replace(']', '>')
        isMatchpw, L33 = cParser.parse(pwsContainer, "<'([^>]+)")
        if isMatchpw:
            total = len(L33)

    L44 = []
    isMatchgo, gosContainer = cParser.parseSingleResult(sHtmlContent, 'go.show.*?</script>')
    if isMatchgo:
        gosContainer = gosContainer.replace('[', '<').replace(']', '>')
        isMatchgo, L44 = cParser.parse(gosContainer, "<'([^>]+)")
        if isMatchgo:
            total = len(L44)

    isDesc, sDesc = cParser.parseSingleResult(sHtmlContent, '</b>([^"]+)<br><br>')
    for i in range(0, total):
        try:
            params.setParam('L11', L11[i])
        except Exception:
            pass
        try:
            params.setParam('L22', L22[i])
        except Exception:
            pass
        try:
            params.setParam('L33', L33[i])
        except Exception:
            pass
        try:
            params.setParam('L44', L44[i])
        except Exception:
            pass
        i = i + 1
        oGuiElement = {}
        if isDesc: oGuiElement["desc"] = sDesc
        oGuiElement["name"] = 'Staffel ' + str(i)
        oGuiElement["season"] = i
        oGuiElement["site"] = SITE_IDENTIFIER
        oGuiElement["key"] = 'showEpisodes'
        if sThumbnail: oGuiElement["thumb"] = sThumbnail
        oGuiElement["url"] = entryUrl
        oGuiElement["mediatype"] = 'season'
        if sTVShowTitle: oGuiElement["title"] = sTVShowTitle
        oGuiElement["total"] = total
        folder.append(oGuiElement)
    return folder


def showEpisodes(sSeasonNr=False, sThumbnail=False, sTVShowTitle=False, sDesc=False):
    folder = []
    L11 = []
    if params.exist('L11'):
        L11 = params.getValue('L11')
        isMatch1, L11 = cParser.parse(L11, "(http[^']+)")
    L22 = []
    if params.exist('L22'):
        L22 = params.getValue('L22')
        isMatch, L22 = cParser.parse(L22, "(http[^']+)")
    L33 = []
    if params.exist('L33'):
        L33 = params.getValue('L33')
        isMatch3, L33 = cParser.parse(L33, "(http[^']+)")
    L44 = []
    if params.exist('L44'):
        L44 = params.getValue('L44')
        isMatch4, L44 = cParser.parse(L44, "(http[^']+)")
    liste = ziplist(L11, L22, L33, L44)
    i = 0
    for sUrl in liste:
        i = i + 1
        oGuiElement = {}
        oGuiElement["sName"] = 'Episode ' + str(i)
        oGuiElement["e"] = i
        oGuiElement["site"] = SITE_IDENTIFIER
        oGuiElement["key"] = 'showHosters'
        oGuiElement["url"] = sUrl
        oGuiElement["mediatype"] = 'episode'
        folder.append(oGuiElement)
    return folder


def showHosters(sLinks=False, entryUrl=False):
    hosters = []
    headers = '&Accept-Language=de%2Cen-US%3Bq%3D0.7%2Cen%3Bq%3D0.3&Accept=%2A%2F%2A&User-Agent=Mozilla%2F5.0+%28Windows+NT+10.0%3B+Win64%3B+x64%3B+rv%3A99.0%29+Gecko%2F20100101+Firefox%2F99.0'
    #params = ParameterHandler()
    if sLinks:
        sUrl = sLinks
        isMatch, aResult = cParser().parse(sUrl, "(http[^']+)")
    else:
        sUrl = entryUrl # params.getValue('entryUrl')
        sHtmlContent = cRequestHandler(sUrl, ignoreErrors=True).request()
        pattern = "show[^>]\d,[^>][^>]'([^']+)"
        isMatch, aResult = cParser().parse(sHtmlContent, pattern)
    if isMatch:
        for sUrl in aResult:
            try:
                if 'kinoger.be' in sUrl:
                    oRequest = cRequestHandler(sUrl, caching=False, ignoreErrors=True)
                    oRequest.addHeaderEntry('Referer', 'https://kinoger.com/')
                    sHtmlContent = oRequest.request() # Durchsucht sHtml Content
                    isMatch, packed = cParser.parseSingleResult(sHtmlContent, '(eval\s*\(function.*?)</script>')
                    if isMatch:
                        sHtmlContent = jsunpacker.unpack(packed)
                    isMatch, j = cParser.parse(sHtmlContent, 'ct":"([^"]+)","iv":"([^"]+)","s":"([^"]+)')
                    if isMatch:
                        try:
                            ciphertext = base64.b64decode(j[0][0])
                            salt = binascii.unhexlify(j[0][2])
                            password = 'XOmurdOgNnjMwYah'.encode('utf-8')
                            sHtmlContent = cUtil.evp_decode(ciphertext, password, salt)
                        except Exception:
                            sHtmlContent = ''
                    isMatch, hUrl = cParser.parseSingleResult(sHtmlContent, 'sources.*?file.*?(http[^"]+)')
                    if isMatch:
                        hUrl = hUrl.replace('\\', '')
                        oRequest = cRequestHandler(hUrl, caching=False, ignoreErrors=True)
                        oRequest.addHeaderEntry('Referer', 'https://kinoger.be/')
                        oRequest.addHeaderEntry('Origin', 'https://kinoger.be')
                        oRequest.removeNewLines(False)
                        sHtmlContent = oRequest.request()
                        pattern = 'RESOLUTION=.*?x(\d+).*?\n([^#"]+)'
                        isMatch, aResult = cParser.parse(sHtmlContent, pattern)
                    if isMatch:
                        for sQuality, sUrl in aResult:
                            sUrl = (hUrl.split('video')[0].strip() + sUrl.strip())
                            sUrl = sUrl + '|Origin=https%3A%2F%2Fkinoger.be&Referer=https%3A%2F%2Fkinoger.be%2F' + headers
                            hoster = {'link': sUrl, 'name': 'Kinoger.be [I][%sp][/I]' % sQuality, 'quality': sQuality, 'resolveable': True}
                            hosters.append(hoster)

                elif 'kinoger.pw' in sUrl: continue # Offline
                elif 'kinoger.re' in sUrl: continue # Offline
                elif 'start.u' in sUrl: continue # Offline
                elif 'delivery' in sUrl: continue
                elif 'cdn0' in sUrl: continue
                elif 'kinoger.ru' in sUrl: continue # Cloudflare aktiv
                elif 'hd-stream.to' in sUrl: continue # Offline
                elif 'protonvideo' in sUrl: continue # Offline

                else:
                    sQuality = '720p'
                    sName = cParser.urlparse(sUrl)
                    for x in (('Kinoger.Be', 'StreamHide'), ('Fsst.Online', 'SecVideo')):
                        sName = sName.replace(*x)
                    hoster = {'link': sUrl + 'DIREKT', 'name': sName, 'displayedName': '%s [I][%s][/I]' % (sName, sQuality), 'quality': sQuality, 'resolveable': True}
                    hosters.append(hoster)
            except Exception:
                pass
    if hosters:
        hosters.append('getHosterUrl')
        return hosters


def getHosterUrl(sUrl=False):
    if sUrl.endswith('DIREKT'):
        if 'kinoger.be' in sUrl:
            sUrl = sUrl.replace('https://kinoger.be/', 'https://streamhide.com/')
            return [{'streamUrl': sUrl[:-6], 'resolved': False}]

        Request = cRequestHandler(sUrl, caching=False)
        Request.request()
        sUrl = Request.getRealUrl()  # hole reale URL von der Umleitung

        return [{'streamUrl': sUrl[:-6], 'resolved': False}]
    else:
        return [{'streamUrl': sUrl, 'resolved': True}]


def search(sSearchText):
    find = showEntries(URL_MAIN, sSearchText)
    if find:
        if len(find) > 0:
            return find
    return None


def get_streamsburl(host, media_id): # StreamSB Url Abfrage
    # Copyright (c) 2019 vb6rocod

    def makeid(length):
        t = string.ascii_letters + string.digits
        return ''.join([random.choice(t) for _ in range(length)])

    x = '{0}||{1}||{2}||streamsb'.format(makeid(12), media_id, makeid(12))
    c1 = binascii.hexlify(x.encode('utf8')).decode('utf8')
    x = '7Vd5jIEF2lKy||nuewwgxb1qs'
    c2 = binascii.hexlify(x.encode('utf8')).decode('utf8')
    return 'https://{0}/{1}7/{2}'.format(host, c2, c1)
