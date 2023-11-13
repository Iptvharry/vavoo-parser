import time, os, sys, signal, multiprocessing, inquirer, asyncio, uvicorn
from concurrent.futures import ProcessPoolExecutor
from typing import Union
from typing_extensions import Annotated

from uvicorn import Server, Config
from fastapi import FastAPI, HTTPException, Request, Response, Body, Form
from fastapi.responses import JSONResponse, StreamingResponse, RedirectResponse, FileResponse
from pydantic import BaseModel
from multiprocessing import Process, Queue

import utils.common as common
from utils.common import Logger as Logger
import utils.xstream as xstream
import utils.vavoo as vavoo
import utils.video as video
import utils.user as user

import resolveurl as resolver
from helper import sites
import cli, services

cachepath = common.cp
listpath = common.lp
con = common.con

common.check()

class UvicornServer(multiprocessing.Process):
    def __init__(self, config: Config):
        super().__init__()

        self.config = config

    def stop(self):
        self.terminate()

    def run(self, *args, **kwargs):
        server = Server(config=self.config)
        server.run()


app = FastAPI()
links = {}
linked = {}


def handleServices():
    #global p3, p4
    #time.sleep(2)
    #if bool(int(cfg.get('Main', 'm3u8_service'))) == True:
        #if not p3:
            #p3 = Process(target=services.loop_m3u8)
            #p3.start()
            #Logger('[LOOP][M3U8::] Successful started...')
        #else: Logger('[LOOP][M3U8::] not started, because service allready running ...')
    #else: Logger('[LOOP][M3U8::] not started, because service are disabled ...')
    #if bool(int(cfg.get('Main', 'epg_service'))) == True:
        #if not p4:
            #p4 = Process(target=services.loop_epg)
            #p4.start()
            #Logger('[LOOP][EPG::] Successful started...')
        #else: Logger('[LOOP][EPG::] not started, because service allready running ...')
    #else: Logger('[LOOP][EPG::] not started, because service are disabled ...')
    return


@app.on_event("startup")
async def on_startup():
    app.state.executor = ProcessPoolExecutor()
    app.state.loop = asyncio.get_event_loop()
    app.state.loop.run_in_executor(app.state.executor, handleServices)


@app.on_event("shutdown")
async def on_shutdown():
    app.state.executor.shutdown()


# API XTREAM-CODES
############################################################################################################
@app.get("/get.php")
async def get_get(username: Union[str, None] = None, password: Union[str, None] = None, type: Union[str, None] = None, output: Union[str, None] = None):
    return
    if username is None: username = "nobody"
    if password is None: password = "pass"
    typ = "m3u8"
    if type is not None:
        if type == "m3u": typ = "m3u"
    out = "mp4"
    if output is not None:
        if output == "ts" or output == "mpegts": out = "ts"
    of = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cache/streams.%s' % typ)
    if not os.path.exists(of):
        video.get_m3u8(username, password, out, typ)
    return FileResponse(of)


@app.post("/get.php")
async def get_post(username: Annotated[str, Form()] = None, password: Annotated[str, Form()] = None, type: Annotated[str, Form()] = None, output: Annotated[str, Form()] = None):
    return
    if username is None: username = "nobody"
    if password is None: password = "pass"
    typ = "m3u8"
    if type is not None:
        if type == "m3u": typ = "m3u"
    out = "mp4"
    if output is not None:
        if output == "ts" or output == "mpegts": out = "ts"
    of = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cache/streams.%s' % typ)
    if not os.path.exists(of):
        get = video.get_m3u8(username, password, out, typ)
        if get == True:
            return FileResponse(of)
    return FileResponse(of)


@app.get("/player_api.php")
async def player_get(username: Union[str, None] = None, password: Union[str, None] = None, action: Union[str, None] = None, vod_id: Union[str, None] = None, series_id: Union[str, None] = None, stream_id: Union[str, None] = None, limit: Union[str, None] = None, category_id: Union[str, None] = None, params: Union[str, None] = None):
    if username is None: username = "nobody"
    if password is None: password = "pass"
    
    user_data = user.auth(username, password)
    if action is None:
        return {
            "user_info": user.user_info_xtream(user_data, username, password),
            "server_info": common.server_info(),
        }
    if action is not None:
        if action == "get_live_categories":
            return video.get_live_categories()
        elif action == "get_live_streams":
            return video.get_live_streams(category_id)
        elif action == "get_vod_categories":
            return video.get_vod_categories()
        elif action == "get_vod_streams":
            return video.get_vod_streams(category_id)
        elif action == "get_vod_info":
            return video.get_vod_info(vod_id)
        elif action == "get_series_categories":
            return video.get_series_categories()
        elif action == "get_series_info":
            return video.get_series_info(series_id)
        elif action == "get_series":
            return video.get_series(category_id)
        elif action == "get_simple_data_table":
            return #video.get_simple_data_table(stream_id)
        elif action == "get_short_epg":
            return #video.get_short_epg(stream_id, limit)


