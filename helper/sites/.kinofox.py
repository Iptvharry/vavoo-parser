# -*- coding: utf-8 -*-
# Python 3
# Always pay attention to the translations in the menu!
# HTML LangzeitCache hinzugefügt
    #showGenre:     48 Stunden
    #showEntries:    6 Stunden

from helper.requestHandler import cRequestHandler
from helper.tools import cParser


SITE_IDENTIFIER = 'kinofox'
SITE_NAME = 'KinoFox'
SITE_ICON = 'kinofox.png'

URL_MAIN = 'https://kinofox.su'
URL_SEARCH = URL_MAIN + '/index.php?do=search'


def load():
    ret = []
    ret.append({"site": SITE_IDENTIFIER, "url": URL_MAIN, "typ": 1, "key": "showEntries", "title": "Movies"})
    return ret


def showEntries(entryUrl=False, sSearchText=False):
    folder = []
    if not entryUrl: return
    oRequest = cRequestHandler(entryUrl, ignoreErrors=True)
    oRequest.cacheTime = 60 * 60 * 24  # 6 Stunden
    if sSearchText:
        oRequest.addParameters('do', 'search')
        oRequest.addParameters('subaction', 'search')
        oRequest.addParameters('search_start', '0')
        oRequest.addParameters('full_search', '1')
        oRequest.addParameters('result_from', '1')
        oRequest.addParameters('story', sSearchText)
        oRequest.addParameters('titleonly', '3')
    sHtmlContent = oRequest.request() 
    pattern = 'short clearfix.*?href="([^"]+).*?title">([^<]+).*?img src="([^"]+).*?short-label sl-y">([^<]+)'
    isMatch, aResult = cParser.parse(sHtmlContent, pattern)
    if not isMatch: return

    total = len(aResult)
    for sUrl, sName, sThumbnail, sQuality in aResult:
        if sSearchText and not cParser().search(sSearchText, sName):
            continue
        if 'taffel' in sName:
            continue
        if 'railer' in sQuality:
            continue
        oGuiElement = {}
        oGuiElement["name"] = sName
        oGuiElement["site"] = SITE_IDENTIFIER
        oGuiElement["key"] = 'showHosters'
        oGuiElement["url"] = sUrl
        oGuiElement["mediatype"] = 'movie'
        oGuiElement["total"] = total
        oGuiElement["quality"] = sQuality
        if sThumbnail.startswith('/'):
            oGuiElement["thumb"] = URL_MAIN + sThumbnail
        else:
            oGuiElement["thumb"] = sThumbnail
        folder.append(oGuiElement)
    return folder


def showHosters(entryUrl=False):
    hosters = []
    sUrl = entryUrl # ParameterHandler().getValue('entryUrl')
    sHtmlContent = cRequestHandler(sUrl).request()
    isMatch, aResult = cParser.parse(sHtmlContent, 'iframe src="([^"]+)')
    if isMatch:
        for sUrl in aResult:
            sName = cParser.urlparse(sUrl)
            hoster = {'link': sUrl, 'name': cParser.urlparse(sUrl)}
            hosters.append(hoster)
    if hosters:
        hosters.append('getHosterUrl')
    return hosters


def getHosterUrl(entryUrl=False):
    Request = cRequestHandler(entryUrl, caching=False)
    Request.request()
    sUrl = Request.getRealUrl()  # hole reale URL von der Umleitung
    return [{'streamUrl': sUrl, 'resolved': False}]


def search(sSearchText):
    find = showEntries(URL_SEARCH, sSearchText)
    if find:
        if len(find) > 0:
            return find
    return None

