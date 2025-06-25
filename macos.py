# Code written by SayyadN
# Code Version 2
#Date : 25-6-2025
# Code For Download macos Recovery & Installers & EFI Folders 

# Resources
# macrecovery_open_core : https://tinyurl.com/bdfkbw43
# olarila_efis : https://tinyurl.com/rkr3w93n
# All Thanks For Tim Sutton && Greg Neagle && vit9696.

#importing Reqired Libs
from __future__ import (
    absolute_import, division, print_function, unicode_literals)
try:
    # python 2
    from urllib.parse import urlsplit

except ImportError:
    # python 3
    from urlparse import urlsplit
from xml.dom import minidom
from xml.parsers.expat import ExpatError
import argparse
import hashlib
import json
import linecache
import os
import random
import struct
import string
import sys
import argparse
import gzip
import plistlib
import subprocess
from cpuinfo import get_cpu_info

#For Checking Xattr 
try:
    import xattr
except ImportError:
    print("This tool requires the Python xattr module. "
          "Perhaps run `pip install xattr` to install it.")
    sys.exit(-1)
try:
    from urllib.request import Request, HTTPError, urlopen
    from urllib.parse import urlparse
except ImportError:
    print('ERROR: Python 2 is not supported, please use Python 3')
    sys.exit(1)


# Main variables for making programming easy

ifit = os.path.exists
p = print


SELF_DIR = os.path.dirname(os.path.realpath(__file__))

# MacPro7,1
RECENT_MAC = 'Mac-27AD2F918AE68F61'
MLB_ZERO = '00000000000000000'
MLB_VALID = 'F5K105303J9K3F71M'
MLB_PRODUCT = 'F5K00000000K3F700'

TYPE_SID = 16
TYPE_K = 64
TYPE_FG = 64

INFO_PRODUCT = 'AP'
INFO_IMAGE_LINK = 'AU'
INFO_IMAGE_HASH = 'AH'
INFO_IMAGE_SESS = 'AT'
INFO_SIGN_LINK = 'CU'
INFO_SIGN_HASH = 'CH'
INFO_SIGN_SESS = 'CT'
INFO_REQURED = [INFO_PRODUCT, INFO_IMAGE_LINK, INFO_IMAGE_HASH, INFO_IMAGE_SESS, INFO_SIGN_LINK, INFO_SIGN_HASH, INFO_SIGN_SESS]

# Use -2 for better resize stability on Windows
TERMINAL_MARGIN = 2

DEFAULT_SUCATALOGS = {
    '17': 'https://swscan.apple.com/content/catalogs/others/'
          'index-10.13-10.12-10.11-10.10-10.9'
          '-mountainlion-lion-snowleopard-leopard.merged-1.sucatalog',
    '18': 'https://swscan.apple.com/content/catalogs/others/'
          'index-10.14-10.13-10.12-10.11-10.10-10.9'
          '-mountainlion-lion-snowleopard-leopard.merged-1.sucatalog',
    '19': 'https://swscan.apple.com/content/catalogs/others/'
          'index-10.15-10.14-10.13-10.12-10.11-10.10-10.9'
          '-mountainlion-lion-snowleopard-leopard.merged-1.sucatalog',
    '20': 'https://swscan.apple.com/content/catalogs/others/'
          'index-10.16-10.15-10.14-10.13-10.12-10.11-10.10-10.9'
          '-mountainlion-lion-snowleopard-leopard.merged-1.sucatalog',
    '21': 'https://swscan.apple.com/content/catalogs/others/'
          'index-12-10.16-10.15-10.14-10.13-10.12-10.11-10.10-10.9'
          '-mountainlion-lion-snowleopard-leopard.merged-1.sucatalog',
    '22': 'https://swscan.apple.com/content/catalogs/others/'
          'index-13-12-10.16-10.15-10.14-10.13-10.12-10.11-10.10-10.9'
          '-mountainlion-lion-snowleopard-leopard.merged-1.sucatalog',
    '23': 'https://swscan.apple.com/content/catalogs/others/'
          'index-14-13-12-10.16-10.15-10.14-10.13-10.12-10.11-10.10-10.9'
          '-mountainlion-lion-snowleopard-leopard.merged-1.sucatalog',
    '24': 'https://swscan.apple.com/content/catalogs/others/'
          'index-15-14-13-12-10.16-10.15-10.14-10.13-10.12-10.11-10.10-10.9'
          '-mountainlion-lion-snowleopard-leopard.merged-1.sucatalog',
    '25': 'https://swscan.apple.com/content/catalogs/others/'
          'index-26-15-14-13-12-10.16-10.15-10.14-10.13-10.12-10.11-10.10-10.9'
          '-mountainlion-lion-snowleopard-leopard.merged-1.sucatalog'
}

SEED_CATALOGS_PLIST = (
    '/System/Library/PrivateFrameworks/Seeding.framework/Versions/Current/'
    'Resources/SeedCatalogs.plist'
)
def check_files_path():
    macrecovery = ifit("macos.py")
    macboards = ifit("boards.json")
    build_image = ifit("build-image.sh")
    
    check_list = []  # empty list for check files
    # checking file path if exists or not
    if macrecovery:
        check_list.append("macos.py : Available")
    else:
        check_list.append("macrecovery.py : Not Available")
    if macboards:
        check_list.append("boards.json : Available")
    else:
        check_list.append("boards.json : Not Available")
    if build_image:
        check_list.append("build-image.sh : Available")
    else:
        check_list.append("build-image.sh : Not Available")

    p(check_list)
    
    # Stop the process if any file is not available
    if not (macrecovery and macboards and build_image):
        p("One or more required files are missing. Stopping the process.")
        exit(1)

def run_query(url, headers, post=None, raw=False):
    if post is not None:
        data = '\n'.join(entry + '=' + post[entry] for entry in post).encode()
    else:
        data = None
    req = Request(url=url, headers=headers, data=data)
    try:
        response = urlopen(req)
        if raw:
            return response
        return dict(response.info()), response.read()
    except HTTPError as e:
        print(f'ERROR: "{e}" when connecting to {url}')
        sys.exit(1)


