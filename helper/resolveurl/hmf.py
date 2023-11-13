import re
import six
from six.moves import urllib_error, urllib_request, urllib_parse
import traceback
import resolveurl
from resolveurl import common

resolver_cache = {}


class HostedMediaFile:
    def __init__(self, url='', host='', media_id='', title='', include_disabled=False, include_universal=None, include_popups=None, return_all=False):
        if not url and not (host and media_id) or (url and (host or media_id)):
            raise ValueError('Set either url, or host AND media_id. No other combinations are valid.')
        self._url = 'http:%s' % url if url.startswith("//") else url
        self._host = host
        self._media_id = media_id
        self._valid_url = None
        self._return_all = return_all
        self.title = title if title else self._host

        if self._url:
            self._domain = self.__top_domain(self._url)
        else:
            self._domain = self.__top_domain(self._host)

        self.__resolvers = self.__get_resolvers(include_disabled, include_universal, include_popups)
        if not url:
            for resolver in self.__resolvers:  # Find a valid URL
                try:
                    if not resolver.isUniversal() and resolver.get_url(host, media_id):
                        self._url = resolver.get_url(host, media_id)
                        break
                except:
                    # Shity resolver. Ignore
                    continue

    def __get_resolvers(self, include_disabled, include_universal, include_popups):
        if include_universal is None:
            include_universal = common.get_setting('allow_universal') == "true"

        if include_popups is None:
            include_popups = common.get_setting('allow_popups') == "true"

        klasses = resolveurl.relevant_resolvers(self._domain, include_universal=include_universal,
                                                include_popups=include_popups, include_external=True,
                                                include_disabled=include_disabled, order_matters=True)
        resolvers = []
        for klass in klasses:
            if klass in resolver_cache:
                common.logger.log_debug('adding resolver from cache: %s' % klass)
                resolvers.append(resolver_cache[klass])
            else:
                common.logger.log_debug('adding resolver to cache: %s' % klass)
                resolver_cache[klass] = klass()
                resolvers.append(resolver_cache[klass])
        return resolvers

    def __top_domain(self, url):
        elements = urllib_parse.urlparse(url)
        domain = elements.netloc or elements.path
        domain = domain.split('@')[-1].split(':')[0]
        regex = r"(?:www\.)?([\w\-]*\.[\w\-]{2,5}(?:\.[\w\-]{2,5})?)$"
        res = re.search(regex, domain)
        if res:
            # domain = res.group(1)
            domain = '.'.join(res.group(1).split('.')[-2:])
        domain = domain.lower()
        return domain

    def get_url(self):
        return self._url

    def get_host(self):
        return self._host

    def get_media_id(self):
        return self._media_id

    def get_resolvers(self, validated=False):
        if validated:
            self.valid_url()
        return self.__resolvers

    def resolve(self, include_universal=True, allow_popups=True):
        for resolver in self.__resolvers:
            try:
                if (include_universal or not resolver.isUniversal()) and (allow_popups or not resolver.isPopup()):
                    if resolver.valid_url(self._url, self._host):
                        common.logger.log_debug('Resolving using %s plugin' % resolver.name)
                        resolver.login()
                        self._host, self._media_id = resolver.get_host_and_id(self._url)
                        if self._return_all and resolver.isUniversal():
                            url_list = resolver.get_media_url(self._host, self._media_id, return_all=self._return_all)
                            self.__resolvers = [resolver]
                            self._valid_url = True
                            return url_list
                        else:
                            stream_url = resolver.get_media_url(self._host, self._media_id)
                        if stream_url.startswith("//"):
                            stream_url = 'http:%s' % stream_url
                        if stream_url and self.__test_stream(stream_url):
                            self.__resolvers = [resolver]  # Found a working resolver, throw out the others
                            self._valid_url = True
                            return stream_url
            except Exception as e:
                url = self._url.encode('utf-8') if isinstance(self._url, six.text_type) and six.PY2 else self._url
                common.logger.log_error('%s Error - From: %s Link: %s: %s' % (type(e).__name__, resolver.name, url, e))
                if resolver == self.__resolvers[-1]:
                    common.logger.log_debug(traceback.format_exc())
                    raise

        self.__resolvers = []  # No resolvers.
        self._valid_url = False
        return False

    def valid_url(self):
        if self._valid_url is None:
            resolvers = []
            for resolver in self.__resolvers:
                try:
                    if resolver.valid_url(self._url, self._domain):
                        resolvers.append(resolver)
                except:
                    continue

            self.__resolvers = resolvers
            self._valid_url = True if resolvers else False
        return self._valid_url

    def __test_stream(self, stream_url):
        try:
            headers = dict([item.split('=') for item in (stream_url.split('|')[1]).split('&')])
        except:
            headers = {}
        for header in headers:
            headers[header] = urllib_parse.unquote_plus(headers[header])
        common.logger.log_debug('Setting Headers on UrlOpen: %s' % headers)

        try:
            import ssl
            ssl_context = ssl._create_unverified_context()
            ssl._create_default_https_context = ssl._create_unverified_context
            ssl_context.set_alpn_protocols(['http/1.1'])
            opener = urllib_request.build_opener(urllib_request.HTTPSHandler(context=ssl_context))
            urllib_request.install_opener(opener)
        except:
            pass

        try:
            msg = ''
            if 'verifypeer' in headers.keys():
                headers.pop('verifypeer')
            request = urllib_request.Request(stream_url.split('|')[0], headers=headers)
            # only do a HEAD request for non m3u8 streams
            if '.m3u8' not in stream_url:
                request.get_method = lambda: 'HEAD'
            #  set urlopen timeout to 15 seconds
            http_code = urllib_request.urlopen(request, timeout=15).getcode()
        except urllib_error.HTTPError as e:
            if isinstance(e, urllib_error.HTTPError):
                http_code = e.code
                if http_code == 405 or http_code == 472:
                    http_code = 200
            else:
                http_code = 600
        except urllib_error.URLError as e:
            http_code = 500
            if hasattr(e, 'reason'):
                # treat an unhandled url type as success
                if 'unknown url type' in str(e.reason).lower():
                    return True
                else:
                    msg = e.reason
            if not msg:
                msg = str(e)

        except Exception as e:
            http_code = 601
            msg = str(e)
            if msg == "''" or 'timed out' in msg:
                http_code = 504

        # added this log line for now so that we can catch any logs on streams that are rejected due to test_stream failures
        # we can remove it once we are sure this works reliably
        if int(http_code) >= 400 and int(http_code) != 504:
            common.logger.log_warning('Stream UrlOpen Failed: Url: %s HTTP Code: %s Msg: %s' % (stream_url, http_code, msg))

        return int(http_code) < 400 or int(http_code) == 504

    def __bool__(self):
        return self.__nonzero__()

    def __nonzero__(self):
        if self._valid_url is None:
            return self.valid_url()
        else:
            return self._valid_url

    def __str__(self):
        return "{url: |%s| host: |%s| media_id: |%s|}" % (self._url, self._host, self._media_id)

    def __repr__(self):
        return self.__str__()
