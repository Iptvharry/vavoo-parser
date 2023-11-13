# -*- coding: utf-8 -*-
# Python 3
# Always pay attention to the translations in the menu!
# HTML LangzeitCache hinzugefügt
# showEntries:    6 Stunden
# showSeasons:    6 Stunden
# showEpisodes:   4 Stunden
# Seite vollständig mit JSON erstellt

import json

from helper.requestHandler import cRequestHandler
from helper.tools import cParser

SITE_IDENTIFIER = 'moflix'
SITE_NAME = 'Moflix-Stream'
SITE_ICON = 'moflix-stream.png'

# Domain Abfrage
URL_MAIN = 'https://moflix-stream.xyz/'
# Movie / Series / Search Links
URL_MOVIES = URL_MAIN + 'api/v1/channel/movies?channelType=channel&restriction=&paginate=simple'
URL_SERIES = URL_MAIN + 'api/v1/channel/series?channelType=channel&restriction=&paginate=simple'
URL_SEARCH = URL_MAIN + 'api/v1/search/%s?query=%s&limit=8'
# Hoster
URL_HOSTER = URL_MAIN + 'api/v1/titles/%s?load=images,genres,productionCountries,keywords,videos,primaryVideo,seasons,compactCredits'


def load():
    ret = []
    ret.append({"site": SITE_IDENTIFIER, "url": URL_MOVIES, "typ": 1, "key": "showEntries", "title": "Movies"})
    ret.append({"site": SITE_IDENTIFIER, "url": URL_SERIES, "typ": 2, "key": "showEntries", "title": "Series"})
    return ret


def showEntries(entryUrl=False):
    folder = []
    # Parameter laden
    if not entryUrl: return
    iPage = int(1)
    oRequest = cRequestHandler(entryUrl + '&page=' + str(iPage) if iPage > 0 else entryUrl, ignoreErrors=True)
    oRequest.addHeaderEntry('Referer', entryUrl)
    oRequest.cacheTime = 60 * 60 * 24  # 24 Stunden
    jSearch = json.loads(oRequest.request())  # Lade JSON aus dem Request der URL
    if not 'success' in jSearch['status']: return  # Status success dann weiter
    aResults = jSearch['channel']['content']['data']
    total = len(aResults)
    if len(aResults) == 0: return
    for i in aResults:
        sId = i['id']  # ID des Films / Serie für die weitere URL
        sName = i['name']  # Name des Films / Serie
        if 'is_series' in i: isTvshow = i['is_series']  # Wenn True dann Serie
        oGuiElement = {}
        oGuiElement["name"] = sName
        oGuiElement["site"] = SITE_IDENTIFIER
        oGuiElement["key"] = 'showSeasons' if isTvshow else 'showHosters'
        if 'year' in i and len(str(i['year'])) == 4: oGuiElement["year"] = i['year']  # Suche bei year nach 4 stelliger Zahl
        # sDesc = i['description']
        if 'description' in i and i['description'] != '': oGuiElement["desc"] = i['description']  # Suche nach Desc wenn nicht leer dann setze GuiElement
        # sThumbnail = i['poster']
        if 'poster' in i and i['poster'] != '': oGuiElement["thumb"] = i['poster']  # Suche nach Desc wenn nicht leer dann setze GuiElement
        # sFanart = i['backdrop']
        if 'backdrop' in i and i['backdrop'] != '': oGuiElement["backdrop"] = i['backdrop'] # Suche nach Desc wenn nicht leer dann setze GuiElement
        oGuiElement["mediatype"] = 'tvshow' if isTvshow else 'movie'
        # Parameter übergeben
        oGuiElement["url"] = URL_HOSTER % sId
        folder.append(oGuiElement)
    return folder


