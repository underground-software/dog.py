#!/usr/bin/env python

from orbit import appver, messageblock, ROOT

def bytes8(s):
    return bytes(s, 'UTF-8')

def application(env, SR):
    SR('200 Ok', [('Content-Type', 'text/html')])
    res=''

    with open(ROOT + '/data/header', 'r') as f:
        res += f.read()
    res += '<h1>Woof!</h1>'
    res += messageblock([('appver', appver())])
    return 
