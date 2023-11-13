# -*- coding: utf-8 -*-
# Python 3
import io, gzip, time, re, socket, os, sys, hashlib, json

from urllib.parse import quote, urlencode, urlparse
from urllib.error import HTTPError, URLError
from urllib.request import HTTPHandler, HTTPSHandler, HTTPCookieProcessor, build_opener, Request, HTTPRedirectHandler
from http.cookiejar import LWPCookieJar, Cookie
from http.client import HTTPException

#from utils.common import Logger as Logger


class cRequestHandler:
    def __init__(self, sUrl, caching=True, ignoreErrors=False, compression=True, jspost=False, ssl_verify=False):
        self._sUrl = sUrl
        self._sRealUrl = ''
        self._USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0'
        self._aParameters = {}
        self._headerEntries = {}
        self._profilePath = '.'
        self._cachePath = ''
        self._cookiePath = ''
        self._Status = ''
        self._sResponseHeader = ''
        self.ignoreDiscard(False)
        self.ignoreExpired(False)
        self.caching = caching
        self.ignoreErrors = ignoreErrors
        self.compression = compression
        self._ssl_verify = ssl_verify
        self.jspost = jspost
        self.cacheTime = 600
        self.requestTimeout = 10
        self.removeBreakLines(True)
        self.removeNewLines(True)
        self.__setDefaultHeader()
        self.setCachePath()
        self.__setCookiePath()
        socket.setdefaulttimeout(self.requestTimeout)

    def getStatus(self):
        return self._Status

    def removeNewLines(self, bRemoveNewLines):
        self.__bRemoveNewLines = bRemoveNewLines

    def removeBreakLines(self, bRemoveBreakLines):
        self.__bRemoveBreakLines = bRemoveBreakLines

    def addHeaderEntry(self, sHeaderKey, sHeaderValue):
        self._headerEntries[sHeaderKey] = sHeaderValue

    def getHeaderEntry(self, sHeaderKey):
        if sHeaderKey in self._headerEntries:
            return self._headerEntries[sHeaderKey]

    def addParameters(self, key, value, Quote=False):
        if not Quote:
            self._aParameters[key] = value
        else:
            self._aParameters[key] = quote(str(value))

    def getResponseHeader(self):
        return self._sResponseHeader

    def getRealUrl(self):
        return self._sRealUrl

    def getRequestUri(self):
        return self._sUrl + '?' + urlencode(self._aParameters)

    def __setDefaultHeader(self):
        self.addHeaderEntry('User-Agent', self._USER_AGENT)
        self.addHeaderEntry('Accept-Language', 'de,en-US;q=0.7,en;q=0.3')
        self.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8')
        if self.compression:
            self.addHeaderEntry('Accept-Encoding', 'gzip, deflate')

    def request(self):
        # für Leerzeichen und Umlaute in der sUrl
        for t in (('²', '&#xB2;'), ('³', '&#xB3;'), ('´', '&#xB4;'), ("'", "&#x27;"),('`', '&#x60;'), ('Ä', '&#xC4;'), ('ä', '&#xE4;'),
                  ('Ö', '&#xD6;'), ('ö', '&#xF6;'), ('Ü', '&#xDC;'), ('ü', '&#xFC;'), ('ß', '&#xDF;'), ('¼', '&#xBC;'), ('½', '&#xBD;'),
                  ('¾', '&#xBE;'), ('⅓', '&#8531;'), ('*', '&#x2A;')):
            self._sUrl = self._sUrl.replace(*t)
        if self.caching and self.cacheTime > 0:
            sContent = self.readCache(self.getRequestUri())
            if sContent:
                self._Status = '200'
                return sContent
        cookieJar = LWPCookieJar(filename=self._cookiePath)
        try:
            cookieJar.load(ignore_discard=self.__bIgnoreDiscard, ignore_expires=self.__bIgnoreExpired)
        except Exception as e:
            print( e)
        if self.jspost:
            sParameters = json.dumps(self._aParameters).encode()
        else:
            sParameters = urlencode(self._aParameters, True).encode()

        if self._ssl_verify:
            handlers = [HTTPSHandler()]
        else:
            import ssl
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            handlers = [HTTPSHandler(context=ssl_context)]

        handlers += [HTTPHandler(), HTTPCookieProcessor(cookiejar=cookieJar), RedirectFilter()]
        opener = build_opener(*handlers)
        oRequest = Request(self._sUrl, sParameters if len(sParameters) > 0 else None)

        for key, value in self._headerEntries.items():
            oRequest.add_header(key, value)
        if self.jspost:
            oRequest.add_header('Content-Type', 'application/json')
        cookieJar.add_cookie_header(oRequest)
        try:
            oResponse = opener.open(oRequest)
        except HTTPError as e:
            oResponse = None
            if str(e.code) == '403' or str(e.code) == '503' or str(e.code) == '500':
                self._Status = str(e.code)
                data = e.fp.read()
                if 'DDOS-GUARD' in str(data):
                    opener = build_opener(HTTPCookieProcessor(cookieJar))
                    opener.addheaders = [('User-agent', self._USER_AGENT), ('Referer', self._sUrl)]
                    response = opener.open('https://check.ddos-guard.net/check.js')
                    content = response.read().decode('utf-8', 'replace').encode('utf-8', 'replace').decode('utf-8', 'replace')
                    url2 = re.findall("Image.*?'([^']+)'; new", content)
                    url3 = urlparse(self._sUrl)
                    url3 = '%s://%s/%s' % (url3.scheme, url3.netloc, url2[0])
                    opener = build_opener(HTTPCookieProcessor(cookieJar))
                    opener.addheaders = [('User-agent', self._USER_AGENT), ('Referer', self._sUrl)]
                    opener.open(url3).read()
                    opener = build_opener(HTTPCookieProcessor(cookieJar))
                    opener.addheaders = [('User-agent', self._USER_AGENT), ('Referer', self._sUrl)]
                    oResponse = opener.open(self._sUrl, sParameters if len(sParameters) > 0 else None)
                    if not oResponse:
                        print( ' -> [requestHandler]: Failed DDOS-GUARD active: ' + self._sUrl)
                        return ''
                elif 'cloudflare' in str(e.headers):
                    print( ' -> [requestHandler]: Failed Cloudflare active: ' + self._sUrl)
                    return 'CF-DDOS-GUARD aktiv'
                else:
                    if not self.ignoreErrors:
                        #xbmcgui.Dialog().ok('xStream', cConfig().getLocalizedString(30259) + ' {0} {1}'.format(self._sUrl, str(e)))
                        print( ' -> [requestHandler]: HTTPError ' + str(e) + ' Url: ' + self._sUrl)
                    return ''
            else:
                oResponse = e
        except URLError as e:
            #if not self.ignoreErrors:
                #xbmcgui.Dialog().ok('xStream', str(e.reason))
            print( ' -> [requestHandler]: URLError ' + str(e.reason) + ' Url: ' + self._sUrl)
            return ''
        except HTTPException as e:
            #if not self.ignoreErrors:
                #xbmcgui.Dialog().ok('xStream', str(e))
            print( ' -> [requestHandler]: HTTPException ' + str(e) + ' Url: ' + self._sUrl)
            return ''

        self._sResponseHeader = oResponse.info()
        if self._sResponseHeader.get('Content-Encoding') == 'gzip':
            sContent = gzip.GzipFile(fileobj=io.BytesIO(oResponse.read())).read()
            sContent = sContent.decode('utf-8', 'replace').encode('utf-8', 'replace').decode('utf-8', 'replace')
        else:
            sContent = oResponse.read().decode('utf-8', 'replace').encode('utf-8', 'replace').decode('utf-8', 'replace')
        if 'lazingfast' in sContent:
            bf = cBF().resolve(self._sUrl, sContent, cookieJar, self._USER_AGENT, sParameters)
            if bf:
                sContent = bf
            else:
                print( ' -> [requestHandler]: Failed Blazingfast active: ' + self._sUrl)
        try:
            cookieJar.save(ignore_discard=self.__bIgnoreDiscard, ignore_expires=self.__bIgnoreExpired)
        except Exception as e:
            print( ' -> [requestHandler]: Failed save cookie: %s' % e)
        if self.__bRemoveNewLines:
            sContent = sContent.replace('\n', '').replace('\r\t', '')
        if self.__bRemoveBreakLines:
            sContent = sContent.replace('&nbsp;', '')
        self._sRealUrl = oResponse.geturl()
        self._Status = oResponse.getcode() if self._sUrl == self._sRealUrl else '301'
        oResponse.close()
        if self.caching and self.cacheTime > 0:
            self.writeCache(self.getRequestUri(), sContent)
        return sContent

    def __setCookiePath(self):
        cookieFile = os.path.join(self._profilePath, 'data', 'cache', 'temp', 'cookies')
        if not os.path.exists(cookieFile):
            os.makedirs(cookieFile)
        if 'dummy' not in self._sUrl:
            cookieFile = os.path.join(cookieFile, urlparse(self._sUrl).netloc.replace('.', '_') + '.txt')
            if not os.path.exists(cookieFile):
                open(cookieFile, 'w').close()
            self._cookiePath = cookieFile

    def getCookie(self, sCookieName, sDomain=''):
        cookieJar = LWPCookieJar()
        try:
            cookieJar.load(self._cookiePath, self.__bIgnoreDiscard, self.__bIgnoreExpired)
        except Exception as e:
            print( e)
        for entry in cookieJar:
            if entry.name == sCookieName:
                if sDomain == '':
                    return entry
                elif entry.domain == sDomain:
                    return entry
        return False

    def setCookie(self, oCookie):
        cookieJar = LWPCookieJar()
        try:
            cookieJar.load(self._cookiePath, self.__bIgnoreDiscard, self.__bIgnoreExpired)
            cookieJar.set_cookie(oCookie)
            cookieJar.save(self._cookiePath, self.__bIgnoreDiscard, self.__bIgnoreExpired)
        except Exception as e:
            print( e)

    def ignoreDiscard(self, bIgnoreDiscard):
        self.__bIgnoreDiscard = bIgnoreDiscard

    def ignoreExpired(self, bIgnoreExpired):
        self.__bIgnoreExpired = bIgnoreExpired

    def setCachePath(self):
        cache = os.path.join(self._profilePath, 'data', 'cache', 'temp', 'htmlcache')
        if not os.path.exists(cache):
            os.makedirs(cache)
        self._cachePath = cache

    def readCache(self, url):
        content = ''
        h = hashlib.md5(url.encode('utf8')).hexdigest()
        cacheFile = os.path.join(self._cachePath, h)
        fileAge = self.getFileAge(cacheFile)
        if 0 < fileAge < self.cacheTime:
            try:
                with open(cacheFile, 'rb') as f:
                        content = f.read().decode('utf8')
            except Exception:
                print( ' -> [requestHandler]: Could not read Cache')
            if content:
                #Logger(1, ' -> [requestHandler]: read html for %s from cache' % url)
                return content
        return ''

    def writeCache(self, url, content):
        try:
            h = hashlib.md5(url.encode('utf8')).hexdigest()
            with open(os.path.join(self._cachePath, h), 'wb') as f:
                f.write(content.encode('utf8'))
        except Exception:
            print( ' -> [requestHandler]: Could not write Cache')

    @staticmethod
    def getFileAge(cacheFile):
        try:
            return time.time() - os.stat(cacheFile).st_mtime
        except Exception:
            return 0

    def clearCache(self):
        files = os.listdir(self._cachePath)
        for file in files:
            os.remove(os.path.join(self._cachePath, file))