def showSeasons(entryUrl=False):
    folder = []
    if not entryUrl: return
    oRequest = cRequestHandler(entryUrl)
    oRequest.addHeaderEntry('Referer', entryUrl)
    oRequest.cacheTime = 60 * 60 * 24  # 24 Stunden
    jSearch = json.loads(oRequest.request()) # Lade JSON aus dem Request der URL
    if not 'success' in jSearch['status']: return # Status success dann weiter
    sDesc = jSearch['title']['description'] # Lade Beschreibung aus JSON
    aResults = jSearch['seasons']['data']
    aResults = sorted(aResults, key=lambda k: k['number'])  # Sortiert die Staffeln nach Nummer aufsteigend
    total = len(aResults)
    if len(aResults) == 0: return
    for i in aResults:
        sId = i['title_id'] # ID ändert sich !!!
        sSeasonNr = str(i['number']) # Staffel Nummer
        oGuiElement = {}
        oGuiElement["name"] = 'Staffel ' + sSeasonNr
        oGuiElement["site"] = SITE_IDENTIFIER
        oGuiElement["key"] = 'showEpisodes'
        oGuiElement["url"] = sId
        oGuiElement["p2"] = sSeasonNr
        oGuiElement["mediatype"] = 'season'
        oGuiElement["s"] = sSeasonNr
        if sDesc != '': oGuiElement["desc"] = sDesc
        folder.append(oGuiElement)
    return folder


def showEpisodes(sId=False, sSeasonNr=False):
    folder = []
    if not sId: return
    if not sSeasonNr: return
    sUrl = URL_MAIN + 'api/v1/titles/%s/seasons/%s?load=episodes,primaryVideo' % (sId, sSeasonNr)
    oRequest = cRequestHandler(sUrl)
    oRequest.addHeaderEntry('Referer', sUrl)
    oRequest.cacheTime = 60 * 60 * 24  # 24 Stunden
    jSearch = json.loads(oRequest.request()) # Lade JSON aus dem Request der URL
    if not 'success' in jSearch['status']: return # Status success dann weiter
    aResults = jSearch['episodes']['data'] # Ausgabe der Suchresultate von jSearch
    total = len(aResults) # Anzahl aller Ergebnisse
    if len(aResults) == 0: return
    for i in aResults:
        sName = i['name'] # Episoden Titel
        sEpisodeNr = str(i['episode_number']) # Episoden Nummer
        sThumbnail = i['poster'] # Episoden Poster
        # Parameter setzen
        #https://cineclix.de/api/v1/titles/2858/seasons/2/episodes/2?load=videos,compactCredits,primaryVideo
        oGuiElement = {}
        if 'description' in i and i['description'] != '': oGuiElement["desc"] = i['description'] # Suche nach Desc wenn nicht leer dann setze GuiElement
        oGuiElement["name"] = 'Episode ' + sEpisodeNr + ' - ' + sName
        oGuiElement["site"] = SITE_IDENTIFIER
        oGuiElement["key"] = 'showHosters'
        oGuiElement["thumb"] = sThumbnail
        oGuiElement["url"] = URL_MAIN + 'api/v1/titles/%s/seasons/%s/episodes/%s?load=videos,compactCredits,primaryVideo' % (sId, sSeasonNr, sEpisodeNr)
        oGuiElement["p2"] = 'episode'
        oGuiElement["mediatype"] = 'episode'
        oGuiElement["s"] = sSeasonNr
        oGuiElement["e"] = sEpisodeNr
        oGuiElement["total"] = total
        folder.append(oGuiElement)
    return folderentryUrl


