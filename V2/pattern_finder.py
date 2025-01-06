import mine_field as mf
import numpy as np
from sklearn.cluster import DBSCAN

def find_pattern(field: mf.MineField):
    data = np.array([(p.x, p.y) for p in field.points()])
    eps = field.pattern_size / 2.5
    dbscan = DBSCAN(eps=eps, min_samples=7)
    labels = dbscan.fit_predict(data)
    return labels

