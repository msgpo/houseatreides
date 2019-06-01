# -*- coding: utf-8 -*-
#######################################################################
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
#  As long as you retain this notice you can do whatever you want with this
# stuff. Just please ask before copying. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return. - Muad'Dib
# ----------------------------------------------------------------------------
#######################################################################

# Addon Name: Atreides
# Addon id: plugin.video.atreides
# Addon Provider: House Atreides

import base64
import hashlib
import re
import traceback
import urllib
import urlparse

import resolveurl

from resources.lib.modules import client, directstream, log_utils, pyaes, trakt


def is_anime(content, type, type_id):
    try:
        r = trakt.getGenre(content, type, type_id)
        return 'anime' in r or 'animation' in r
    except Exception:
        return False


def get_release_quality(release_name, release_link=None):

    if release_name is None:
        return

    try:
        release_name = release_name.encode('utf-8')
    except Exception:
        pass

    try:
        quality = None

        fmt = re.sub('[^A-Za-z0-9]+', ' ', release_name)
        fmt = str(fmt.lower())
        try:
            fmt = fmt.encode('utf-8')
        except Exception:
            pass

        if ' 2160p ' in fmt:
            quality = '4K'
        elif ' 2160 ' in fmt:
            quality = '4K'
        elif ' uhd ' in fmt:
            quality = '4K'
        elif ' 4k ' in fmt:
            quality = '4K'
        elif ' 1080p ' in fmt:
            quality = '1080p'
        elif ' 1080 ' in fmt:
            quality = '1080p'
        elif ' fullhd ' in fmt:
            quality = '1080p'
        elif ' 720p ' in fmt:
            quality = '720p'
        elif ' hd ' in fmt:
            quality = '720p'
        elif ' 480p ' in fmt:
            quality = 'SD'
        elif ' 480 ' in fmt:
            quality = 'SD'
        elif ' 576p ' in fmt:
            quality = 'SD'
        elif ' 576 ' in fmt:
            quality = 'SD'
        elif any(i in [' dvdscr ', ' r5 ', ' r6 '] for i in fmt):
            quality = 'SCR'
        elif any(i in [' camrip ', ' tsrip ', ' hdcam ', ' hdts ', ' dvdcam ', ' dvdts ', ' cam ', ' telesync ', ' ts '] for i in fmt):
            quality = 'CAM'

        if not quality:
            if release_link:
                release_link = client.replaceHTMLCodes(release_link)
                release_link = re.sub('[^A-Za-z0-9 ]+', ' ', release_link)
                release_link = str(release_link.lower())

                try:
                    release_link = release_link.encode('utf-8')
                except Exception:
                    pass
                if ' 4k ' in release_link:
                    quality = '4k'
                elif ' 2160 ' in release_link:
                    quality = '4k'
                elif ' 2160p ' in release_link:
                    quality = '4k'
                elif ' uhd ' in release_link:
                    quality = '4k'
                elif ' 1080 ' in release_link:
                    quality = '1080p'
                elif ' 1080p ' in release_link:
                    quality = '1080p'
                elif ' fullhd ' in release_link:
                    quality = '1080p'
                elif ' 720p ' in release_link:
                    quality = '720p'
                elif ' hd ' in release_link:
                    quality = '720p'
                else:
                    if any(i in [' dvdscr ', ' r5 ', ' r6 '] for i in release_link):
                        quality = 'SCR'
                    elif any(i in [' camrip ', ' tsrip ', ' hdcam ', ' hdts ', ' dvdcam ', ' dvdts ', ' cam ', ' telesync ', ' ts '] for i in release_link):
                        quality = 'CAM'
                    else:
                        quality = 'SD'
            else:
                quality = 'SD'
        info = []
        if '3d' in fmt or '.3D.' in release_name:
            info.append('3D')
        if any(i in ['hevc', 'h265', 'x265'] for i in fmt):
            info.append('HEVC')

        return quality, info
    except Exception:
        return 'SD', []