class cBF:
    def resolve(self, url, html, cookie_jar, user_agent, sParameters):
        page = urlparse(url).scheme + '://' + urlparse(url).netloc
        j = re.findall('<script[^>]src="([^"]+)', html)
        if j:
            opener = build_opener(HTTPCookieProcessor(cookie_jar))
            opener.addheaders = [('User-agent', user_agent), ('Referer', url)]
            opener.open(page + j[0])
        a = re.findall('xhr\.open\("GET","([^,]+)",', html)
        if a:
            import random
            aespage = page + a[0].replace('" + ww +"', str(random.randint(700, 1500)))
            opener = build_opener(HTTPCookieProcessor(cookie_jar))
            opener.addheaders = [('User-agent', user_agent), ('Referer', url)]
            html = opener.open(aespage).read().decode('utf-8', 'replace').encode('utf-8', 'replace').decode('utf-8', 'replace')
            cval = self.aes_decode(html)
            cdata = re.findall('cookie="([^="]+).*?domain[^>]=([^;]+)', html)
            if cval and cdata:
                c = Cookie(version=0, name=cdata[0][0], value=cval, port=None, port_specified=False, domain=cdata[0][1], domain_specified=True, domain_initial_dot=False, path="/", path_specified=True, secure=False, expires=time.time() + 21600, discard=False, comment=None, comment_url=None, rest={})
                cookie_jar.set_cookie(c)
                opener = build_opener(HTTPCookieProcessor(cookie_jar))
                opener.addheaders = [('User-agent', user_agent), ('Referer', url)]
                return opener.open(url, sParameters if len(sParameters) > 0 else None).read().decode('utf-8', 'replace').encode('utf-8', 'replace').decode('utf-8', 'replace')

    def aes_decode(self, html):
        try:
            import pyaes
            keys = re.findall('toNumbers\("([^"]+)"', html)
            if keys:
                from binascii import hexlify, unhexlify
                msg = unhexlify(keys[2])
                key = unhexlify(keys[0])
                iv = unhexlify(keys[1])
                decrypter = pyaes.Decrypter(pyaes.AESModeOfOperationCBC(key, iv))
                plain_text = decrypter.feed(msg)
                plain_text += decrypter.feed()
                return hexlify(plain_text).decode()
        except Exception as e:
            print( e)


class RedirectFilter(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, hdrs, newurl):
        if 'notice.cuii' in newurl:
            return None
        return HTTPRedirectHandler.redirect_request(self, req, fp, code, msg, hdrs, newurl)