@app.post("/player_api.php")
async def player_post(username: Annotated[str, Form()] = None, password: Annotated[str, Form()] = None, action: Annotated[str, Form()] = None, vod_id: Annotated[str, Form()] = None, series_id: Annotated[str, Form()] = None, stream_id: Annotated[str, Form()] = None, limit: Annotated[str, Form()] = None, category_id: Annotated[str, Form()] = None, params: Annotated[str, Form()] = None):
    if username is None: username = "nobody"
    if password is None: password = "pass"

    user_data = user.auth(username, password)
    if action is None:
        return {
            "user_info": user.user_info_xtream(user_data, username, password),
            "server_info": common.server_info(),
        }
    if action is not None:
        if action == "get_live_categories":
            return video.get_live_categories()
        elif action == "get_live_streams":
            return video.get_live_streams(category_id)
        elif action == "get_vod_categories":
            return video.get_vod_categories()
        elif action == "get_vod_streams":
            return video.get_vod_streams(category_id)
        elif action == "get_vod_info":
            return video.get_vod_info(vod_id)
        elif action == "get_series_categories":
            return video.get_series_categories()
        elif action == "get_series_info":
            return video.get_series_info(series_id)
        elif action == "get_series":
            return video.get_series(category_id)
        elif action == "get_simple_data_table":
            return #video.get_simple_data_table(stream_id)
        elif action == "get_short_epg":
            return #video.get_short_epg(stream_id, limit)


@app.get("/panel_api.php")
async def panel_get(username: Union[str, None] = None, password: Union[str, None] = None, action: Union[str, None] = None):
    if username is None: username = "nobody"
    if password is None: password = "pass"

    user_data = user.auth(username, password)
    return {
        "user_info": user.user_info_xtream(user_data, username, password),
        "server_info": common.server_info(),
        "categories": { "live": video.get_live_categories(), "movie": video.get_vod_categories(), "series": video.get_series_categories() },
        "available_channels": video.get_all_channels(),
    }


@app.post("/panel_api.php")
async def panel_post(username: Annotated[str, Form()] = None, password: Annotated[str, Form()] = None, action: Annotated[str, Form()] = None):
    if username is None: username = "nobody"
    if password is None: password = "pass"

    user_data = user.auth(username, password)
    return {
        "user_info": user.user_info_xtream(user_data, username, password),
        "server_info": common.server_info(),
        "categories": { "live": video.get_live_categories(), "movie": video.get_vod_categories(), "series": video.get_series_categories() },
        "available_channels": video.get_all_channels(),
    }


@app.get("/live/{username}/{password}/{sid}.{ext}", response_class=RedirectResponse, status_code=302)
async def live(username: str, password: str, sid: str, ext: str):
    if username is None: username = "nobody"
    if password is None: password = "pass"

    user_data = user.auth(username, password)
    cur = con.cursor()
    cur.execute('SELECT * FROM channel WHERE id="' + sid + '"')
    data = cur.fetchone()
    sig = vavoo.getAuthSignature()
    if data and sig:
        url = str(data['url'])
        link = url + '?n=1&b=5&vavoo_auth=' + sig
        return link
    else: raise HTTPException(status_code=404, detail="Stream not found")


