#!/usr/bin/env python3

import base64
import httpx
import json
import re
from pathlib import Path
try:
    from commands.malpedia import defaults as settings
except ModuleNotFoundError: # local test run
    import defaults as settings
    if Path('settings.py').is_file():
        import settings
else:
    if Path('commands/malpedia/settings.py').is_file():
        try:
            from commands.malpedia import settings
        except ModuleNotFoundError: # local test run
            import settings

async def process(connection, channel, username, params):
    if len(params)>0:
        params = params[0]
        headers = {
            'Content-Type': settings.CONTENTTYPE,
            'Authorization': 'apitoken %s' % (settings.APIURL['malpedia']['key'],),
        }
        try:
            hash_algo = None
            bytes = None
            filename = None
            result = {'messages': []}
            if re.search(r"^[A-Za-z0-9]{32}$", params):
                hash_algo = 'md5'
            elif re.search(r"^[A-Za-z0-9]{64}$", params):
                hash_algo = 'sha256'
            if hash_algo:
                apipath = 'get/sample/%s/zip' % (params,)
                async with httpx.AsyncClient(headers=headers) as session:
                    response = await session.get(settings.APIURL['malpedia']['url'] + apipath)
                    json_response = response.json()
                    if 'detail' in json_response:
                        # You don't have a registered account/API key to get samples!
                        if json_response['detail'] == 'Authentication credentials were not provided.':
                            return ("An error occured searching Malpedia: you need a registered account/API key to search for hashes!",)
                    elif 'zipped' in json_response:
                        # We found a sample!
                        filename = params
                        bytes = base64.b64decode(json_response['zipped'].encode())
                        text = 'Malpedia hash search for `%s`:\n' % (params,)
                    else:
                        text = "Malpedia hash search for `%s` returned no results." % (params,)
                    if filename and bytes:
                        result['messages'].append(
                            {'text': text, 'uploads': [{'filename': filename, 'bytes': bytes}]}
                        )
                    else:
                        result['messages'].append(
                            {'text': text}
                        )
                return result
            if re.search(r"^[A-Za-z0-9]+$", params):
                apipath = 'find/actor/%s' % (params,)
                async with httpx.AsyncClient(headers=headers) as session:
                    response = await session.get(settings.APIURL['malpedia']['url'] + apipath)
                    actors = response.json()
                apipath = 'find/family/%s' % (params,)
                async with httpx.AsyncClient(headers=headers) as session:
                    response = await session.get(settings.APIURL['malpedia']['url'] + apipath)
                    families = response.json()
                if actors:
                    items = {}
                    subtrees = ('Malwares', 'Subtechniques', 'Techniques', 'Tools')
                    for subtree in subtrees:
                        items[subtree] = set()
                    text = 'Malpedia actor search for `%s`:' % (params,)
                    for actor in actors:
                        actornames = []
                        actornames.append(actor['common_name'])
                        actornames.extend(actor['synonyms'])
                        # Now find the common tools this actor uses
                        text += '\n- Actor names/synonyms: `' + '`, `'.join(sorted(actornames, key=str.lower)) + '`'
                        for actorname in actornames:
                            if re.search(r"^G[0-9]{4}$", actorname):
                                async with httpx.AsyncClient(headers=headers) as session:
                                    response = await session.get(settings.APIURL['mitre']['url'] + 'Enterprise/Actors/' + actorname)
                                    mitre = response.json()
                                    if mitre:
                                        mitre = mitre['Enterprise']['Actors'][actorname]
                                        for subtree in subtrees:
                                            if not subtree in items:
                                                items[subtree] = list()
                                            if subtree in mitre:
                                                for mitrecode in sorted(mitre[subtree], key=str.lower):
                                                    name = mitre[subtree][mitrecode]['name']
                                                    link = '[' +  mitrecode + '](' + settings.APIURL['mitre']['url'] + 'Enterprise/' + subtree + '/' + mitrecode + ')'
                                                    description = mitre[subtree][mitrecode]['description'].split('. ')[0].split('\n')[0]
                                                    items[subtree].add((link, name, description))
                    for subtree in subtrees:
                        text += '\n  - ' + subtree + ':'
                        for link, name, description in sorted(items[subtree]):
                            text += '\n    - ' + link + ' `' + name + '`: ' + description
                    result['messages'].append({'text': text},)
                if families:
                    text = 'Malpedia malware search for `%s`:' % (params,)
                    for family in families:
                        malwarenames = []
                        malwarenames.append(family['name'])
                        malwarenames.extend(family['alt_names'])
                        entry = '`, `'.join(sorted(malwarenames, key=str.lower))
                        text += '\n- Malware family: `' + entry + '`'
                    result['messages'].append(
                        {'text': text},
                    )
                return result
        except Exception as e:
            return {'messages': [
                {'text': 'An error occurred searching Malpedia for `%s`:\nError: `%s`' % (params, str(e))},
            ]}
