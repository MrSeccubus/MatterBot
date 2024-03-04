#!/usr/bin/env python3

BINDS = ['@docgen']
CHANS = ['debug']
CONTENTTYPE = 'application/json'
APIURL = {
    'docgen':   {
        'url': '<your WikiJS instance\'s URL here>',
        'key': '<your WikiJS\' API token here>',
    },
}
HELP = {
    'DEFAULT': {
        'args': '<lang> <casenumber> or <upload>',
        'desc': 'Generate a new composite PDF document in language `lang` for case number `casenumber`. E.g.: `@docgen en_US memo 2023041101`.\nWith the `upload` feature, the module will take the accompanying image attachment(s) and convert it/them to Base64 blobs on Wiki page(s) (with an optional title) for easy inclusion in other documents.',
    },
}
TEMPLATECASES = 'Template Cases'
TEMPLATEIDCHAIN = 'Template ID Chain'
TEMPLATECUSTOMERS = 'Template Customers'
# Set your default language
DEFAULTLOCALE = "en_US"
# Set your template directory
TEMPLATEDIR = "my_fancy_business_template/"
# Map the template entries to files
LANGMAP = {
    'en_US': {
        'toc': TEMPLATEDIR+"toc_en.html",
        'css': TEMPLATEDIR+"your_css.css",
        'header': TEMPLATEDIR+"header_en.html",
        'footer': TEMPLATEDIR+"footer_en.html",
        'titlebreak': TEMPLATEDIR+"titlebreak_en.html",
        'pagebreak': TEMPLATEDIR+"titlebreak_en.html",
    },
}