def generate_id(id_type, id_value=None):
    return id_value or ''.join(random.choices(string.hexdigits[:16].upper(), k=id_type))


def product_mlb(mlb):
    return '00000000000' + mlb[11:15] + '00'


def mlb_from_eeee(eeee):
    if len(eeee) != 4:
        print('ERROR: Invalid EEEE code length!')
        sys.exit(1)

    return f'00000000000{eeee}00'


# zhangyoufu https://gist.github.com/MCJack123/943eaca762730ca4b7ae460b731b68e7#gistcomment-3061078 2021-10-08
Apple_EFI_ROM_public_key_1 = 0xC3E748CAD9CD384329E10E25A91E43E1A762FF529ADE578C935BDDF9B13F2179D4855E6FC89E9E29CA12517D17DFA1EDCE0BEBF0EA7B461FFE61D94E2BDF72C196F89ACD3536B644064014DAE25A15DB6BB0852ECBD120916318D1CCDEA3C84C92ED743FC176D0BACA920D3FCF3158AFF731F88CE0623182A8ED67E650515F75745909F07D415F55FC15A35654D118C55A462D37A3ACDA08612F3F3F6571761EFCCBCC299AEE99B3A4FD6212CCFFF5EF37A2C334E871191F7E1C31960E010A54E86FA3F62E6D6905E1CD57732410A3EB0C6B4DEFDABE9F59BF1618758C751CD56CEF851D1C0EAA1C558E37AC108DA9089863D20E2E7E4BF475EC66FE6B3EFDCF

ChunkListHeader = struct.Struct('<4sIBBBxQQQ')
assert ChunkListHeader.size == 0x24

Chunk = struct.Struct('<I32s')
assert Chunk.size == 0x24


def verify_chunklist(cnkpath):
    with open(cnkpath, 'rb') as f:
        hash_ctx = hashlib.sha256()
        data = f.read(ChunkListHeader.size)
        hash_ctx.update(data)
        magic, header_size, file_version, chunk_method, signature_method, chunk_count, chunk_offset, signature_offset = ChunkListHeader.unpack(data)
        assert magic == b'CNKL'
        assert header_size == ChunkListHeader.size
        assert file_version == 1
        assert chunk_method == 1
        assert signature_method in [1, 2]
        assert chunk_count > 0
        assert chunk_offset == 0x24
        assert signature_offset == chunk_offset + Chunk.size * chunk_count
        for _ in range(chunk_count):
            data = f.read(Chunk.size)
            hash_ctx.update(data)
            chunk_size, chunk_sha256 = Chunk.unpack(data)
            yield chunk_size, chunk_sha256
        digest = hash_ctx.digest()
        if signature_method == 1:
            data = f.read(256)
            assert len(data) == 256
            signature = int.from_bytes(data, 'little')
            plaintext = int(f'0x1{"f"*404}003031300d060960864801650304020105000420{"0"*64}', 16) | int.from_bytes(digest, 'big')
            assert pow(signature, 0x10001, Apple_EFI_ROM_public_key_1) == plaintext
        elif signature_method == 2:
            data = f.read(32)
            assert data == digest
            raise RuntimeError('Chunklist missing digital signature')
        else:
            raise NotImplementedError
        assert f.read(1) == b''


def get_session(args):
    headers = {
        'Host': 'osrecovery.apple.com',
        'Connection': 'close',
        'User-Agent': 'InternetRecovery/1.0',
    }

    headers, _ = run_query('http://osrecovery.apple.com/', headers)

    if args.verbose:
        print('Session headers:')
        for header in headers:
            print(f'{header}: {headers[header]}')

    for header in headers:
        if header.lower() == 'set-cookie':
            cookies = headers[header].split('; ')
            for cookie in cookies:
                return cookie if cookie.startswith('session=') else ...

    raise RuntimeError('No session in headers ' + str(headers))


def get_image_info(session, bid, mlb=MLB_ZERO, diag=False, os_type='default', cid=None):
    headers = {
        'Host': 'osrecovery.apple.com',
        'Connection': 'close',
        'User-Agent': 'InternetRecovery/1.0',
        'Cookie': session,
        'Content-Type': 'text/plain',
    }

    post = {
        'cid': generate_id(TYPE_SID, cid),
        'sn': mlb,
        'bid': bid,
        'k': generate_id(TYPE_K),
        'fg': generate_id(TYPE_FG)
    }

    if diag:
        url = 'http://osrecovery.apple.com/InstallationPayload/Diagnostics'
    else:
        url = 'http://osrecovery.apple.com/InstallationPayload/RecoveryImage'
        post['os'] = os_type

    headers, output = run_query(url, headers, post)

    output = output.decode('utf-8')
    info = {}
    for line in output.split('\n'):
        try:
            key, value = line.split(': ')
            info[key] = value
        except KeyError:
            continue
        except ValueError:
            continue

    for k in INFO_REQURED:
        if k not in info:
            raise RuntimeError(f'Missing key {k}')

    return info


