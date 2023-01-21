#!/usr/bin/env python3

BINDS = ['@am', '@attackmatrix']
CHANS = ['debug']
APIURL = {
    'attackmatrix':  {
        'url': 'http://149.210.137.179:8008/api',
        'details': 'https://www.valethosting.net/~penguin/attackmap/attackmap.php?q=explore',
    }
}
CONTENTTYPE = 'application/json'
MAXRESULTS = 4
HELP = {
    'DEFAULT': {
        'args': None,
        'desc': 'Query an AttackMatrix API instance for information on actors, techniques, tools, etc. For '
                'more information about `AttackMatrix`, visit https://github.com/uforia/AttackMatrix.'
    },
    'search': {
        'args': '<keyword1> <keyword2> ... <keyword#>',
        'desc': 'Find all entries (Actors, TTPs, etc.) that contain any of the given keyword(s) (logical OR). '
                'Useful for finding the correct MITRE ATT&CK names (e.g. T1574, G0064, S0008) for followup '
                'queries.',
    },
    'mitre': {
        'args': '<mitreid>',
        'desc': 'Return detailed information about an Actor/TTP. MITRE ATT&CK ID notation is required, e.g. '
        '`... mitre T1574.001`. Valid MITRE ATT&CK IDs are of the type: `Actor`, `Malware`, `Mitigation`, '
        '`Subtechnique`, `Tactic`, `Technique` and `Tool`. You can use the `search` feature to determine '
        'the correct IDs.',
    },
    'actoroverlap': {
        'args': '<actor1> <actor2> ... <actord#>',
        'desc': 'Check what TTPs overlap between the given actors. At least two actors must be given, '
        'in MITRE ATT&CK notation, e.g.: `... actoroverlap G0064 G0050 G0008`.',
    },
    'ttpoverlap': {
        'args': '<ttp1> <ttp2> ... <ttp3>',
        'desc': 'Check what actors share the given TTPs. At least two TTPs must be given,'
        'in MITRE ATT&CK notation, e.g.: `... ttpoverlap T1078 T1588.002 S0002 S0008`.',
    },
}
