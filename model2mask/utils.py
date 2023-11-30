import functools
import math

import numpy as np
import pandas as pd

from scipy import optimize


def parse_top_bottom(model: pd.DataFrame):

    # Check that the model actually contains an even number of countours
    if not len(model.contour_id.unique()) % 2 == 0:
        raise ValueError(
            'The supplied input model has an odd number of contours')

    # Check the contours have 2 points each:
    for contour in model.contour_id.unique():
        if not len(model[model.contour_id == contour].index) == 2:
            raise ValueError(
                f'Contour {contour} has {len(model[model.contour_id== contour].index)} points.')

    # For each contour pair, check which one is top and which one is bottom
    # Output only xyz coordintes

    points_top = []
    points_bottom = []

    for contour_pair in model.contour_id.unique()[::2]:

        subset1 = model[model.contour_id == contour_pair]
        subset2 = model[model.contour_id == (contour_pair + 1)]

        if subset1.z[0] > subset2.z[0] and subset1.z[1] > subset2.z[1]:
            points_top.append([subset1.x[0], subset1.y[0], subset1.z[0]])
            points_top.append([subset1.x[1], subset1.y[1], subset1.z[1]])

            points_bottom.append([subset2.x[0], subset2.y[0], subset2.z[0]])
            points_bottom.append([subset2.x[1], subset2.y[1], subset2.z[1]])

        else:
            points_bottom.append([subset1.x[0], subset1.y[0], subset1.z[0]])
            points_bottom.append([subset1.x[1], subset1.y[1], subset1.z[1]])

            points_top.append([subset2.x[0], subset2.y[0], subset2.z[0]])
            points_top.append([subset2.x[1], subset2.y[1], subset2.z[1]])

    return points_top, points_bottom


def fit_plane(points: []):
    # inspired by https://stackoverflow.com/questions/20699821/find-and-draw-regression-plane-to-a-set-of-points/

    points = np.array(points)

    fun = functools.partial(error, points=points)
    params0 = [0, 0, 0]
    res = optimize.minimize(fun, params0)

    a = res.x[0]
    b = res.x[1]
    c = res.x[2]
    
    return a,b,c


def plane(x, y, params):
    a = params[0]
    b = params[1]
    c = params[2]
    z = a*x + b*y + c
    return z


def error(params, points):
    result = 0
    for (x, y, z) in points:
        plane_z = plane(x, y, params)
        diff = abs(plane_z - z)
        result += diff**2
    return result


def cross(a, b):
    return [a[1]*b[2] - a[2]*b[1],
            a[2]*b[0] - a[0]*b[2],
            a[0]*b[1] - a[1]*b[0]]


def angle(a1, b1, c1, a2, b2, c2):
    d = (a1*a2 + b1*b2 + c1*c2)
    e1 = math.sqrt(a1*a1 + b1*b1 + c1*c1)
    e2 = math.sqrt(a2*a2 + b2*b2 + c2*c2)
    d = d / (e1*e2)
    A = math.degrees(math.acos(d))
    return A

def distance(a1, b1, c1, a2, b2, c2, x, y):
    z1 = plane(x, y, [a1, b1, c1])
    z2 = plane(x, y, [a2, b2, c2])
        
    return z1-z2