def save_image(url, sess, filename='', directory=''):
    purl = urlparse(url)
    headers = {
        'Host': purl.hostname,
        'Connection': 'close',
        'User-Agent': 'InternetRecovery/1.0',
        'Cookie': '='.join(['AssetToken', sess])
    }

    if not os.path.exists(directory):
        os.makedirs(directory)

    if filename == '':
        filename = os.path.basename(purl.path)
    if filename.find(os.sep) >= 0 or filename == '':
        raise RuntimeError('Invalid save path ' + filename)

    print(f'Saving {url} to {directory}{os.sep}{filename}...')

    with open(os.path.join(directory, filename), 'wb') as fh:
        response = run_query(url, headers, raw=True)
        headers = dict(response.headers)
        totalsize = -1
        for header in headers:
            if header.lower() == 'content-length':
                totalsize = int(headers[header])
                break
        size = 0
        oldterminalsize = 0
        while True:
            chunk = response.read(2**20)
            if not chunk:
                break
            fh.write(chunk)
            size += len(chunk)
            terminalsize = max(os.get_terminal_size().columns - TERMINAL_MARGIN, 0)
            if oldterminalsize != terminalsize:
                print(f'\r{"":<{terminalsize}}', end='')
                oldterminalsize = terminalsize
            if totalsize > 0:
                progress = size / totalsize
                barwidth = terminalsize // 3
                print(f'\r{size / (2**20):.1f}/{totalsize / (2**20):.1f} MB ', end='')
                if terminalsize > 55:
                    print(f'|{"=" * int(barwidth * progress):<{barwidth}}|', end='')
                print(f' {progress*100:.1f}% downloaded', end='')
            else:
                # Fallback if Content-Length isn't available
                print(f'\r{size / (2**20)} MB downloaded...', end='')
            sys.stdout.flush()
        print('\nDownload complete!')

    return os.path.join(directory, os.path.basename(filename))


def verify_image(dmgpath, cnkpath):
    print('Verifying image with chunklist...')

    with open(dmgpath, 'rb') as dmgf:
        for cnkcount, (cnksize, cnkhash) in enumerate(verify_chunklist(cnkpath), 1):
            terminalsize = max(os.get_terminal_size().columns - TERMINAL_MARGIN, 0)
            print(f'\r{f"Chunk {cnkcount} ({cnksize} bytes)":<{terminalsize}}', end='')
            sys.stdout.flush()
            cnk = dmgf.read(cnksize)
            if len(cnk) != cnksize:
                raise RuntimeError(f'Invalid chunk {cnkcount} size: expected {cnksize}, read {len(cnk)}')
            if hashlib.sha256(cnk).digest() != cnkhash:
                raise RuntimeError(f'Invalid chunk {cnkcount}: hash mismatch')
        if dmgf.read(1) != b'':
            raise RuntimeError('Invalid image: larger than chunklist')
        print('\nImage verification complete!')


def action_download(args):
    """
    Reference information for queries:

    Recovery latest:
    cid=3076CE439155BA14
    sn=...
    bid=Mac-E43C1C25D4880AD6
    k=4BE523BB136EB12B1758C70DB43BDD485EBCB6A457854245F9E9FF0587FB790C
    os=latest
    fg=B2E6AA07DB9088BE5BDB38DB2EA824FDDFB6C3AC5272203B32D89F9D8E3528DC

    Recovery default:
    cid=4A35CB95FF396EE7
    sn=...
    bid=Mac-E43C1C25D4880AD6
    k=0A385E6FFC3DDD990A8A1F4EC8B98C92CA5E19C9FF1DD26508C54936D8523121
    os=default
    fg=B2E6AA07DB9088BE5BDB38DB2EA824FDDFB6C3AC5272203B32D89F9D8E3528DC

    Diagnostics:
    cid=050C59B51497CEC8
    sn=...
    bid=Mac-E43C1C25D4880AD6
    k=37D42A8282FE04A12A7D946304F403E56A2155B9622B385F3EB959A2FBAB8C93
    fg=B2E6AA07DB9088BE5BDB38DB2EA824FDDFB6C3AC5272203B32D89F9D8E3528DC
    """

    session = get_session(args)
    info = get_image_info(session, bid=args.board_id, mlb=args.mlb, diag=args.diagnostics, os_type=args.os_type)
    if args.verbose:
        print(info)
    print(f'Downloading {info[INFO_PRODUCT]}...')
    cnkname = '' if args.basename == '' else args.basename + '.chunklist'
    cnkpath = save_image(info[INFO_SIGN_LINK], info[INFO_SIGN_SESS], cnkname, args.outdir)
    dmgname = '' if args.basename == '' else args.basename + '.dmg'
    dmgpath = save_image(info[INFO_IMAGE_LINK], info[INFO_IMAGE_SESS], dmgname, args.outdir)
    try:
        verify_image(dmgpath, cnkpath)
        return 0
    except Exception as err:
        if isinstance(err, AssertionError) and str(err) == '':
            try:
                tb = sys.exc_info()[2]
                while tb.tb_next:
                    tb = tb.tb_next
                err = linecache.getline(tb.tb_frame.f_code.co_filename, tb.tb_lineno, tb.tb_frame.f_globals).strip()
            except Exception:
                err = "Invalid chunklist"
        print(f'\rImage verification failed. ({err})')
        return 1