def getFileType(url):

    try:
        url = client.replaceHTMLCodes(url)
        url = re.sub('[^A-Za-z0-9]+', ' ', url)
        url = url.encode('utf-8')
        url = str(url.lower())
    except Exception:
        url = str(url)
    type = ''

    if any(i in url for i in [' bluray ', ' blu ray ']):
        type += ' BLURAY /'
    if any(i in url for i in [' bd r ', ' bdr ', ' bd rip ', ' bdrip ', ' br rip ', ' brrip ']):
        type += ' BD-RIP /'
    if ' remux ' in url:
        type += ' REMUX /'
    if any(i in url for i in [' dvdrip ', ' dvd rip ']):
        type += ' DVD-RIP /'
    if any(i in url for i in [' dvd ', ' dvdr ', ' dvd r ']):
        type += ' DVD /'
    if any(i in url for i in [' webdl ', ' web dl ', ' web ', ' web rip ', ' webrip ']):
        type += ' WEB /'
    if ' hdtv ' in url:
        type += ' HDTV /'
    if ' sdtv ' in url:
        type += ' SDTV /'
    if any(i in url for i in [' hdrip ', ' hd rip ']):
        type += ' HDRIP /'
    if any(i in url for i in [' uhdrip ', ' uhd rip ']):
        type += ' UHDRIP /'
    if ' r5 ' in url:
        type += ' R5 /'
    if any(i in url for i in [' cam ', ' cam rip ', ' camrip ']):
        type += ' CAM /'
    if any(i in url for i in [' ts ', ' telesync ', ' hdts ', ' pdvd ']):
        type += ' TS /'
    if any(i in url for i in [' tc ', ' telecine ', ' hdtc ']):
        type += ' TC /'
    if any(i in url for i in [' scr ', ' screener ', ' dvdscr ', ' dvd scr ']):
        type += ' SCR /'
    if ' xvid ' in url:
        type += ' XVID /'
    if ' avi ' in url:
        type += ' AVI /'
    if any(i in url for i in [' h 264 ', ' h264 ', ' x264 ', ' avc ']):
        type += ' H.264 /'
    if any(i in url for i in [' h 265 ', ' h256 ', ' x265 ', ' hevc ']):
        type += ' HEVC /'
    if ' hi10p ' in url:
        type += ' HI10P /'
    if ' 10bit ' in url:
        type += ' 10BIT /'
    if ' 3d ' in url:
        type += ' 3D /'
    if ' hdr ' in url:
        type += ' HDR /'
    if ' imax ' in url:
        type += ' IMAX /'
    if ' ac3 ' in url:
        type += ' AC3 /'
    if ' eac3 ' in url:
        type += ' EAC3 /'
    if ' aac ' in url:
        type += ' AAC /'
    if any(i in url for i in [' dd ', ' dolby ', ' dolbydigital ', ' dolby digital ']):
        type += ' DD /'
    if any(i in url for i in [' truehd ', ' true hd ']):
        type += ' TRUEHD /'
    if ' atmos ' in url:
        type += ' ATMOS /'
    if any(i in url for i in [' ddplus ', ' dd plus ', ' ddp ']):
        type += ' DD+ /'
    if ' dts ' in url:
        type += ' DTS /'
    if any(i in url for i in [' hdma ', ' hd ma ']):
        type += ' HD.MA /'
    if any(i in url for i in [' hdhra ', ' hd hra ']):
        type += ' HD.HRA /'
    if any(i in url for i in [' dtsx ', ' dts x ']):
        type += ' DTS:X /'
    if ' dd5 1 ' in url:
        type += ' DD / 5.1 /'
    if any(i in url for i in [' 5 1 ', ' 6ch ']):
        type += ' 5.1 /'
    if any(i in url for i in [' 7 1 ', ' 8ch ']):
        type += ' 7.1 /'
    if 'subs' in url:
        if type != '':
            type += ' - WITH SUBS'
        else:
            type = 'SUBS'
    type = type.rstrip('/')
    return type


def check_sd_url(release_link):
    try:
        release_link = re.sub('[^A-Za-z0-9]+', ' ', release_link)
        release_link = str(release_link.lower())
        try:
            release_link = release_link.encode('utf-8')
        except Exception:
            pass
        if ' 2160 ' in release_link:
            quality = '4K'
        elif ' 2160p ' in release_link:
            quality = '4K'
        elif ' 4k ' in release_link:
            quality = '4K'
        elif ' uhd ' in release_link:
            quality = '4K'
        elif ' 1080 ' in release_link:
            quality = '1080p'
        elif ' 1080p ' in release_link:
            quality = '1080p'
        elif ' fullhd ' in release_link:
            quality = '1080p'
        elif ' 720p ' in release_link:
            quality = '720p'
        elif ' hd ' in release_link:
            quality = '720p'
        elif any(i in [' dvdscr ', ' r5 ', ' r6 '] for i in release_link):
            quality = 'SCR'
        elif any(i in [' camrip ', ' tsrip ', ' hdcam ', ' hdts ', ' dvdcam ', ' dvdts ', ' cam ', ' telesync ', ' ts '] for i in release_link):
            quality = 'CAM'
        else:
            quality = 'SD'
        return quality
    except Exception:
        return 'SD'


def label_to_quality(label):
    try:
        try:
            label = int(re.search('(\d+)', label).group(1))
        except Exception:
            label = 0

        if label >= 2160:
            return '4K'
        elif label >= 1440:
            return '1440p'
        elif label >= 1080:
            return '1080p'
        elif 720 <= label < 1080:
            return '720p'
        elif label < 720:
            return 'SD'
    except Exception:
        return 'SD'


def strip_domain(url):
    try:
        if url.lower().startswith('http') or url.startswith('/'):
            url = re.findall('(?://.+?|)(/.+)', url)[0]
        url = client.replaceHTMLCodes(url)
        url = url.encode('utf-8')
        return url
    except Exception:
        return


