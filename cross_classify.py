import itertools

import numpy

ALLOWED_RATIO = 0.6


def cross_classify(source1, source2):
    if len(source1) > 0 and len(source2) > 0:
        validated1, validated2 = numpy.ndarray(shape=(0,4)), numpy.ndarray(shape=(0,4))
        mids1 = calc_mids(source1)
        mids2 = calc_mids(source2)
        for r1, m1 in itertools.izip(source1, mids1):
            for r2, m2 in itertools.izip(source2, mids2):
                if cross_valid(r1, m1, r2, m2):
                    validated1 = numpy.vstack([validated1, r1])
                    validated2 = numpy.vstack([validated2, r2])
        return validated1.astype(int), validated2.astype(int)
    else:
        return source1, source2


def cross_valid(rect1, mid1, rect2, mid2):
    size = (avg_rect_side(rect1) + avg_rect_side(rect2)) / 2.0
    dist = numpy.linalg.norm(numpy.array(mid1) - numpy.array(mid2))
    return dist < size * ALLOWED_RATIO


def avg_rect_side(rect):
    (x, y, w, h) = rect
    return (w + h) / 2.0


def calc_mids(rects):
    return [(int(ex + ew / 2.0), int(ey + eh / 2.0)) for (ex, ey, ew, eh) in rects]