@app.get("/{typ}/{username}/{password}/{sid}.{ext}", response_class=RedirectResponse, status_code=302)
async def vod(typ: str, username: str, password: str, sid: str, ext: str):
    if username is None: username = "nobody"
    if password is None: password = "pass"

    user_data = user.auth(username, password)
    cur = con.cursor()
    cur.execute('SELECT * FROM streams WHERE id="' + sid + '"')
    data = cur.fetchone()
    if not data:
        raise HTTPException(status_code=404, detail="No Data")
    if sid not in links:
        urls = xstream.getHoster(data)
        if urls:
            links[sid] = urls
            if sid not in linked: linked[sid] = {}
            if username not in linked[sid]: linked[sid][username] = 0
    if sid in links:
        if len(links[sid]) > linked[sid][username]:
            url = links[sid][linked[sid][username]]
            if not "streamUrl" in url:
                try:
                    shost = xstream.getHosterUrl(url["link"], data['site'])
                    if shost:
                        url["streamUrl"] = shost[0]["streamUrl"]
                except Exception:
                    link = None
            if "streamUrl" in url:
                try:
                    link = xstream.getStream(url["streamUrl"])
                except Exception:
                    link = None
            linked[sid][username] += 1
            if link is None: 
                Logger(1, "Link (%s/%s) not found" %(str(linked[sid][username]), str(len(links[sid]))))
                raise HTTPException(status_code=404, detail="Link (%s/%s) not found" %(str(linked[sid][username]), str(len(links[sid]))))
            return link
        elif len(links[sid]) > 1:
            linked[sid][username] = 0
            return
    else: raise HTTPException(status_code=404, detail="Stream not found")


@app.get("/xmltv.php")
async def epg(username: str, password: str):
    if username is None: username = "nobody"
    if password is None: password = "pass"

    user_data = user.auth(username, password)
    f = os.path.join(cachepath, 'xmltv.xml')
    if os.path.exists(f):
        file = open(f, "rb")
        headers = {'Content-Disposition': 'attachment; filename="xmltv.xml"', 'Connection': 'close'}
        return StreamingResponse(file, headers=headers, media_type="application/xml; charset=utf-8")
    else:
        raise HTTPException(status_code=404, detail="File not found")


# VAVOO API
############################################################################################################
@app.get("/")
async def root(response: Response):
    data = ''
    listdir = os.listdir(listpath)
    for l in listdir:
        data += '<a href="'+l+'">'+l+'</a><br>'
    return Response(content=data, media_type="text/html")


@app.get("/{m3u8}.m3u8", response_class=RedirectResponse, status_code=302)
async def m3u8(m3u8: str):
    f = os.path.join(listpath, m3u8+'.m3u8')
    if os.path.exists(f):
        file = open(f, "rb")
        return StreamingResponse(file)
    else: 
        raise HTTPException(status_code=404, detail="File not found")


@app.get("/epg.xml.gz", response_class=RedirectResponse, status_code=302)
async def gz():
    f = os.path.join(listpath, 'epg.xml.gz')
    if os.path.exists(f):
        file = open(f, "rb")
        return StreamingResponse(file)
    else: 
        raise HTTPException(status_code=404, detail="File not found")


@app.get("/channel/{sid}", response_class=RedirectResponse, status_code=302)
async def channel(sid: str):
    cur = con.cursor()
    cur.execute('SELECT * FROM channel WHERE id="' + sid + '"')
    data = cur.fetchone()
    sig = vavoo.getAuthSignature()
    if data and sig:
        url = str(data['url'])
        link = url + '?n=1&b=5&vavoo_auth=' + sig
        return link
    else: raise HTTPException(status_code=404, detail="Stream not found")


@app.get("/stream/{sid}", response_class=RedirectResponse, status_code=302)
async def stream(sid: str):
    cur = con.cursor()
    cur.execute('SELECT * FROM streams WHERE id="' + sid + '"')
    data = cur.fetchone()
    if not data:
        raise HTTPException(status_code=404, detail="No Data")
    if sid not in links:
        urls = xstream.getHoster(data)
        if urls:
            links[sid] = urls
            if sid not in linked: linked[sid] = 0
    if sid in links:
        if len(links[sid]) > linked[sid]:
            url = links[sid][linked[sid]]
            if not "streamUrl" in url:
                try:
                    shost = xstream.getHosterUrl(url["link"], data['site'])
                    if shost:
                        url["streamUrl"] = shost[0]["streamUrl"]
                except Exception:
                    link = None
            if "streamUrl" in url:
                try:
                    link = xstream.getStream(url["streamUrl"])
                except Exception:
                    link = None
            linked[sid] += 1
            if link is None: 
                Logger(1, "Link (%s/%s) not found" %(str(linked[sid]), str(len(links[sid]))))
                raise HTTPException(status_code=404, detail="Link (%s/%s) not found" %(str(linked[sid]), str(len(links[sid]))))
            return link
        elif len(links[sid]) > 1:
            linked[sid] = 0
            return
    else: raise HTTPException(status_code=404, detail="Stream not found")

