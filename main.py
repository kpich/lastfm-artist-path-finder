#!/usr/bin/python
# -*- coding: UTF-8 -*-

import dijkstra
from lastgraph import LastGraph

if __name__ == '__main__':
    g = LastGraph()
    path = dijkstra.shortestPath(g,
                                 g.key_for_band_name('david bowie'),
                                 g.key_for_band_name('vanilla ice'))
    for i in range(len(path) - 1):
        print('%s -> %s (%f%% similarity)' %
              (g[path[i]].get_name(),
               g[path[i+1]].get_name(),
               g[path[i]].get_similarity(path[i+1]) * 100))
