#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pylast
import sys
from artistnode import ArtistNode

API_KEY = "your-api-key"
API_SECRET ="your-api-secret"

class LastGraph:
    '''so this acts like a dict with keys equal to artist MBIDs.
       each value ALSO acts like a dict with keys equal to artist MBIDs (the
       value of which will be edge weights).
       '''

    def __init__(self):
        self.__fetched_artist_nodes = dict()
        self.__network = pylast.get_lastfm_network(api_key = API_KEY,
                                                   api_secret = API_SECRET)

    def key_for_band_name(self, band_name):
        try:
            artist = self.__network.get_artist(band_name)
        except Exception as e:
            sys.stderr('ERROR (%s)! Trying again...\n' % e)
            artist = self.__network.get_artist(band_name)
        #if artist.get_mbid() not in self.__fetched_artist_nodes:
        #    self.__fetch_artist(artist.get_mbid())
        return artist.get_mbid()

    def clear(self): self.__fetched_artist_nodes.clear()

    def copy(self):
        import copy
        return copy.copy(self)

    def keys(self): return self.__fetched_artist_nodes.keys()

    def items(self): return self.__fetched_artist_nodes.items()

    def values(self): return self.__fetched_artist_nodes.values()

    def __iter__(self):
        def iterfn():
            for it in self.keys():
                yield it
        return iterfn()

    def __getitem__(self, key):
        if key not in self.__fetched_artist_nodes:
            self.__fetch_artist(key)
        return self.__fetched_artist_nodes[key]

    def __setitem__(self, key, item):
        '''will print warning to stderr if called. Probably
           shouldn't be!
           '''
        sys.stderr.write(
            'WARNING! LastGraph.__setitem__ called with (%s, %s)\n' %
            (key, value))
        self.__fetched_artist_nodes[key] = item

    def __fetch_artist(self, mbid):
        print('fetching artist %s...' % mbid)
        try:
            artist = self.__network.get_artist_by_mbid(mbid)
        except Exception as e:
            sys.stderr.write('ERROR (%s)! Trying again...\n' % e)
            artist = self.__network.get_artist_by_mbid(mbid)
        print(' success! got artist %s!' % artist.get_name())
        self.__fetched_artist_nodes[mbid] = ArtistNode(self, artist)


if __name__ == '__main__':
    import dijkstra
    g = LastGraph()
    k = g.key_for_band_name('radiohead')
    for x in g[k]:
        print(g[k][x])

