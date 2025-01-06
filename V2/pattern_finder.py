import mine_field as mf
import numpy as np
from sklearn.cluster import DBSCAN

import numpy as np

def _find_densest_zone_1D(values, zone_size) -> int:
    start = min(values)
    end = max(values)
    hist = [0] * (end - start + 1)

    if len(hist) <= zone_size:
        blank = zone_size - len(hist)
        return start - blank // 2

    for v in values:
        hist[v - start] += 1

    m = 0
    i = -1
    
    for j in range(len(hist) - zone_size + 1):
        s = sum(hist[j:j+zone_size])

        if s > m:
            m = s
            i = j

    return start + i
    

def _find_densest_zone(points, zone_size) -> tuple[int, int]:
    x = _find_densest_zone_1D(tuple(p[0] for p in points), zone_size)
    y = _find_densest_zone_1D(tuple(p[1] for p in points), zone_size)
    return (x, y)

def find_pattern(field: mf.MineField) -> list[tuple[int, int]]:
    data = np.array([(p.x, p.y) for p in field.points()])
    eps = field.pattern_size / 2.5
    dbscan = DBSCAN(eps=eps, min_samples=7)
    labels = dbscan.fit_predict(data)

    clusters = [[] for _ in range(max(labels) + 1)]

    for label, point in zip(labels, data):
        if label == -1:
            continue

        clusters[label].append(point)
    
    return [_find_densest_zone(cluster, field.pattern_size) for cluster in clusters]
