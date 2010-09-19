#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pylast
import sys

class ArtistNode:
    '''This is a node in the graph. It acts like a dict mapping
       artist MBIDs to distances. That is, say we have ArtistNode v.
       Then v[w] will be the distance from v to w.

       The "dict" will NOT be populated at the time of creation of
       this object. It will instead be populated the first time
       keys(), items() values() or __getitem__() is called.

       The population of this dict basically means we call get_similar
       on the Artist at this particular node. If we did this at creation
       time, the population of a single node would cause an endless
       cascade of node population!
       '''

    MAX_SIMILAR_TO_FETCH = 10

    class Edge:
        EPSILON = 0.001
        def __init__(self, rhs_artist_node, similarity):
            self.__dest_artist = rhs_artist_node
            print('similarity: %f' % similarity)
            self.__similarity = similarity

        def get_dist(self):
            return 1.0 - self.__similarity + self.EPSILON

        def get_similarity(self):
            return self.__similarity

    def __init__(self, graph, artist):
        '''Artist is a pylast.Artist object.
        '''
        self.__artist = artist
        self.__have_gotten_similar = False
        self.__graph = graph
        self.__edges = dict()

    def get_name(self):
        return self.__artist.get_name()

    def get_similarity(self, other_mbid):
        return self.__edges[other_mbid].get_similarity()

    def clear(self): self.__edges.clear()

    def copy(self):
        import copy
        return copy.copy(self)

    def keys(self):
        if not self.__have_gotten_similar:
            self.__fetch_similar()
        return self.__edges.keys()

    def items(self):
        if not self.__have_gotten_similar:
            self.__fetch_similar()
        return [(x[0], x[1].get_dist()) for x in self.__edges.items()]

    def values(self):
        if not self.__have_gotten_similar:
            self.__fetch_similar()
        return [x.get_dist() for x in self.__edges.values()]

    def __iter__(self):
        def iterfn():
            for it in self.keys():
                yield it
        return iterfn()

    def __getitem__(self, key):
        if not self.__have_gotten_similar:
            self.__fetch_similar()
        return self.__edges[key].get_dist()

    def __setitem__(self, key, item):
        '''will print warning to stderr if called. Probably
           shouldn't be! In any case, will be Totally Inefficacious.
           '''
        sys.stderr.write(
            'WARNING! ArtistNode.__setitem__ called with (%s, %s)\n' %
            (key, value))
        sys.stderr.write('No action taken.\n')

    def __fetch_similar(self):
        print('fetching artists similar to %s...' % self.__artist.get_name())
        try:
            sims = self.__artist.get_similar(self.MAX_SIMILAR_TO_FETCH)
        except Exception as e:
            sys.stderr.write('ERROR (%s)! Trying again...\n' % e)
            sims = self.__artist.get_similar(self.MAX_SIMILAR_TO_FETCH)
        print('success! Got %d similar artists.' % len(sims))
        for similar_item in sims:
            if similar_item.item.get_mbid() is None:
                sys.stderr.write(
                    'ERROR: artist %s has MBID of NoneType. Continuing on...\n' %
                    similar_item.item.get_name().encode("utf-8"))
                continue
            other_artistnode = self.__graph[similar_item.item.get_mbid()]
            self.__edges[similar_item.item.get_mbid()] = self.Edge(other_artistnode,
                                                              similar_item.match)
        self.__have_gotten_similar = True