def is_host_valid(url, domains):
    try:
        host = __top_domain(url)
        hosts = [domain.lower() for domain in domains if host and host in domain.lower()]

        if hosts and '.' not in host:
            host = hosts[0]
        if hosts and any([h for h in ['google', 'picasa', 'blogspot'] if h in host]):
            host = 'gvideo'
        if hosts and any([h for h in ['akamaized', 'ocloud'] if h in host]):
            host = 'CDN'
        return any(hosts), host
    except Exception:
        return False, ''


def __top_domain(url):
    elements = urlparse.urlparse(url)
    domain = elements.netloc or elements.path
    domain = domain.split('@')[-1].split(':')[0]
    regex = "(?:www\.)?([\w\-]*\.[\w\-]{2,3}(?:\.[\w\-]{2,3})?)$"
    res = re.search(regex, domain)
    if res:
        domain = res.group(1)
    domain = domain.lower()
    return domain


def uResolve(url):
    resolvers = resolveurl.relevant_resolvers(order_matters=True)
    hostDict = resolvers
    hostDict = [i.domains for i in hostDict if '*' not in i.domains]
    hostDict = [i.lower() for i in reduce(lambda x, y: x+y, hostDict)]
    hostDict = [x for y, x in enumerate(hostDict) if x not in hostDict[:y]]
    valid, host = is_host_valid(url, hostDict)
    if not valid:
        log_utils.log('Source Utils uResolve: Invalid Host: ' + str(url))
        return None
    try:
        resolver = [resolver for resolver in resolvers if resolver.name in url][0]
        host, media_id = resolver().get_host_and_id(url)
        url = resolver().get_media_url(host, media_id)
    except Exception:
        failure = traceback.format_exc()
        log_utils.log('Source Utils uResolve: Invalid Resolve: ' + str(failure))
        return None
    return url


def aliases_to_array(aliases, filter=None):
    try:
        if not filter:
            filter = []
        if isinstance(filter, str):
            filter = [filter]

        return [x.get('title') for x in aliases if not filter or x.get('country') in filter]
    except Exception:
        return []


def append_headers(headers):
    return '|%s' % '&'.join(['%s=%s' % (key, urllib.quote_plus(headers[key])) for key in headers])


def get_size(url):
    try:
        size = client.request(url, output='file_size')
        if size == '0':
            size = False
        size = convert_size(size)
        return size
    except Exception:
        return False


def convert_size(size_bytes):
    import math
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    if size_name[i] == 'B' or size_name[i] == 'KB':
        return None
    return "%s %s" % (s, size_name[i])


def check_directstreams(url, hoster='', quality='SD'):
    urls = []
    host = hoster

    if 'google' in url or any(x in url for x in ['youtube.', 'docid=']):
        urls = directstream.google(url)
        if not urls:
            tag = directstream.googletag(url)
            if tag:
                urls = [{'quality': tag[0]['quality'], 'url': url}]
        if urls:
            host = 'gvideo'
    elif 'ok.ru' in url:
        urls = directstream.odnoklassniki(url)
        if urls:
            host = 'vk'
    elif 'vk.com' in url:
        urls = directstream.vk(url)
        if urls:
            host = 'vk'
    elif any(x in url for x in ['akamaized', 'blogspot', 'ocloud.stream']):
        urls = [{'url': url}]
        if urls:
            host = 'CDN'

    direct = True if urls else False

    if not urls:
        urls = [{'quality': quality, 'url': url}]

    return urls, host, direct


# if salt is provided, it should be string
# ciphertext is base64 and passphrase is string
def evp_decode(cipher_text, passphrase, salt=None):
    cipher_text = base64.b64decode(cipher_text)
    if not salt:
        salt = cipher_text[8:16]
        cipher_text = cipher_text[16:]
    data = evpKDF(passphrase, salt)
    decrypter = pyaes.Decrypter(pyaes.AESModeOfOperationCBC(data['key'], data['iv']))
    plain_text = decrypter.feed(cipher_text)
    plain_text += decrypter.feed()
    return plain_text


def evpKDF(passwd, salt, key_size=8, iv_size=4, iterations=1, hash_algorithm="md5"):
    target_key_size = key_size + iv_size
    derived_bytes = ""
    number_of_derived_words = 0
    block = None
    hasher = hashlib.new(hash_algorithm)
    while number_of_derived_words < target_key_size:
        if block is not None:
            hasher.update(block)

        hasher.update(passwd)
        hasher.update(salt)
        block = hasher.digest()
        hasher = hashlib.new(hash_algorithm)

        for _i in range(1, iterations):
            hasher.update(block)
            block = hasher.digest()
            hasher = hashlib.new(hash_algorithm)

        derived_bytes += block[0: min(len(block), (target_key_size - number_of_derived_words) * 4)]

        number_of_derived_words += len(block) / 4

    return {
        "key": derived_bytes[0: key_size * 4],
        "iv": derived_bytes[key_size * 4:]
    }
