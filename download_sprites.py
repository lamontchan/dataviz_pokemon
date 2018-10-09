#!/usr/bin/python
import re
import os
import sys
import requests
import shutil

'''
Downloads pokemon sprites from generation 1-7 from pokemondb
'''

# download pokemon sprite
# sprites from https://img.pokemondb.net/sprites/x-y/normal/<poke_name>.png
def download_image(name):
    try:
        name.decode('ascii')
    except UnicodeEncodeError:
        print "Not an ASCII-encoded string"
    else:
        url = 'https://img.pokemondb.net/sprites/x-y/normal/%s.png' % name.lower() # xy sprite
        url_sm = "https://img.pokemondb.net/sprites/sun-moon/dex/normal/%s.png" % (name.lower()) # sun moon sprite
        img = "data/sprites/%s.png" % name.lower()
        print "saving %s to %s" % (url, img)

        # check xy sprite; then sun-moon
        r = requests.get(url)
        if r.status_code == 200:
            with open(img, 'wb') as f:
                f.write(r.content)
        else:
            r_sm = requests.get(url_sm)
            if r_sm.status_code == 200:
                with open(img, 'wb') as f:
                    f.write(r_sm.content)
            else:
                print "could not download image from %s or %s. Error: %s" % (url, url_sm, r.status_code)
                return 1
    return 0

# get all pokemon names
def get_pokemon_names():

    names = []
    URL = 'https://pokemondb.net/sprites' # sprites from this location
    r = requests.get(URL)
    if r.status_code == 200:
        for line in r.text.split("\n"):
            if 'sprites' in line.strip():
                poke_line = line.split('<a class="infocard"')
                for poke in poke_line:
                    r_match = re.match(r'(.*?)data-src="(.*?)" data-alt="(.*?) icon"', poke)
                    if r_match:
                        # download sprite
                        sprite_link = r_match.group(2)
                        name = r_match.group(3)
                        names.append(name)
    return names


if __name__ == "__main__":

    names = get_pokemon_names()
    for name in names:
        #exceptions
        name = name.replace('\'','') # farfetch'd
        name = name.replace('. ','-') # mr. mime
        name = re.sub(r' (.*)','', name) # various pokemon forms
        if 'tapu' in name.lower():
            name = name.replace(' ','-')
        
        # download sprites
        download_image(name)

    # pokemon names with exceptions
    exceptionNames = [  'nidoran-m', 
                        'nidoran-f', 
                        'flabebe', 
                        'oricorio-pom-pom', 
                        'lycanroc-midday',
                        'wishiwashi-school',
                        'type-null',
                        'minior-core',
                        'mr-mime',
                        'mime-jr',
                        'tapu-koko',
                        'tapu-lele',
                        'tapu-bulu',
                        'tapu-fini',
                    ]

    for name in exceptionNames:
        download_image(name)