def action_selfcheck(args):
    """
    Sanity check server logic for recovery:

    if not valid(bid):
        return error()
    ppp = get_ppp(sn)
    if not valid(ppp):
        return latest_recovery(bid = bid)             # Returns newest for bid.
    if valid(sn):
        if os == 'default':
            return default_recovery(sn = sn, ppp = ppp) # Returns oldest for sn.
        else:
            return latest_recovery(sn = sn, ppp = ppp)  # Returns newest for sn.
    return default_recovery(ppp = ppp)              # Returns oldest.
    """

    session = get_session(args)
    valid_default = get_image_info(session, bid=RECENT_MAC, mlb=MLB_VALID, diag=False, os_type='default')
    valid_latest = get_image_info(session, bid=RECENT_MAC, mlb=MLB_VALID, diag=False, os_type='latest')
    product_default = get_image_info(session, bid=RECENT_MAC, mlb=MLB_PRODUCT, diag=False, os_type='default')
    product_latest = get_image_info(session, bid=RECENT_MAC, mlb=MLB_PRODUCT, diag=False, os_type='latest')
    generic_default = get_image_info(session, bid=RECENT_MAC, mlb=MLB_ZERO, diag=False, os_type='default')
    generic_latest = get_image_info(session, bid=RECENT_MAC, mlb=MLB_ZERO, diag=False, os_type='latest')

    if args.verbose:
        print(valid_default)
        print(valid_latest)
        print(product_default)
        print(product_latest)
        print(generic_default)
        print(generic_latest)

    if valid_default[INFO_PRODUCT] == valid_latest[INFO_PRODUCT]:
        # Valid MLB must give different default and latest if this is not a too new product.
        print(f'ERROR: Cannot determine any previous product, got {valid_default[INFO_PRODUCT]}')
        return 1

    if product_default[INFO_PRODUCT] != product_latest[INFO_PRODUCT]:
        # Product-only MLB must give the same value for default and latest.
        print(f'ERROR: Latest and default do not match for product MLB, got {product_default[INFO_PRODUCT]} and {product_latest[INFO_PRODUCT]}')
        return 1

    if generic_default[INFO_PRODUCT] != generic_latest[INFO_PRODUCT]:
        # Zero MLB always give the same value for default and latest.
        print(f'ERROR: Generic MLB gives different product, got {generic_default[INFO_PRODUCT]} and {generic_latest[INFO_PRODUCT]}')
        return 1

    if valid_latest[INFO_PRODUCT] != generic_latest[INFO_PRODUCT]:
        # Valid MLB must always equal generic MLB.
        print(f'ERROR: Cannot determine unified latest product, got {valid_latest[INFO_PRODUCT]} and {generic_latest[INFO_PRODUCT]}')
        return 1

    if product_default[INFO_PRODUCT] != valid_default[INFO_PRODUCT]:
        # Product-only MLB can give the same value with valid default MLB.
        # This is not an error for all models, but for our chosen code it is.
        print(f'ERROR: Valid and product MLB give mismatch, got {product_default[INFO_PRODUCT]} and {valid_default[INFO_PRODUCT]}')
        return 1

    print('SUCCESS: Found no discrepancies with MLB validation algorithm!')
    return 0


def action_verify(args):
    """
    Try to verify MLB serial number.
    """
    session = get_session(args)
    generic_latest = get_image_info(session, bid=RECENT_MAC, mlb=MLB_ZERO, diag=False, os_type='latest')
    uvalid_default = get_image_info(session, bid=args.board_id, mlb=args.mlb, diag=False, os_type='default')
    uvalid_latest = get_image_info(session, bid=args.board_id, mlb=args.mlb, diag=False, os_type='latest')
    uproduct_default = get_image_info(session, bid=args.board_id, mlb=product_mlb(args.mlb), diag=False, os_type='default')

    if args.verbose:
        print(generic_latest)
        print(uvalid_default)
        print(uvalid_latest)
        print(uproduct_default)

    # Verify our MLB number.
    if uvalid_default[INFO_PRODUCT] != uvalid_latest[INFO_PRODUCT]:
        print(f'SUCCESS: {args.mlb} MLB looks valid and supported!' if uvalid_latest[INFO_PRODUCT] == generic_latest[INFO_PRODUCT] else f'SUCCESS: {args.mlb} MLB looks valid, but probably unsupported!')
        return 0

    print('UNKNOWN: Run selfcheck, check your board-id, or try again later!')

    # Here we have matching default and latest products. This can only be true for very
    # new models. These models get either latest or special builds.
    if uvalid_default[INFO_PRODUCT] == generic_latest[INFO_PRODUCT]:
        print(f'UNKNOWN: {args.mlb} MLB can be valid if very new!')
        return 0
    if uproduct_default[INFO_PRODUCT] != uvalid_default[INFO_PRODUCT]:
        print(f'UNKNOWN: {args.mlb} MLB looks invalid, other models use product {uproduct_default[INFO_PRODUCT]} instead of {uvalid_default[INFO_PRODUCT]}!')
        return 0
    print(f'UNKNOWN: {args.mlb} MLB can be valid if very new and using special builds!')
    return 0


def action_guess(args):
    """
    Attempt to guess which model does this MLB belong.
    """

    mlb = args.mlb
    anon = mlb.startswith('000')

    with open(args.board_db, 'r', encoding='utf-8') as fh:
        db = json.load(fh)

    supported = {}

    session = get_session(args)

    generic_latest = get_image_info(session, bid=RECENT_MAC, mlb=MLB_ZERO, diag=False, os_type='latest')

    for model in db:
        try:
            if anon:
                # For anonymous lookup check when given model does not match latest.
                model_latest = get_image_info(session, bid=model, mlb=MLB_ZERO, diag=False, os_type='latest')

                if model_latest[INFO_PRODUCT] != generic_latest[INFO_PRODUCT]:
                    if db[model] == 'current':
                        print(f'WARN: Skipped {model} due to using latest product {model_latest[INFO_PRODUCT]} instead of {generic_latest[INFO_PRODUCT]}')
                    continue

                user_default = get_image_info(session, bid=model, mlb=mlb, diag=False, os_type='default')

                if user_default[INFO_PRODUCT] != generic_latest[INFO_PRODUCT]:
                    supported[model] = [db[model], user_default[INFO_PRODUCT], generic_latest[INFO_PRODUCT]]
            else:
                # For normal lookup check when given model has mismatching normal and latest.
                user_latest = get_image_info(session, bid=model, mlb=mlb, diag=False, os_type='latest')

                user_default = get_image_info(session, bid=model, mlb=mlb, diag=False, os_type='default')

                if user_latest[INFO_PRODUCT] != user_default[INFO_PRODUCT]:
                    supported[model] = [db[model], user_default[INFO_PRODUCT], user_latest[INFO_PRODUCT]]

        except Exception as e:
            print(f'WARN: Failed to check {model}, exception: {e}')

    if len(supported) > 0:
        print(f'SUCCESS: MLB {mlb} looks supported for:')
        for model in supported.items():
            print(f'- {model}, up to {supported[model][0]}, default: {supported[model][1]}, latest: {supported[model][2]}')
        return 0

    print(f'UNKNOWN: Failed to determine supported models for MLB {mlb}!')
    return None




