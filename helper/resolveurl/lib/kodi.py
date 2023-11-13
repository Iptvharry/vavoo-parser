"""
    ResolveURL Addon for Kodi
    Copyright (C) 2016 t0mm0, tknorris

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
from six.moves import urllib_parse
import six
import sys
import os
import re
import time
from resolveurl.lib import strings
from resolveurl.lib import CustomProgressDialog

py_ver = sys.version
py_info = sys.version_info


def get_path():
    return '/home/masta/bin/lib/python3/resolveurl/'


def get_profile():
    return '/home/masta/bin/lib/python3/resolveurl/userdata/'


def translate_path(path):
    return


def get_setting(sid):
    if sid in setting:
        return setting[sid]
    return
    


def set_setting(id, value):
    if not isinstance(value, six.string_types):
        value = str(value)
    addon.setSetting(id, value)


def get_version():
    return "5.1.106"


def get_id():
    return "script.module.resolveurl"


def get_name():
    return "ResolveURL"


def kodi_version():

    return float(18)


def supported_video_extensions():
    supported_video_extensions = ['.mp4', '.ts', '.mkv', '.m3u8']
    unsupported = ['.url', '.zip', '.rar', '.001', '.7z', '.tar.gz', '.tar.bz2',
                   '.tar.xz', '.tgz', '.tbz2', '.gz', '.bz2', '.xz', '.tar', '']
    return [i for i in supported_video_extensions if i not in unsupported]


def open_settings():
    return 


def get_keyboard_legacy(heading, default='', hide_input=False):
    return

    keyboard = xbmc.Keyboard(hidden=hide_input)
    keyboard.setHeading(heading)

    if default:
        keyboard.setDefault(default)

    keyboard.doModal()

    if keyboard.isConfirmed():
        return keyboard.getText()
    else:
        return None


def get_keyboard_new(heading, default='', hide_input=False):
    return

    """
    This function has been in support since XBMC Gotham v13
    """

    if hide_input is False:
        hide_input = 0
    elif hide_input is True:
        hide_input = xbmcgui.ALPHANUM_HIDE_INPUT

    dialog = xbmcgui.Dialog()

    keyboard = dialog.input(heading, defaultt=default, type=0, option=hide_input)

    if keyboard:

        return keyboard

    return None


#if kodi_version() >= 13.0:

    #get_keyboard = get_keyboard_new

#else:

    #get_keyboard = get_keyboard_legacy


def i18n(string_id):
    return
    try:
        return six.ensure_str(addon.getLocalizedString(strings.STRINGS[string_id]))
    except Exception as e:
        _log('Failed String Lookup: %s (%s)' % (string_id, e))
        return string_id


def get_plugin_url(queries):
    try:
        query = urllib_parse.urlencode(queries)
    except UnicodeEncodeError:
        for k in queries:
            if isinstance(queries[k], six.text_type) and six.PY2:
                queries[k] = queries[k].encode('utf-8')
        query = urllib_parse.urlencode(queries)

    return sys.argv[0] + '?' + query


def end_of_directory(cache_to_disc=True):
    pass
    xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=cache_to_disc)


def set_content(content):
    pass
    xbmcplugin.setContent(int(sys.argv[1]), content)


def create_item(queries, label, thumb='', fanart='', is_folder=None, is_playable=None, total_items=0, menu_items=None, replace_menu=False):
    list_item = xbmcgui.ListItem(label, iconImage=thumb, thumbnailImage=thumb)
    add_item(queries, list_item, fanart, is_folder, is_playable, total_items, menu_items, replace_menu)


def add_item(queries, list_item, fanart='', is_folder=None, is_playable=None, total_items=0, menu_items=None, replace_menu=False):
    return
    if menu_items is None:
        menu_items = []
    if is_folder is None:
        is_folder = False if is_playable else True

    if is_playable is None:
        playable = 'false' if is_folder else 'true'
    else:
        playable = 'true' if is_playable else 'false'

    liz_url = get_plugin_url(queries)
    if fanart:
        list_item.setProperty('fanart_image', fanart)
    list_item.setInfo('video', {'title': list_item.getLabel()})
    list_item.setProperty('isPlayable', playable)
    list_item.addContextMenuItems(menu_items, replaceItems=replace_menu)
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), liz_url, list_item, isFolder=is_folder, totalItems=total_items)


def parse_query(query):
    q = {'mode': 'main'}
    if query.startswith('?'):
        query = query[1:]
    queries = urllib_parse.parse_qs(query)
    for key in queries:
        if len(queries[key]) == 1:
            q[key] = queries[key][0]
        else:
            q[key] = queries[key]
    return q


def notify(header=None, msg='', duration=2000, sound=None):
    if header is None:
        header = get_name()
    if sound is None:
        sound = get_setting('mute_notifications') == 'false'
    icon_path = os.path.join(get_path(), 'icon.png')
    try:
        xbmcgui.Dialog().notification(header, msg, icon_path, duration, sound)
    except:
        builtin = "XBMC.Notification(%s,%s, %s, %s)" % (header, msg, duration, icon_path)
        xbmc.executebuiltin(builtin)


def close_all():
    xbmc.executebuiltin('Dialog.Close(all)')


def get_current_view():
    return
    #skinPath = translate_path('special://skin/')
    #xml = os.path.join(skinPath, 'addon.xml')
    #f = xbmcvfs.File(xml)
    #read = f.read()
    #f.close()
    #try:
        #src = re.search('defaultresolution="([^"]+)', read, re.DOTALL).group(1)
    #except:
        #src = re.search('<res.+?folder="([^"]+)', read, re.DOTALL).group(1)
    #src = os.path.join(skinPath, src, 'MyVideoNav.xml')
    #f = xbmcvfs.File(src)
    #read = f.read()
    #f.close()
    #match = re.search('<views>([^<]+)', read, re.DOTALL)
    #if match:
        #views = match.group(1)
        #for view in views.split(','):
            #if xbmc.getInfoLabel('Control.GetLabel(%s)' % view):
                #return view


def yesnoDialog(heading=get_name(), line1='', line2='', line3='', nolabel='', yeslabel=''):
    return #xbmcgui.Dialog().yesno(heading, line1 + '[CR]' + line2 + '[CR]' + line3, nolabel=nolabel, yeslabel=yeslabel)


class WorkingDialog(object):
    def __init__(self):
        return
        xbmc.executebuiltin('ActivateWindow(busydialog)')

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        return
        xbmc.executebuiltin('Dialog.Close(busydialog)')


def has_addon(addon_id):
    return #xbmc.getCondVisibility('System.HasAddon(%s)' % addon_id) == 1


class ProgressDialog(object):
    pass
    def __init__(self, heading, line1='', line2='', line3='', background=False, active=True, timer=0):
        self.line1 = line1
        self.line2 = line2
        self.line3 = line3
        self.begin = time.time()
        self.timer = timer
        self.background = background
        self.heading = heading
        if active and not timer:
            self.pd = self.__create_dialog(line1, line2, line3)
            self.pd.update(0)
        else:
            self.pd = None

    def __create_dialog(self, line1, line2, line3):
        if self.background:
            pd = xbmcgui.DialogProgressBG()
            msg = line1 + line2 + line3
            pd.create(self.heading, msg)
        else:
            if xbmc.getCondVisibility('Window.IsVisible(progressdialog)'):
                pd = CustomProgressDialog.ProgressDialog()
            else:
                pd = xbmcgui.DialogProgress()
            if six.PY2:
                pd.create(self.heading, line1, line2, line3)
            else:
                pd.create(self.heading,
                          line1 + '\n'
                          + line2 + '\n'
                          + line3)
        return pd

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if self.pd is not None:
            self.pd.close()
            del self.pd

    def is_canceled(self):
        if self.pd is not None and not self.background:
            return self.pd.iscanceled()
        else:
            return False

    def update(self, percent, line1='', line2='', line3=''):
        if not line1:
            line1 = self.line1
        if not line2:
            line2 = self.line2
        if not line3:
            line3 = self.line3
        if self.pd is None and self.timer and (time.time() - self.begin) >= self.timer:
            self.pd = self.__create_dialog(line1, line2, line3)

        if self.pd is not None:
            if self.background:
                msg = line1 + line2 + line3
                self.pd.update(percent, self.heading, msg)
            else:
                if six.PY2:
                    self.pd.update(percent, line1, line2, line3)
                else:
                    self.pd.update(percent,
                                   line1 + '\n'
                                   + line2 + '\n'
                                   + line3)


class CountdownDialog(object):
    pass
    __INTERVALS = 5

    def __init__(self, heading, line1='', line2='', line3='', active=True, countdown=60, interval=5):
        self.heading = heading
        self.countdown = countdown
        self.interval = interval
        self.line1 = line1
        self.line2 = line2
        self.line3 = line3
        if active:
            if xbmc.getCondVisibility('Window.IsVisible(progressdialog)'):
                pd = CustomProgressDialog.ProgressDialog()
            else:
                pd = xbmcgui.DialogProgress()
            if not self.line3:
                line3 = 'Expires in: %s seconds' % countdown
            if six.PY2:
                pd.create(self.heading, line1, line2, line3)
            else:
                pd.create(self.heading,
                          line1 + '\n'
                          + line2 + '\n'
                          + line3)
            pd.update(100)
            self.pd = pd
        else:
            self.pd = None

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if self.pd is not None:
            self.pd.close()
            del self.pd

    def start(self, func, args=None, kwargs=None):
        if args is None:
            args = []
        if kwargs is None:
            kwargs = {}
        result = func(*args, **kwargs)
        if result:
            return result

        if self.pd is not None:
            start = time.time()
            expires = time_left = self.countdown
            interval = self.interval
            while time_left > 0:
                for _ in range(CountdownDialog.__INTERVALS):
                    sleep(int(interval * 1000 / CountdownDialog.__INTERVALS))
                    if self.is_canceled():
                        return
                    time_left = expires - int(time.time() - start)
                    if time_left < 0:
                        time_left = 0
                    progress = int(time_left * 100 / expires)
                    line3 = 'Expires in: %s seconds' % time_left if not self.line3 else ''
                    self.update(progress, line3=line3)

                result = func(*args, **kwargs)
                if result:
                    return result

    def is_canceled(self):
        if self.pd is None:
            return False
        else:
            return self.pd.iscanceled()

    def update(self, percent, line1='', line2='', line3=''):
        if not line1:
            line1 = self.line1
        if not line2:
            line2 = self.line2
        if not line3:
            line3 = self.line3
        if self.pd is not None:
            if six.PY2:
                self.pd.update(percent, line1, line2, line3)
            else:
                self.pd.update(percent,
                               line1 + '\n'
                               + line2 + '\n'
                               + line3)


def fill_settings():
    setting = {}
    setting["allow_universal"] = 'true'
    setting["allow_popups"] = 'true'
    setting["auto_pick"] = 'true'
    setting["use_cache"] = 'true'
    setting["reset_cache"] = 'true'
    setting["personal_nid"] = 'true'
    setting["last_ua_create"] = 0
    setting["current_ua"] = 'true'
    setting["addon_debug"] = 'false'
    setting["clean_settings"] = 'true'
    setting["AllDebridResolver_priority"] = 100
    setting["AllDebridResolver_enabled"] = 'true'
    setting["AllDebridResolver_login"] = 'true'
    setting["AllDebridResolver_torrents"] = 'true'
    setting["AllDebridResolver_cached_only"] = 'false'
    setting["AllDebridResolver_auth"] = 'true'
    setting["AllDebridResolver_reset"] = 'true'
    setting["AllDebridResolver_token"] = 'true'
    setting["BoxbitResolver_priority"] = 100
    setting["BoxbitResolver_enabled"] = 'true'
    setting["BoxbitResolver_login"] = 'false'
    setting["BoxbitResolver_email"] = 'true'
    setting["BoxbitResolver_password"] = 'true'
    setting["BoxbitResolver_token"] = 'true'
    setting["BoxbitResolver_uuid"] = 'true'
    setting["BoxbitResolver_time_expired"] = 'true'
    setting["DebridLinkResolver_priority"] = 100
    setting["DebridLinkResolver_enabled"] = 'true'
    setting["DebridLinkResolver_login"] = 'true'
    setting["DebridLinkResolver_torrents"] = 'true'
    setting["DebridLinkResolver_cached_only"] = 'false'
    setting["DebridLinkResolver_auth"] = 'true'
    setting["DebridLinkResolver_reset"] = 'true'
    setting["DebridLinkResolver_token"] = 'true'
    setting["DebridLinkResolver_refresh"] = 'true'
    setting["DebridLinkResolver_client_id"] = 'true'
    setting["LinkSnappyResolver_priority"] = 100
    setting["LinkSnappyResolver_enabled"] = 'true'
    setting["LinkSnappyResolver_login"] = 'true'
    setting["LinkSnappyResolver_username"] = 'true'
    setting["LinkSnappyResolver_password"] = 'true'
    setting["LinkSnappyResolver_auth"] = 'true'
    setting["LinkSnappyResolver_reset"] = 'true'
    setting["LinkSnappyResolver_cached_files_only"] = 'false'
    setting["LinkSnappyResolver_torrents"] = 'true'
    setting["LinkSnappyResolver_cached_only"] = 'true'
    setting["LinkSnappyResolver_expiration_timestamp"] = 'true'
    setting["MegaDebridResolver_priority"] = 100
    setting["MegaDebridResolver_enabled"] = 'true'
    setting["MegaDebridResolver_use_https"] = 'true'
    setting["MegaDebridResolver_login"] = 'false'
    setting["MegaDebridResolver_username"] = 'true'
    setting["MegaDebridResolver_password"] = 'true'
    setting["PremiumizeMeResolver_priority"] = 100
    setting["PremiumizeMeResolver_enabled"] = 'true'
    setting["PremiumizeMeResolver_login"] = 'true'
    setting["PremiumizeMeResolver_torrents"] = 'true'
    setting["PremiumizeMeResolver_cached_only"] = 'false'
    setting["PremiumizeMeResolver_clear_finished"] = 'false'
    setting["PremiumizeMeResolver_auth"] = 'true'
    setting["PremiumizeMeResolver_reset"] = 'true'
    setting["PremiumizeMeResolver_token"] = 'true'
    setting["RealDebridResolver_priority"] = 100
    setting["RealDebridResolver_enabled"] = 'true'
    setting["RealDebridResolver_login"] = 'true'
    setting["RealDebridResolver_torrents"] = 'true'
    setting["RealDebridResolver_cached_only"] = 'false'
    setting["RealDebridResolver_autopick"] = 'false'
    setting["RealDebridResolver_auth"] = 'true'
    setting["RealDebridResolver_reset"] = 'true'
    setting["RealDebridResolver_token"] = 'true'
    setting["RealDebridResolver_refresh"] = 'true'
    setting["RealDebridResolver_client_id"] = 'true'
    setting["RealDebridResolver_client_secret"] = 'true'
    setting["RPnetResolver_priority"] = 100
    setting["RPnetResolver_enabled"] = 'true'
    setting["RPnetResolver_login"] = 'false'
    setting["RPnetResolver_username"] = 'true'
    setting["RPnetResolver_password"] = 'true'
    setting["SimplyDebridResolver_priority"] = 100
    setting["SimplyDebridResolver_enabled"] = 'true'
    setting["SimplyDebridResolver_login"] = 'false'
    setting["SimplyDebridResolver_username"] = 'true'
    setting["SimplyDebridResolver_password"] = 'true'
    setting["SmoozedResolver_priority"] = 100
    setting["SmoozedResolver_enabled"] = 'true'
    setting["SmoozedResolver_login"] = 'false'
    setting["SmoozedResolver_username"] = 'true'
    setting["SmoozedResolver_password"] = 'true'
    setting["SmoozedResolver_session_key"] = 'true'
    setting["AdultSwimResolver_priority"] = 100
    setting["AdultSwimResolver_enabled"] = 'true'
    setting["AdultSwimResolver_login"] = 'true'
    setting["AliezResolver_priority"] = 100
    setting["AliezResolver_enabled"] = 'true'
    setting["AliezResolver_login"] = 'true'
    setting["AllViidResolver_priority"] = 100
    setting["AllViidResolver_enabled"] = 'true'
    setting["AllViidResolver_login"] = 'true'
    setting["AmazonCloudResolver_priority"] = 100
    setting["AmazonCloudResolver_enabled"] = 'true'
    setting["AmazonCloudResolver_login"] = 'true'
    setting["AnafastResolver_priority"] = 100
    setting["AnafastResolver_enabled"] = 'true'
    setting["AnafastResolver_login"] = 'true'
    setting["AniStreamResolver_priority"] = 100
    setting["AniStreamResolver_enabled"] = 'true'
    setting["AniStreamResolver_login"] = 'true'
    setting["AnonFilesResolver_priority"] = 100
    setting["AnonFilesResolver_enabled"] = 'true'
    setting["AnonFilesResolver_login"] = 'true'
    setting["AnonymFileResolver_priority"] = 100
    setting["AnonymFileResolver_enabled"] = 'true'
    setting["AnonymFileResolver_login"] = 'true'
    setting["AparatResolver_priority"] = 100
    setting["AparatResolver_enabled"] = 'true'
    setting["AparatResolver_login"] = 'true'
    setting["ArchiveResolver_priority"] = 100
    setting["ArchiveResolver_enabled"] = 'true'
    setting["ArchiveResolver_login"] = 'true'
    setting["AVideoResolver_priority"] = 100
    setting["AVideoResolver_enabled"] = 'true'
    setting["AVideoResolver_login"] = 'true'
    setting["BannedVideoResolver_priority"] = 100
    setting["BannedVideoResolver_enabled"] = 'true'
    setting["BannedVideoResolver_login"] = 'true'
    setting["BitchuteResolver_priority"] = 100
    setting["BitchuteResolver_enabled"] = 'true'
    setting["BitchuteResolver_login"] = 'true'
    setting["BrighteonResolver_priority"] = 100
    setting["BrighteonResolver_enabled"] = 'true'
    setting["BrighteonResolver_login"] = 'true'
    setting["BRUploadResolver_priority"] = 100
    setting["BRUploadResolver_enabled"] = 'true'
    setting["BRUploadResolver_login"] = 'true'
    setting["CastampResolver_priority"] = 100
    setting["CastampResolver_enabled"] = 'true'
    setting["CastampResolver_login"] = 'true'
    setting["CdaResolver_priority"] = 100
    setting["CdaResolver_enabled"] = 'true'
    setting["CdaResolver_login"] = 'true'
    setting["ChillXResolver_priority"] = 100
    setting["ChillXResolver_enabled"] = 'true'
    setting["ChillXResolver_login"] = 'true'
    setting["ChromecastResolver_priority"] = 100
    setting["ChromecastResolver_enabled"] = 'true'
    setting["ChromecastResolver_login"] = 'true'
    setting["ClickNUploadResolver_priority"] = 100
    setting["ClickNUploadResolver_enabled"] = 'true'
    setting["ClickNUploadResolver_login"] = 'true'
    setting["ClipWatchingResolver_priority"] = 100
    setting["ClipWatchingResolver_enabled"] = 'true'
    setting["ClipWatchingResolver_login"] = 'true'
    setting["CloudbResolver_priority"] = 100
    setting["CloudbResolver_enabled"] = 'true'
    setting["CloudbResolver_login"] = 'true'
    setting["CloudMailRuResolver_priority"] = 100
    setting["CloudMailRuResolver_enabled"] = 'true'
    setting["CloudMailRuResolver_login"] = 'true'
    setting["CloudVideoResolver_priority"] = 100
    setting["CloudVideoResolver_enabled"] = 'true'
    setting["CloudVideoResolver_login"] = 'true'
    setting["CosTVResolver_priority"] = 100
    setting["CosTVResolver_enabled"] = 'true'
    setting["CosTVResolver_login"] = 'true'
    setting["DailymotionResolver_priority"] = 100
    setting["DailymotionResolver_enabled"] = 'true'
    setting["DailymotionResolver_login"] = 'true'
    setting["DaxabResolver_priority"] = 100
    setting["DaxabResolver_enabled"] = 'true'
    setting["DaxabResolver_login"] = 'true'
    setting["DembedResolver_priority"] = 100
    setting["DembedResolver_enabled"] = 'true'
    setting["DembedResolver_login"] = 'true'
    setting["DesiuploadResolver_priority"] = 100
    setting["DesiuploadResolver_enabled"] = 'true'
    setting["DesiuploadResolver_login"] = 'true'
    setting["DoodStreamResolver_priority"] = 100
    setting["DoodStreamResolver_enabled"] = 'true'
    setting["DoodStreamResolver_login"] = 'true'
    setting["DownAceResolver_priority"] = 100
    setting["DownAceResolver_enabled"] = 'true'
    setting["DownAceResolver_login"] = 'true'
    setting["DrkVidResolver_priority"] = 100
    setting["DrkVidResolver_enabled"] = 'true'
    setting["DrkVidResolver_login"] = 'true'
    setting["DropResolver_priority"] = 100
    setting["DropResolver_enabled"] = 'true'
    setting["DropResolver_login"] = 'true'
    setting["DropLoadResolver_priority"] = 100
    setting["DropLoadResolver_enabled"] = 'true'
    setting["DropLoadResolver_login"] = 'true'
    setting["DubokuResolver_priority"] = 100
    setting["DubokuResolver_enabled"] = 'true'
    setting["DubokuResolver_login"] = 'true'
    setting["EmbedGramResolver_priority"] = 100
    setting["EmbedGramResolver_enabled"] = 'true'
    setting["EmbedGramResolver_login"] = 'true'
    setting["EmbedRiseResolver_priority"] = 100
    setting["EmbedRiseResolver_enabled"] = 'true'
    setting["EmbedRiseResolver_login"] = 'true'
    setting["EnterVideoResolver_priority"] = 100
    setting["EnterVideoResolver_enabled"] = 'true'
    setting["EnterVideoResolver_login"] = 'true'
    setting["FacebookResolver_priority"] = 100
    setting["FacebookResolver_enabled"] = 'true'
    setting["FacebookResolver_login"] = 'true'
    setting["FacebookResolver_quality"] = 0
    setting["FastDriveResolver_priority"] = 100
    setting["FastDriveResolver_enabled"] = 'true'
    setting["FastDriveResolver_login"] = 'true'
    setting["FastPlayResolver_priority"] = 100
    setting["FastPlayResolver_enabled"] = 'true'
    setting["FastPlayResolver_login"] = 'true'
    setting["FastUploadResolver_priority"] = 100
    setting["FastUploadResolver_enabled"] = 'true'
    setting["FastUploadResolver_login"] = 'true'
    setting["FEmbedResolver_priority"] = 100
    setting["FEmbedResolver_enabled"] = 'true'
    setting["FEmbedResolver_login"] = 'true'
    setting["FileLionsResolver_priority"] = 100
    setting["FileLionsResolver_enabled"] = 'true'
    setting["FileLionsResolver_login"] = 'true'
    setting["FileMoonResolver_priority"] = 100
    setting["FileMoonResolver_enabled"] = 'true'
    setting["FileMoonResolver_login"] = 'true'
    setting["FilePupResolver_priority"] = 100
    setting["FilePupResolver_enabled"] = 'true'
    setting["FilePupResolver_login"] = 'true'
    setting["FilerIoResolver_priority"] = 100
    setting["FilerIoResolver_enabled"] = 'true'
    setting["FilerIoResolver_login"] = 'true'
    setting["FilesFMResolver_priority"] = 100
    setting["FilesFMResolver_enabled"] = 'true'
    setting["FilesFMResolver_login"] = 'true'
    setting["FilesIMResolver_priority"] = 100
    setting["FilesIMResolver_enabled"] = 'true'
    setting["FilesIMResolver_login"] = 'true'
    setting["Film77Resolver_priority"] = 100
    setting["Film77Resolver_enabled"] = 'true'
    setting["Film77Resolver_login"] = 'true'
    setting["FlashXResolver_priority"] = 100
    setting["FlashXResolver_enabled"] = 'true'
    setting["FlashXResolver_login"] = 'true'
    setting["Full30Resolver_priority"] = 100
    setting["Full30Resolver_enabled"] = 'true'
    setting["Full30Resolver_login"] = 'true'
    setting["GamoVideoResolver_priority"] = 100
    setting["GamoVideoResolver_enabled"] = 'true'
    setting["GamoVideoResolver_login"] = 'true'
    setting["ResolveGeneric_priority"] = 100
    setting["ResolveGeneric_enabled"] = 'true'
    setting["ResolveGeneric_login"] = 'true'
    setting["GoFileResolver_priority"] = 100
    setting["GoFileResolver_enabled"] = 'true'
    setting["GoFileResolver_login"] = 'true'
    setting["GoloadResolver_priority"] = 100
    setting["GoloadResolver_enabled"] = 'true'
    setting["GoloadResolver_login"] = 'true'
    setting["GomoPlayerResolver_priority"] = 100
    setting["GomoPlayerResolver_enabled"] = 'true'
    setting["GomoPlayerResolver_login"] = 'true'
    setting["GoodStreamResolver_priority"] = 100
    setting["GoodStreamResolver_enabled"] = 'true'
    setting["GoodStreamResolver_login"] = 'true'
    setting["GoogleResolver_priority"] = 100
    setting["GoogleResolver_enabled"] = 'true'
    setting["GoogleResolver_login"] = 'true'
    setting["GoogleResolver_use_gdrive"] = 'false'
    setting["GooStreamResolver_priority"] = 100
    setting["GooStreamResolver_enabled"] = 'true'
    setting["GooStreamResolver_login"] = 'true'
    setting["GoStreamResolver_priority"] = 100
    setting["GoStreamResolver_enabled"] = 'true'
    setting["GoStreamResolver_login"] = 'true'
    setting["GoVadResolver_priority"] = 100
    setting["GoVadResolver_enabled"] = 'true'
    setting["GoVadResolver_login"] = 'true'
    setting["HDvidResolver_priority"] = 100
    setting["HDvidResolver_enabled"] = 'true'
    setting["HDvidResolver_login"] = 'true'
    setting["HexUploadResolver_priority"] = 100
    setting["HexUploadResolver_enabled"] = 'true'
    setting["HexUploadResolver_login"] = 'true'
    setting["HolaVidResolver_priority"] = 100
    setting["HolaVidResolver_enabled"] = 'true'
    setting["HolaVidResolver_login"] = 'true'
    setting["HurryStreamResolver_priority"] = 100
    setting["HurryStreamResolver_enabled"] = 'true'
    setting["HurryStreamResolver_login"] = 'true'
    setting["HXFileResolver_priority"] = 100
    setting["HXFileResolver_enabled"] = 'true'
    setting["HXFileResolver_login"] = 'true'
    setting["IndaVideoResolver_priority"] = 100
    setting["IndaVideoResolver_enabled"] = 'true'
    setting["IndaVideoResolver_login"] = 'true'
    setting["ItemFixResolver_priority"] = 100
    setting["ItemFixResolver_enabled"] = 'true'
    setting["ItemFixResolver_login"] = 'true'
    setting["JustOKResolver_priority"] = 100
    setting["JustOKResolver_enabled"] = 'true'
    setting["JustOKResolver_login"] = 'true'
    setting["K2SResolver_priority"] = 100
    setting["K2SResolver_enabled"] = 'true'
    setting["K2SResolver_login"] = 'true'
    setting["KrakenFilesResolver_priority"] = 100
    setting["KrakenFilesResolver_enabled"] = 'true'
    setting["KrakenFilesResolver_login"] = 'true'
    setting["KwikResolver_priority"] = 100
    setting["KwikResolver_enabled"] = 'true'
    setting["KwikResolver_login"] = 'true'
    setting["LatestViewResolver_priority"] = 100
    setting["LatestViewResolver_enabled"] = 'true'
    setting["LatestViewResolver_login"] = 'true'
    setting["LbryResolver_priority"] = 100
    setting["LbryResolver_enabled"] = 'true'
    setting["LbryResolver_login"] = 'true'
    setting["LetsUploadResolver_priority"] = 100
    setting["LetsUploadResolver_enabled"] = 'true'
    setting["LetsUploadResolver_login"] = 'true'
    setting["LewdHostResolver_priority"] = 100
    setting["LewdHostResolver_enabled"] = 'true'
    setting["LewdHostResolver_login"] = 'true'
    setting["LiiVideoResolver_priority"] = 100
    setting["LiiVideoResolver_enabled"] = 'true'
    setting["LiiVideoResolver_login"] = 'true'
    setting["LinkBoxResolver_priority"] = 100
    setting["LinkBoxResolver_enabled"] = 'true'
    setting["LinkBoxResolver_login"] = 'true'
    setting["LuluStreamResolver_priority"] = 100
    setting["LuluStreamResolver_enabled"] = 'true'
    setting["LuluStreamResolver_login"] = 'true'
    setting["MailRuResolver_priority"] = 100
    setting["MailRuResolver_enabled"] = 'true'
    setting["MailRuResolver_login"] = 'true'
    setting["MegaUpNetResolver_priority"] = 100
    setting["MegaUpNetResolver_enabled"] = 'true'
    setting["MegaUpNetResolver_login"] = 'true'
    setting["MeGoGoResolver_priority"] = 100
    setting["MeGoGoResolver_enabled"] = 'true'
    setting["MeGoGoResolver_login"] = 'true'
    setting["MightyUploadResolver_priority"] = 100
    setting["MightyUploadResolver_enabled"] = 'true'
    setting["MightyUploadResolver_login"] = 'true'
    setting["MixDropResolver_priority"] = 100
    setting["MixDropResolver_enabled"] = 'true'
    setting["MixDropResolver_login"] = 'true'
    setting["MP4UploadResolver_priority"] = 100
    setting["MP4UploadResolver_enabled"] = 'true'
    setting["MP4UploadResolver_login"] = 'true'
    setting["MVidooResolver_priority"] = 100
    setting["MVidooResolver_enabled"] = 'true'
    setting["MVidooResolver_login"] = 'true'
    setting["MyCloudResolver_priority"] = 100
    setting["MyCloudResolver_enabled"] = 'true'
    setting["MyCloudResolver_login"] = 'true'
    setting["MyFeministResolver_priority"] = 100
    setting["MyFeministResolver_enabled"] = 'true'
    setting["MyFeministResolver_login"] = 'true'
    setting["MyUpload_priority"] = 100
    setting["MyUpload_enabled"] = 'true'
    setting["MyUpload_login"] = 'true'
    setting["NeoHDResolver_priority"] = 100
    setting["NeoHDResolver_enabled"] = 'true'
    setting["NeoHDResolver_login"] = 'true'
    setting["NewTubeResolver_priority"] = 100
    setting["NewTubeResolver_enabled"] = 'true'
    setting["NewTubeResolver_login"] = 'true'
    setting["OKResolver_priority"] = 100
    setting["OKResolver_enabled"] = 'true'
    setting["OKResolver_login"] = 'true'
    setting["OneUploadResolver_priority"] = 100
    setting["OneUploadResolver_enabled"] = 'true'
    setting["OneUploadResolver_login"] = 'true'
    setting["PandaFilesResolver_priority"] = 100
    setting["PandaFilesResolver_enabled"] = 'true'
    setting["PandaFilesResolver_login"] = 'true'
    setting["PeerTubeResolver_priority"] = 100
    setting["PeerTubeResolver_enabled"] = 'true'
    setting["PeerTubeResolver_login"] = 'true'
    setting["PixelDrainResolver_priority"] = 100
    setting["PixelDrainResolver_enabled"] = 'true'
    setting["PixelDrainResolver_login"] = 'true'
    setting["PKSpeedResolver_priority"] = 100
    setting["PKSpeedResolver_enabled"] = 'true'
    setting["PKSpeedResolver_login"] = 'true'
    setting["PlayHDResolver_priority"] = 100
    setting["PlayHDResolver_enabled"] = 'true'
    setting["PlayHDResolver_login"] = 'true'
    setting["PlayWireResolver_priority"] = 100
    setting["PlayWireResolver_enabled"] = 'true'
    setting["PlayWireResolver_login"] = 'true'
    setting["RacatyResolver_priority"] = 100
    setting["RacatyResolver_enabled"] = 'true'
    setting["RacatyResolver_login"] = 'true'
    setting["RapidgatorResolver_priority"] = 100
    setting["RapidgatorResolver_enabled"] = 'true'
    setting["RapidgatorResolver_login"] = 'false'
    setting["RapidgatorResolver_username"] = 'true'
    setting["RapidgatorResolver_password"] = 'true'
    setting["RapidgatorResolver_premium"] = 'false'
    setting["RapidgatorResolver_session_id"] = 'true'
    setting["ReviewRateResolver_priority"] = 100
    setting["ReviewRateResolver_enabled"] = 'true'
    setting["ReviewRateResolver_login"] = 'true'
    setting["ReviewTechResolver_priority"] = 100
    setting["ReviewTechResolver_enabled"] = 'true'
    setting["ReviewTechResolver_login"] = 'true'
    setting["RoVideoResolver_priority"] = 100
    setting["RoVideoResolver_enabled"] = 'true'
    setting["RoVideoResolver_login"] = 'true'
    setting["RumbleResolver_priority"] = 100
    setting["RumbleResolver_enabled"] = 'true'
    setting["RumbleResolver_login"] = 'true'
    setting["RuTubeResolver_priority"] = 100
    setting["RuTubeResolver_enabled"] = 'true'
    setting["RuTubeResolver_login"] = 'true'
    setting["SapoResolver_priority"] = 100
    setting["SapoResolver_enabled"] = 'true'
    setting["SapoResolver_login"] = 'true'
    setting["SaruchResolver_priority"] = 100
    setting["SaruchResolver_enabled"] = 'true'
    setting["SaruchResolver_login"] = 'true'
    setting["SecVideoResolver_priority"] = 100
    setting["SecVideoResolver_enabled"] = 'true'
    setting["SecVideoResolver_login"] = 'true'
    setting["SendResolver_priority"] = 100
    setting["SendResolver_enabled"] = 'true'
    setting["SendResolver_login"] = 'true'
    setting["SendVidResolver_priority"] = 100
    setting["SendVidResolver_enabled"] = 'true'
    setting["SendVidResolver_login"] = 'true'
    setting["SibnetResolver_priority"] = 100
    setting["SibnetResolver_enabled"] = 'true'
    setting["SibnetResolver_login"] = 'true'
    setting["SolidFilesResolver_priority"] = 100
    setting["SolidFilesResolver_enabled"] = 'true'
    setting["SolidFilesResolver_login"] = 'true'
    setting["SpeedoStreamResolver_priority"] = 100
    setting["SpeedoStreamResolver_enabled"] = 'true'
    setting["SpeedoStreamResolver_login"] = 'true'
    setting["Streama2zResolver_priority"] = 100
    setting["Streama2zResolver_enabled"] = 'true'
    setting["Streama2zResolver_login"] = 'true'
    setting["StreamableResolver_priority"] = 100
    setting["StreamableResolver_enabled"] = 'true'
    setting["StreamableResolver_login"] = 'true'
    setting["StreamCommunityResolver_priority"] = 100
    setting["StreamCommunityResolver_enabled"] = 'true'
    setting["StreamCommunityResolver_login"] = 'true'
    setting["StreamEmbedResolver_priority"] = 100
    setting["StreamEmbedResolver_enabled"] = 'true'
    setting["StreamEmbedResolver_login"] = 'true'
    setting["StreamHideResolver_priority"] = 100
    setting["StreamHideResolver_enabled"] = 'true'
    setting["StreamHideResolver_login"] = 'true'
    setting["StreamHubResolver_priority"] = 100
    setting["StreamHubResolver_enabled"] = 'true'
    setting["StreamHubResolver_login"] = 'true'
    setting["StreamLareResolver_priority"] = 100
    setting["StreamLareResolver_enabled"] = 'true'
    setting["StreamLareResolver_login"] = 'true'
    setting["StreamoUploadResolver_priority"] = 100
    setting["StreamoUploadResolver_enabled"] = 'true'
    setting["StreamoUploadResolver_login"] = 'true'
    setting["StreamRapidResolver_priority"] = 100
    setting["StreamRapidResolver_enabled"] = 'true'
    setting["StreamRapidResolver_login"] = 'true'
    setting["StreamRubyResolver_priority"] = 100
    setting["StreamRubyResolver_enabled"] = 'true'
    setting["StreamRubyResolver_login"] = 'true'
    setting["StreamSBResolver_priority"] = 100
    setting["StreamSBResolver_enabled"] = 'true'
    setting["StreamSBResolver_login"] = 'true'
    setting["StreamTapeResolver_priority"] = 100
    setting["StreamTapeResolver_enabled"] = 'true'
    setting["StreamTapeResolver_login"] = 'true'
    setting["StreamVidResolver_priority"] = 100
    setting["StreamVidResolver_enabled"] = 'true'
    setting["StreamVidResolver_login"] = 'true'
    setting["StreamVidsResolver_priority"] = 100
    setting["StreamVidsResolver_enabled"] = 'true'
    setting["StreamVidsResolver_login"] = 'true'
    setting["StreamWishResolver_priority"] = 100
    setting["StreamWishResolver_enabled"] = 'true'
    setting["StreamWishResolver_login"] = 'true'
    setting["StreamZResolver_priority"] = 100
    setting["StreamZResolver_enabled"] = 'true'
    setting["StreamZResolver_login"] = 'true'
    setting["SuperEmbedsResolver_priority"] = 100
    setting["SuperEmbedsResolver_enabled"] = 'true'
    setting["SuperEmbedsResolver_login"] = 'true'
    setting["SuperITUResolver_priority"] = 100
    setting["SuperITUResolver_enabled"] = 'true'
    setting["SuperITUResolver_login"] = 'true'
    setting["SuperVideoResolver_priority"] = 100
    setting["SuperVideoResolver_enabled"] = 'true'
    setting["SuperVideoResolver_login"] = 'true'
    setting["TruHDResolver_priority"] = 100
    setting["TruHDResolver_enabled"] = 'true'
    setting["TruHDResolver_login"] = 'true'
    setting["TubeLoadResolver_priority"] = 100
    setting["TubeLoadResolver_enabled"] = 'true'
    setting["TubeLoadResolver_login"] = 'true'
    setting["TubiTvResolver_priority"] = 100
    setting["TubiTvResolver_enabled"] = 'true'
    setting["TubiTvResolver_login"] = 'true'
    setting["TudouResolver_priority"] = 100
    setting["TudouResolver_enabled"] = 'true'
    setting["TudouResolver_login"] = 'true'
    setting["TurboVIPlayResolver_priority"] = 100
    setting["TurboVIPlayResolver_enabled"] = 'true'
    setting["TurboVIPlayResolver_login"] = 'true'
    setting["TusFilesResolver_priority"] = 100
    setting["TusFilesResolver_enabled"] = 'true'
    setting["TusFilesResolver_login"] = 'true'
    setting["TVLogyResolver_priority"] = 100
    setting["TVLogyResolver_enabled"] = 'true'
    setting["TVLogyResolver_login"] = 'true'
    setting["TwitchResolver_priority"] = 100
    setting["TwitchResolver_enabled"] = 'true'
    setting["TwitchResolver_login"] = 'true'
    setting["TwitchResolver_client_id"] = "am6l6dn0x3bxrdgc557p1qeg1ma3bto"
    setting["UpBaamResolver_priority"] = 100
    setting["UpBaamResolver_enabled"] = 'true'
    setting["UpBaamResolver_login"] = 'true'
    setting["UploadBazResolver_priority"] = 100
    setting["UploadBazResolver_enabled"] = 'true'
    setting["UploadBazResolver_login"] = 'true'
    setting["UploadDoResolver_priority"] = 100
    setting["UploadDoResolver_enabled"] = 'true'
    setting["UploadDoResolver_login"] = 'true'
    setting["UploadEverResolver_priority"] = 100
    setting["UploadEverResolver_enabled"] = 'true'
    setting["UploadEverResolver_login"] = 'true'
    setting["UploadFlixResolver_priority"] = 100
    setting["UploadFlixResolver_enabled"] = 'true'
    setting["UploadFlixResolver_login"] = 'true'
    setting["UploadingSiteResolver_priority"] = 100
    setting["UploadingSiteResolver_enabled"] = 'true'
    setting["UploadingSiteResolver_login"] = 'true'
    setting["UploadRajaResolver_priority"] = 100
    setting["UploadRajaResolver_enabled"] = 'true'
    setting["UploadRajaResolver_login"] = 'true'
    setting["UppitResolver_priority"] = 100
    setting["UppitResolver_enabled"] = 'true'
    setting["UppitResolver_login"] = 'true'
    setting["UpStreamResolver_priority"] = 100
    setting["UpStreamResolver_enabled"] = 'true'
    setting["UpStreamResolver_login"] = 'true'
    setting["UpToBoxResolver_priority"] = 100
    setting["UpToBoxResolver_enabled"] = 'true'
    setting["UpToBoxResolver_login"] = 'true'
    setting["UpToBoxResolver_premium"] = 'false'
    setting["UpToBoxResolver_auth"] = 'true'
    setting["UpToBoxResolver_reset"] = 'true'
    setting["UpToBoxResolver_token"] = 'true'
    setting["UpVidResolver_priority"] = 100
    setting["UpVidResolver_enabled"] = 'true'
    setting["UpVidResolver_login"] = 'true'
    setting["UpVideoResolver_priority"] = 100
    setting["UpVideoResolver_enabled"] = 'true'
    setting["UpVideoResolver_login"] = 'true'
    setting["UQLoadResolver_priority"] = 100
    setting["UQLoadResolver_enabled"] = 'true'
    setting["UQLoadResolver_login"] = 'true'
    setting["UserLoadResolver_priority"] = 100
    setting["UserLoadResolver_enabled"] = 'true'
    setting["UserLoadResolver_login"] = 'true'
    setting["UsersCloudResolver_priority"] = 100
    setting["UsersCloudResolver_enabled"] = 'true'
    setting["UsersCloudResolver_login"] = 'true'
    setting["VeeHDResolver_priority"] = 100
    setting["VeeHDResolver_enabled"] = 'true'
    setting["VeeHDResolver_login"] = 'false'
    setting["VeeHDResolver_username"] = 'true'
    setting["VeeHDResolver_password"] = 'true'
    setting["VemBXResolver_priority"] = 100
    setting["VemBXResolver_enabled"] = 'true'
    setting["VemBXResolver_login"] = 'true'
    setting["VeohResolver_priority"] = 100
    setting["VeohResolver_enabled"] = 'true'
    setting["VeohResolver_login"] = 'true'
    setting["VidBobResolver_priority"] = 100
    setting["VidBobResolver_enabled"] = 'true'
    setting["VidBobResolver_login"] = 'true'
    setting["VidBomResolver_priority"] = 100
    setting["VidBomResolver_enabled"] = 'true'
    setting["VidBomResolver_login"] = 'true'
    setting["VidCloudResolver_priority"] = 100
    setting["VidCloudResolver_enabled"] = 'true'
    setting["VidCloudResolver_login"] = 'true'
    setting["VidCloud9Resolver_priority"] = 100
    setting["VidCloud9Resolver_enabled"] = 'true'
    setting["VidCloud9Resolver_login"] = 'true'
    setting["VideaResolver_priority"] = 100
    setting["VideaResolver_enabled"] = 'true'
    setting["VideaResolver_login"] = 'true'
    setting["VidelloResolver_priority"] = 100
    setting["VidelloResolver_enabled"] = 'true'
    setting["VidelloResolver_login"] = 'true'
    setting["VideoApneResolver_priority"] = 100
    setting["VideoApneResolver_enabled"] = 'true'
    setting["VideoApneResolver_login"] = 'true'
    setting["VideoBinResolver_priority"] = 100
    setting["VideoBinResolver_enabled"] = 'true'
    setting["VideoBinResolver_login"] = 'true'
    setting["VideoooResolver_priority"] = 100
    setting["VideoooResolver_enabled"] = 'true'
    setting["VideoooResolver_login"] = 'true'
    setting["VideoSeyredResolver_priority"] = 100
    setting["VideoSeyredResolver_enabled"] = 'true'
    setting["VideoSeyredResolver_login"] = 'true'
    setting["VideoWoodResolver_priority"] = 100
    setting["VideoWoodResolver_enabled"] = 'true'
    setting["VideoWoodResolver_login"] = 'true'
    setting["VideoZooResolver_priority"] = 100
    setting["VideoZooResolver_enabled"] = 'true'
    setting["VideoZooResolver_login"] = 'true'
    setting["VidFastResolver_priority"] = 100
    setting["VidFastResolver_enabled"] = 'true'
    setting["VidFastResolver_login"] = 'true'
    setting["VidGuardResolver_priority"] = 100
    setting["VidGuardResolver_enabled"] = 'true'
    setting["VidGuardResolver_login"] = 'true'
    setting["VidHDResolver_priority"] = 100
    setting["VidHDResolver_enabled"] = 'true'
    setting["VidHDResolver_login"] = 'true'
    setting["VidLookResolver_priority"] = 100
    setting["VidLookResolver_enabled"] = 'true'
    setting["VidLookResolver_login"] = 'true'
    setting["VidMojoResolver_priority"] = 100
    setting["VidMojoResolver_enabled"] = 'true'
    setting["VidMojoResolver_login"] = 'true'
    setting["VidMolyResolver_priority"] = 100
    setting["VidMolyResolver_enabled"] = 'true'
    setting["VidMolyResolver_login"] = 'true'
    setting["VidMXResolver_priority"] = 100
    setting["VidMXResolver_enabled"] = 'true'
    setting["VidMXResolver_login"] = 'true'
    setting["VidoResolver_priority"] = 100
    setting["VidoResolver_enabled"] = 'true'
    setting["VidoResolver_login"] = 'true'
    setting["VidOrgResolver_priority"] = 100
    setting["VidOrgResolver_enabled"] = 'true'
    setting["VidOrgResolver_login"] = 'true'
    setting["VidozaResolver_priority"] = 100
    setting["VidozaResolver_enabled"] = 'true'
    setting["VidozaResolver_login"] = 'true'
    setting["VidProResolver_priority"] = 100
    setting["VidProResolver_enabled"] = 'true'
    setting["VidProResolver_login"] = 'true'
    setting["VidSpeedResolver_priority"] = 100
    setting["VidSpeedResolver_enabled"] = 'true'
    setting["VidSpeedResolver_login"] = 'true'
    setting["VidStoreResolver_priority"] = 100
    setting["VidStoreResolver_enabled"] = 'true'
    setting["VidStoreResolver_login"] = 'true'
    setting["VidzStoreResolver_priority"] = 100
    setting["VidzStoreResolver_enabled"] = 'true'
    setting["VidzStoreResolver_login"] = 'true'
    setting["VimeoResolver_priority"] = 100
    setting["VimeoResolver_enabled"] = 'true'
    setting["VimeoResolver_login"] = 'true'
    setting["VipSSResolver_priority"] = 100
    setting["VipSSResolver_enabled"] = 'true'
    setting["VipSSResolver_login"] = 'true'
    setting["VKResolver_priority"] = 100
    setting["VKResolver_enabled"] = 'true'
    setting["VKResolver_login"] = 'true'
    setting["VKPrimeResolver_priority"] = 100
    setting["VKPrimeResolver_enabled"] = 'true'
    setting["VKPrimeResolver_login"] = 'true'
    setting["VKSpeedResolver_priority"] = 100
    setting["VKSpeedResolver_enabled"] = 'true'
    setting["VKSpeedResolver_login"] = 'true'
    setting["VlalaComResolver_priority"] = 100
    setting["VlalaComResolver_enabled"] = 'true'
    setting["VlalaComResolver_login"] = 'true'
    setting["VlalaNetResolver_priority"] = 100
    setting["VlalaNetResolver_enabled"] = 'true'
    setting["VlalaNetResolver_login"] = 'true'
    setting["VoeResolver_priority"] = 100
    setting["VoeResolver_enabled"] = 'true'
    setting["VoeResolver_login"] = 'true'
    setting["VoxzerResolver_priority"] = 100
    setting["VoxzerResolver_enabled"] = 'true'
    setting["VoxzerResolver_login"] = 'true'
    setting["VShareResolver_priority"] = 100
    setting["VShareResolver_enabled"] = 'true'
    setting["VShareResolver_login"] = 'true'
    setting["VTubeResolver_priority"] = 100
    setting["VTubeResolver_enabled"] = 'true'
    setting["VTubeResolver_login"] = 'true'
    setting["VudeoResolver_priority"] = 100
    setting["VudeoResolver_enabled"] = 'true'
    setting["VudeoResolver_login"] = 'true'
    setting["YandexResolver_priority"] = 100
    setting["YandexResolver_enabled"] = 'true'
    setting["YandexResolver_login"] = 'true'
    setting["YouDBoxResolver_priority"] = 100
    setting["YouDBoxResolver_enabled"] = 'true'
    setting["YouDBoxResolver_login"] = 'true'
    setting["YourUploadResolver_priority"] = 100
    setting["YourUploadResolver_enabled"] = 'true'
    setting["YourUploadResolver_login"] = 'true'
    setting["YouTubeResolver_priority"] = 100
    setting["YouTubeResolver_enabled"] = 'true'
    setting["YouTubeResolver_login"] = 'true'
    setting["ZPlayerResolver_priority"] = 100
    setting["ZPlayerResolver_enabled"] = 'true'
    setting["ZPlayerResolver_login"] = 'true'
    setting["ZtreamHubResolver_priority"] = 100
    setting["ZtreamHubResolver_enabled"] = 'true'
    setting["ZtreamHubResolver_login"] = 'true'
    return setting
setting = fill_settings()