def showSearchEntries(entryUrl=False, sSearchText=''):
    folder = []
    # Parameter laden
    if not entryUrl: return
    oRequest = cRequestHandler(entryUrl, ignoreErrors=True)
    oRequest.addHeaderEntry('Referer', entryUrl)
    jSearch = json.loads(oRequest.request()) # Lade JSON aus dem Request der URL
    if not 'success' in jSearch['status']: return # Status success dann weiter
    aResults = jSearch['results'] # Ausgabe der Suchresultate von jSearch
    total = len(aResults) # Anzahl aller Ergebnisse
    if len(aResults) == 0: return # Wenn Resultate 0 zeige Benachrichtigung
    isTvshow = False
    for i in aResults:
        if 'person' in i['model_type']: continue # Personen in der Suche ausblenden
        sId = i['id']   # ID des Films / Serie für die weitere URL
        sName = i['name'] # Name des Films / Serie
        if sSearchText.lower() and not cParser().search(sSearchText, sName.lower()): continue
        if 'is_series' in i: isTvshow = i['is_series'] # Wenn True dann Serie
        oGuiElement = {}
        if 'year' in i and len(str(i['year'])) == 4: oGuiElement["year"] = i['year'] # Suche bei year nach 4 stelliger Zahl
        #sDesc = i['description']
        if 'description' in i and i['description'] != '': oGuiElement["desc"] = i['description'] # Suche nach Desc wenn nicht leer dann setze GuiElement
        # sThumbnail = i['poster']
        if 'poster' in i and i['poster'] != '': oGuiElement["thumb"] = i['poster'] # Suche nach Desc wenn nicht leer dann setze GuiElement
        # sFanart = i['backdrop']
        if 'backdrop' in i and i['backdrop'] != '': oGuiElement["backdrop"] = i['backdrop'] # Suche nach Desc wenn nicht leer dann setze GuiElement
        # Parameter setzen
        oGuiElement["name"] = sName
        oGuiElement["site"] = SITE_IDENTIFIER
        oGuiElement["key"] = 'showSeasons' if isTvshow else 'showHosters'
        oGuiElement["url"] = URL_HOSTER % sId
        oGuiElement["p2"] = 'tvshow' if isTvshow else 'movie'
        oGuiElement["mediatype"] = 'tvshow' if isTvshow else 'movie'
        oGuiElement["total"] = total
        folder.append(oGuiElement)
    return folder


def isBlockedHoster(domain, checkResolver=True ):
    domain = urlparse(domain).path if urlparse(domain).hostname == None else urlparse(domain).hostname
    hostblockDict = ['flashx','streamlare','evoload']  # permanenter Block
    for i in hostblockDict:
        if i in domain.lower() or i.split('.')[0] in domain.lower(): return True, domain
    if checkResolver:   # Überprüfung in resolveUrl
        if resolver.relevant_resolvers(domain=domain) == []:
            print('[xStream] -> [isblockedHoster]: In resolveUrl no domain for url: %s' % domain)
            return True, domain    # Domain nicht in resolveUrl gefunden
    return False, domain


def showHosters(entryUrl=False, mediaType=False):
    hosters = []
    sUrl = ParameterHandler().getValue('entryUrl')
    oRequest = cRequestHandler(sUrl)
    oRequest.addHeaderEntry('Referer', sUrl)
    jSearch = json.loads(oRequest.request())  # Lade JSON aus dem Request der URL
    if not 'success' in jSearch['status']: return  # Status success dann weiter
    if mediaType == 'movie': #Bei MediaTyp Filme nutze das Result
        aResults = jSearch['title']['videos'] # Ausgabe der Suchresultate von jSearch für Filme
    else:
        aResults = jSearch['episode']['videos'] # Ausgabe der Suchresultate von jSearch für Episoden
    # total = len(aResults)  # Anzahl aller Ergebnisse
    if len(aResults) == 0: return
    for i in aResults:
        sName = i['name'].split('-')[0].strip()
        sQuality = str(i['quality'])
        if sQuality != '': sQuality = '720p'
        sUrl = i['src']
        if isBlockedHoster(sUrl)[0]: continue  # Hoster aus settings.xml oder deaktivierten Resolver ausschließen
        if 'youtube' in sUrl: continue # Trailer ausblenden
        hoster = {'link': sUrl, 'name': sName, 'displayedName': '%s [I][%s][/I]' % (sName, sQuality), 'quality': sQuality, 'resolveable': True}
        hosters.append(hoster)
    if hosters:
        hosters.append('getHosterUrl')
    return hosters


def getHosterUrl(sUrl=False):
    return [{'streamUrl': sUrl, 'resolved': False}]


def search(sSearchText):
    sID1 = cParser().quote(sSearchText)
    sID2 = cParser().quotePlus(sSearchText)
    find = showSearchEntries(URL_SEARCH % (sID1, sID2), sSearchText)
    if find:
        if len(find) > 0:
            return find
    return None