def get_input(prompt=None):
    '''Python 2 and 3 wrapper for raw_input/input'''
    try:
        return raw_input(prompt)
    except NameError:
        # raw_input doesn't exist in Python 3
        return input(prompt)


def read_plist(filepath):
    '''Wrapper for the differences between Python 2 and Python 3's plistlib'''
    try:
        with open(filepath, "rb") as fileobj:
            return plistlib.load(fileobj)
    except AttributeError:
        # plistlib module doesn't have a load function (as in Python 2)
        return plistlib.readPlist(filepath)


def read_plist_from_string(bytestring):
    '''Wrapper for the differences between Python 2 and Python 3's plistlib'''
    try:
        return plistlib.loads(bytestring)
    except AttributeError:
        # plistlib module doesn't have a load function (as in Python 2)
        return plistlib.readPlistFromString(bytestring)


def get_seeding_program(sucatalog_url):
    '''Returns a seeding program name based on the sucatalog_url'''
    try:
        seed_catalogs = read_plist(SEED_CATALOGS_PLIST)
        for key, value in seed_catalogs.items():
            if sucatalog_url == value:
                return key
        return ''
    except (OSError, IOError, ExpatError, AttributeError, KeyError) as err:
        print(err, file=sys.stderr)
        return ''


def get_seed_catalog(seedname='DeveloperSeed'):
    '''Returns the developer seed sucatalog'''
    try:
        seed_catalogs = read_plist(SEED_CATALOGS_PLIST)
        return seed_catalogs.get(seedname)
    except (OSError, IOError, ExpatError, AttributeError, KeyError) as err:
        print(err, file=sys.stderr)
        return ''


def get_seeding_programs():
    '''Returns the list of seeding program names'''
    try:
        seed_catalogs = read_plist(SEED_CATALOGS_PLIST)
        return list(seed_catalogs.keys())
    except (OSError, IOError, ExpatError, AttributeError, KeyError) as err:
        print(err, file=sys.stderr)
        return ''


def get_default_catalog():
    '''Returns the default softwareupdate catalog for the current OS'''
    darwin_major = os.uname()[2].split('.')[0]
    return DEFAULT_SUCATALOGS.get(darwin_major)


def make_sparse_image(volume_name, output_path):
    '''Make a sparse disk image we can install a product to'''
    # note: for macOS 26 Tahoe we needed to increase the size
    cmd = ['/usr/bin/hdiutil', 'create', '-size', '20g', '-fs', 'HFS+',
           '-volname', volume_name, '-type', 'SPARSE', '-plist', output_path]
    try:
        output = subprocess.check_output(cmd)
    except subprocess.CalledProcessError as err:
        print(err, file=sys.stderr)
        exit(-1)
    try:
        return read_plist_from_string(output)[0]
    except IndexError as err:
        print('Unexpected output from hdiutil: %s' % output, file=sys.stderr)
        exit(-1)
    except ExpatError as err:
        print('Malformed output from hdiutil: %s' % output, file=sys.stderr)
        print(err, file=sys.stderr)
        exit(-1)


def make_compressed_dmg(app_path, diskimagepath):
    """Returns path to newly-created compressed r/o disk image containing
    Install macOS.app"""

    print('Making read-only compressed disk image containing %s...'
          % os.path.basename(app_path))
    cmd = ['/usr/bin/hdiutil', 'create', '-fs', 'HFS+',
           '-srcfolder', app_path, diskimagepath]
    try:
        subprocess.check_call(cmd)
    except subprocess.CalledProcessError as err:
        print(err, file=sys.stderr)
    else:
        print('Disk image created at: %s' % diskimagepath)


def mountdmg(dmgpath):
    """
    Attempts to mount the dmg at dmgpath and returns first mountpoint
    """
    mountpoints = []
    dmgname = os.path.basename(dmgpath)
    cmd = ['/usr/bin/hdiutil', 'attach', dmgpath,
           '-mountRandom', '/tmp', '-nobrowse', '-plist',
           '-owners', 'on']
    proc = subprocess.Popen(cmd, bufsize=-1,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (pliststr, err) = proc.communicate()
    if proc.returncode:
        print('Error: "%s" while mounting %s.' % (err, dmgname),
              file=sys.stderr)
        return None
    if pliststr:
        plist = read_plist_from_string(pliststr)
        for entity in plist['system-entities']:
            if 'mount-point' in entity:
                mountpoints.append(entity['mount-point'])

    return mountpoints[0]


def unmountdmg(mountpoint):
    """
    Unmounts the dmg at mountpoint
    """
    proc = subprocess.Popen(['/usr/bin/hdiutil', 'detach', mountpoint],
                            bufsize=-1, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    (dummy_output, err) = proc.communicate()
    if proc.returncode:
        print('Polite unmount failed: %s' % err, file=sys.stderr)
        print('Attempting to force unmount %s' % mountpoint, file=sys.stderr)
        # try forcing the unmount
        retcode = subprocess.call(['/usr/bin/hdiutil', 'detach', mountpoint,
                                   '-force'])
        if retcode:
            print('Failed to unmount %s' % mountpoint, file=sys.stderr)


def install_product(dist_path, target_vol):
    '''Install a product to a target volume.
    Returns a boolean to indicate success or failure.'''
    # set CM_BUILD env var to make Installer bypass eligibilty checks
    # when installing packages (for machine-specific OS builds)
    os.environ["CM_BUILD"] = "CM_BUILD"
    cmd = ['/usr/sbin/installer', '-pkg', dist_path, '-target', target_vol]
    try:
        subprocess.check_call(cmd)
    except subprocess.CalledProcessError as err:
        print(err, file=sys.stderr)
        return False
    else:
        # Apple postinstall script bug ends up copying files to a path like
        # /tmp/dmg.T9ak1HApplications
        path = target_vol + 'Applications'
        if os.path.exists(path):
            print('*********************************************************')
            print('*** Working around a very dumb Apple bug in a package ***')
            print('*** postinstall script that fails to correctly target ***')
            print('*** the Install macOS.app when installed to a volume  ***')
            print('*** other than the current boot volume.               ***')
            print('***       Please file feedback with Apple!            ***')
            print('*********************************************************')
            subprocess.check_call(
                ['/usr/bin/ditto',
                 path,
                 os.path.join(target_vol, 'Applications')]
            )
            subprocess.check_call(['/bin/rm', '-r', path])
        return True

class ReplicationError(Exception):
    '''A custom error when replication fails'''
    pass


def replicate_url(full_url,
                  root_dir='/tmp',
                  show_progress=False,
                  ignore_cache=False,
                  attempt_resume=False):
    '''Downloads a URL and stores it in the same relative path on our
    filesystem. Returns a path to the replicated file.'''

    path = urlsplit(full_url)[2]
    relative_url = path.lstrip('/')
    relative_url = os.path.normpath(relative_url)
    local_file_path = os.path.join(root_dir, relative_url)
    if show_progress:
        options = '-fL'
    else:
        options = '-sfL'
    need_download = True
    while need_download:
        curl_cmd = ['/usr/bin/curl', options,
                    '--create-dirs',
                    '-o', local_file_path,
                    '-w', '%{http_code}']
        if not full_url.endswith(".gz"):
            # stupid hack for stupid Apple behavior where it sometimes returns
            # compressed files even when not asked for
            curl_cmd.append('--compressed')
        resumed = False
        if not ignore_cache and os.path.exists(local_file_path):
            if not attempt_resume:
                curl_cmd.extend(['-z', local_file_path])
            else:
                resumed = True
                curl_cmd.extend(['-z', '-' + local_file_path, '-C', '-'])
        curl_cmd.append(full_url)
        print("Downloading %s..." % full_url)
        need_download = False
        try:
            output = subprocess.check_output(curl_cmd)
        except subprocess.CalledProcessError as err:
            if not resumed or not err.output.isdigit():
                raise ReplicationError(err)
            # HTTP error 416 on resume: the download is already complete and the
            # file is up-to-date
            # HTTP error 412 on resume: the file was updated server-side
            if int(err.output) == 412:
                print("Removing %s and retrying." % local_file_path)
                os.unlink(local_file_path)
                need_download = True
            elif int(err.output) != 416:
                raise ReplicationError(err)
    return local_file_path


def parse_server_metadata(filename):
    '''Parses a softwareupdate server metadata file, looking for information
    of interest.
    Returns a dictionary containing title, version, and description.'''
    title = ''
    vers = ''
    try:
        md_plist = read_plist(filename)
    except (OSError, IOError, ExpatError) as err:
        print('Error reading %s: %s' % (filename, err), file=sys.stderr)
        return {}
    vers = md_plist.get('CFBundleShortVersionString', '')
    localization = md_plist.get('localization', {})
    preferred_localization = (localization.get('English') or
                              localization.get('en'))
    if preferred_localization:
        title = preferred_localization.get('title', '')

    metadata = {}
    metadata['title'] = title
    metadata['version'] = vers
    return metadata


def get_server_metadata(catalog, product_key, workdir, ignore_cache=False):
    '''Replicate ServerMetaData'''
    try:
        url = catalog['Products'][product_key]['ServerMetadataURL']
        try:
            smd_path = replicate_url(
                url, root_dir=workdir, ignore_cache=ignore_cache)
            return smd_path
        except ReplicationError as err:
            print('Could not replicate %s: %s' % (url, err), file=sys.stderr)
            return None
    except KeyError:
        #print('Malformed catalog.', file=sys.stderr)
        return None


def parse_dist(filename):
    '''Parses a softwareupdate dist file, returning a dict of info of
    interest'''
    dist_info = {}
    try:
        dom = minidom.parse(filename)
    except ExpatError:
        print('Invalid XML in %s' % filename, file=sys.stderr)
        return dist_info
    except IOError as err:
        print('Error reading %s: %s' % (filename, err), file=sys.stderr)
        return dist_info

    titles = dom.getElementsByTagName('title')
    if titles:
        dist_info['title_from_dist'] = titles[0].firstChild.wholeText

    auxinfos = dom.getElementsByTagName('auxinfo')
    if not auxinfos:
        return dist_info
    auxinfo = auxinfos[0]
    key = None
    value = None
    children = auxinfo.childNodes
    # handle the possibility that keys from auxinfo may be nested
    # within a 'dict' element
    dict_nodes = [n for n in auxinfo.childNodes
                  if n.nodeType == n.ELEMENT_NODE and
                  n.tagName == 'dict']
    if dict_nodes:
        children = dict_nodes[0].childNodes
    for node in children:
        if node.nodeType == node.ELEMENT_NODE and node.tagName == 'key':
            key = node.firstChild.wholeText
        if node.nodeType == node.ELEMENT_NODE and node.tagName == 'string':
            value = node.firstChild.wholeText
        if key and value:
            dist_info[key] = value
            key = None
            value = None
    return dist_info


def download_and_parse_sucatalog(sucatalog, workdir, ignore_cache=False):
    '''Downloads and returns a parsed softwareupdate catalog'''
    try:
        localcatalogpath = replicate_url(
            sucatalog, root_dir=workdir, ignore_cache=ignore_cache)
    except ReplicationError as err:
        print('Could not replicate %s: %s' % (sucatalog, err), file=sys.stderr)
        exit(-1)
    if os.path.splitext(localcatalogpath)[1] == '.gz':
        with gzip.open(localcatalogpath) as the_file:
            content = the_file.read()
            try:
                catalog = read_plist_from_string(content)
                return catalog
            except ExpatError as err:
                print('Error reading %s: %s' % (localcatalogpath, err),
                      file=sys.stderr)
                exit(-1)
    else:
        try:
            catalog = read_plist(localcatalogpath)
            return catalog
        except (OSError, IOError, ExpatError) as err:
            print('Error reading %s: %s' % (localcatalogpath, err),
                  file=sys.stderr)
            exit(-1)


def find_mac_os_installers(catalog):
    '''Return a list of product identifiers for what appear to be macOS
    installers'''
    mac_os_installer_products = []
    if 'Products' in catalog:
        for product_key in catalog['Products'].keys():
            product = catalog['Products'][product_key]
            try:
                if product['ExtendedMetaInfo'][
                        'InstallAssistantPackageIdentifiers']:
                    mac_os_installer_products.append(product_key)
            except KeyError:
                continue
    return mac_os_installer_products


def os_installer_product_info(catalog, workdir, ignore_cache=False):
    '''Returns a dict of info about products that look like macOS installers'''
    product_info = {}
    installer_products = find_mac_os_installers(catalog)
    for product_key in installer_products:
        product_info[product_key] = {}
        filename = get_server_metadata(catalog, product_key, workdir)
        if filename:
            product_info[product_key] = parse_server_metadata(filename)
        else:
            print('No server metadata for %s' % product_key)
            product_info[product_key]['title'] = None
            product_info[product_key]['version'] = None

        product = catalog['Products'][product_key]
        product_info[product_key]['PostDate'] = product['PostDate']
        distributions = product['Distributions']
        dist_url = distributions.get('English') or distributions.get('en')
        try:
            dist_path = replicate_url(
                dist_url, root_dir=workdir, ignore_cache=ignore_cache)
        except ReplicationError as err:
            print('Could not replicate %s: %s' % (dist_url, err),
                  file=sys.stderr)
        else:
            dist_info = parse_dist(dist_path)
            product_info[product_key]['DistributionPath'] = dist_path
            product_info[product_key].update(dist_info)
            if not product_info[product_key]['title']:
                product_info[product_key]['title'] = dist_info.get('title_from_dist')
            if not product_info[product_key]['version']:
                product_info[product_key]['version'] = dist_info.get('VERSION')
        
    return product_info


def replicate_product(catalog, product_id, workdir, ignore_cache=False):
    '''Downloads all the packages for a product'''
    product = catalog['Products'][product_id]
    for package in product.get('Packages', []):
        # TO-DO: Check 'Size' attribute and make sure
        # we have enough space on the target
        # filesystem before attempting to download
        if 'URL' in package:
            try:
                replicate_url(
                    package['URL'], root_dir=workdir,
                    show_progress=True, ignore_cache=ignore_cache,
                    attempt_resume=(not ignore_cache))
            except ReplicationError as err:
                print('Could not replicate %s: %s' % (package['URL'], err),
                      file=sys.stderr)
                exit(-1)
        if 'MetadataURL' in package:
            try:
                replicate_url(package['MetadataURL'], root_dir=workdir,
                              ignore_cache=ignore_cache)
            except ReplicationError as err:
                print('Could not replicate %s: %s'
                      % (package['MetadataURL'], err), file=sys.stderr)
                exit(-1)


def find_installer_app(mountpoint):
    '''Returns the path to the Install macOS app on the mountpoint'''
    applications_dir = os.path.join(mountpoint, 'Applications')
    for item in os.listdir(applications_dir):
        if item.endswith('.app'):
            return os.path.join(applications_dir, item)
    return None
 



class efi_folders(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        super().__init__(option_strings, dest, nargs, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        # جلب معلومات المعالج
        cpuinfo_data = get_cpu_info()
        cpu_name = cpuinfo_data.get('brand_raw', 'Unknown Processor')
        print(f"Processor Name: {cpu_name}")
        print("\nIf your CPU starts with (for example) 6xxx, your CPU is Skylake.")
        print("You must choose it for your code name. Here's the list of Intel i5 generations:")

        # قائمة بأجيال معالجات i5
        intel_i5_generations = [
            "i5-1xxx (Nehalem)",
            "i5-2xxx (Sandy Bridge)",
            "i5-3xxx (Ivy Bridge)",
            "i5-4xxx (Haswell)",
            "i5-5xxx (Broadwell)",
            "i5-6xxx (Skylake)",
            "i5-7xxx (Kaby Lake)",
            "i5-8xxx (Coffee Lake)",
            "i5-9xxx (Coffee Lake Refresh)",
            "i5-10xxx (Comet Lake / Ice Lake)",
            "i5-11xxx (Tiger Lake / Rocket Lake)",
            "i5-12xxx (Alder Lake)",
            "i5-13xxx (Raptor Lake)",
            "i5-14xxx or Core 5xxx (Meteor Lake / Core Ultra)"
        ]
        
        # طباعة الأجيال
        for gen in intel_i5_generations:
            print(gen)

        print("\nDownload Your EFI From Here: olarila_efis : https://tinyurl.com/rkr3w93n")

        # تخزين القيمة في المتغير المرتبط بـ '--efi'
        setattr(namespace, self.dest, True)
        
        # Exit after showing EFI info
        parser.exit()


def main():
    check_files_path()
    parser = argparse.ArgumentParser(description="App By SAyyadN")
    
    parser.add_argument('action', choices=['download', 'selfcheck', 'verify', 'guess'],
                        help='Action to perform: "download" - performs recovery downloading,'
                             ' "selfcheck" checks whether MLB serial validation is possible, "verify" performs'
                             ' MLB serial verification, "guess" tries to find suitable mac model for MLB.',
                        nargs='?')  # Make action optional when using --efi
    
    parser.add_argument('-o', '--outdir', type=str, default='com.apple.recovery.boot')
    parser.add_argument('-n', '--basename', type=str, default='')
    parser.add_argument('-b', '--board-id', type=str, default=RECENT_MAC)
    parser.add_argument('-m', '--mlb', type=str, default=MLB_ZERO)
    parser.add_argument('-e', '--code', type=str, default='')
    parser.add_argument('-os', '--os-type', type=str, default='default', choices=['default', 'latest'])
    parser.add_argument('-diag', '--diagnostics', action='store_true')
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-db', '--board-db', type=str, default=os.path.join(SELF_DIR, 'boards.json'))
    parser.add_argument('--seedprogram', default='')
    parser.add_argument('--catalogurl', default='')
    parser.add_argument('--workdir', metavar='path_to_working_dir', default='.')
    parser.add_argument('--compress', action='store_true')
    parser.add_argument('--raw', action='store_true')
    parser.add_argument('--ignore-cache', action='store_true')

    # ✅ EFI argument using custom action class
    parser.add_argument('--efi', action=efi_folders, nargs=0, help="Show info and download link for EFI folders")

    args = parser.parse_args()

    # Check if action is provided (the efi_folders action will exit before reaching here)
    if not args.action:
        parser.error("action is required")

    # Root check for other operations
    if os.getuid() != 0:
        sys.exit('This command requires root (to install packages), so please run again with sudo or as root.')

    current_dir = os.getcwd()
    if os.path.expanduser("~") in current_dir:
        bad_dirs = ['Documents', 'Desktop', 'Downloads', 'Library']
        for bad_dir in bad_dirs:
            if bad_dir in os.path.split(current_dir):
                print('Running this script from %s may not work as expected. '
                      'If this does not run as expected, please run again from '
                      'somewhere else, such as /Users/Shared.'
                      % current_dir, file=sys.stderr)
    
    if args.code != '':
        args.mlb = mlb_from_eeee(args.code)
    if len(args.mlb) != 17:
        print('ERROR: Cannot use MLBs in non 17 character format!')
        sys.exit(1)

    # Handle different actions
    if args.action == 'download':
        return action_download(args)
    if args.action == 'selfcheck':
        return action_selfcheck(args)
    if args.action == 'verify':
        return action_verify(args)
    if args.action == 'guess':
        return action_guess(args)

    # If we reach here, it means action is 'download' and we need to continue with the download logic
    if args.catalogurl:
        su_catalog_url = args.catalogurl
    elif args.seedprogram:
        su_catalog_url = get_seed_catalog(args.seedprogram)
        if not su_catalog_url:
            print('Could not find a catalog url for seed program %s'
                  % args.seedprogram, file=sys.stderr)
            print('Valid seeding programs are: %s'
                  % ', '.join(get_seeding_programs()), file=sys.stderr)
            exit(-1)
    else:
        su_catalog_url = get_default_catalog()
        if not su_catalog_url:
            print('Could not find a default catalog url for this OS version.',
                  file=sys.stderr)
            exit(-1)

    # download sucatalog and look for products that are for macOS installers
    catalog = download_and_parse_sucatalog(
        su_catalog_url, args.workdir, ignore_cache=args.ignore_cache)
    product_info = os_installer_product_info(
        catalog, args.workdir, ignore_cache=args.ignore_cache)

    if not product_info:
        print('No macOS installer products found in the sucatalog.',
              file=sys.stderr)
        exit(-1)

    # display a menu of choices (some seed catalogs have multiple installers)
    print('%2s %14s %10s %8s %11s  %s'
          % ('#', 'ProductID', 'Version', 'Build', 'Post Date', 'Title'))
    for index, product_id in enumerate(product_info):
        print('%2s %14s %10s %8s %11s  %s' % (
            index + 1,
            product_id,
            product_info[product_id].get('version', 'UNKNOWN'),
            product_info[product_id].get('BUILD', 'UNKNOWN'),
            product_info[product_id]['PostDate'].strftime('%Y-%m-%d'),
            product_info[product_id]['title']
        ))

    answer = get_input(
        '\nChoose a product to download (1-%s): ' % len(product_info))
    try:
        index = int(answer) - 1
        if index < 0:
            raise ValueError
        product_id = list(product_info.keys())[index]
    except (ValueError, IndexError):
        print('Exiting.')
        exit(0)

    # download all the packages for the selected product
    replicate_product(
        catalog, product_id, args.workdir, ignore_cache=args.ignore_cache)

    # generate a name for the sparseimage
    volname = ('Install_macOS_%s-%s'
               % (product_info[product_id]['version'],
                  product_info[product_id]['BUILD']))
    sparse_diskimage_path = os.path.join(args.workdir, volname + '.sparseimage')
    if os.path.exists(sparse_diskimage_path):
        os.unlink(sparse_diskimage_path)

    # make an empty sparseimage and mount it
    print('Making empty sparseimage...')
    sparse_diskimage_path = make_sparse_image(volname, sparse_diskimage_path)
    mountpoint = mountdmg(sparse_diskimage_path)
    if mountpoint:
        # install the product to the mounted sparseimage volume
        success = install_product(
            product_info[product_id]['DistributionPath'],
            mountpoint)
        if not success:
            print('Product installation failed.', file=sys.stderr)
            unmountdmg(mountpoint)
            exit(-1)
        # add the seeding program xattr to the app if applicable
        seeding_program = get_seeding_program(su_catalog_url)
        if seeding_program:
            installer_app = find_installer_app(mountpoint)
            if installer_app:
                print("Adding seeding program %s extended attribute to app"
                      % seeding_program)
                xattr.setxattr(installer_app, 'SeedProgram',
                               seeding_program.encode("UTF-8"))
        print('Product downloaded and installed to %s' % sparse_diskimage_path)
        if args.raw:
            unmountdmg(mountpoint)
        else:
            # if --raw option not given, create a r/o compressed diskimage
            # containing the Install macOS app
            compressed_diskimagepath = os.path.join(
                args.workdir, volname + '.dmg')
            if os.path.exists(compressed_diskimagepath):
                os.unlink(compressed_diskimagepath)
            app_path = find_installer_app(mountpoint)
            if app_path:
                make_compressed_dmg(app_path, compressed_diskimagepath)
            # unmount sparseimage
            unmountdmg(mountpoint)
            # delete sparseimage since we don't need it any longer
            os.unlink(sparse_diskimage_path)

main()