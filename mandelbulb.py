from numpy import zeros
from numpy import sin
from numpy import cos
from numpy import arctan
from numpy import arccos
from numpy import sqrt
from numpy import power

ColorList = [0, 8, 7, 15, 14, 1, 4, 5, 13, 3, 9, 11, 10, 2, 6, 12]

inputs = (
    ("Parameter", (8, 4, 100)),
)

def perform(level, box, options):
    param = options["Parameter"]
    
    width = box.maxx - box.minx
    height = box.maxy - box.miny
    depth = box.maxz - box.minz

    for dx in xrange(width):
        x = dx * 2.0 / width - 1.0
        for dy in xrange(height):
            y = dy * 2.0 / width - 1.0
            for dz in xrange(depth):
                z = dz * 2.0 / depth - 1.0

                iterations = -1
                C = (x, y, z)
                Z = (0, 0, 0)

                while r(Z) < 1000 and iterations < 21:
                    Z = add(exp(Z, param), C)
                    iterations = iterations + 1

                if iterations < 21 and iterations >= 5:
                    level.setBlockAt(box.minx + dx, box.miny + dy, box.minz + dz, 35)
                    level.setBlockDataAt(box.minx + dx, box.miny + dy, box.minz + dz, ColorList[iterations-5])

    level.markDirtyBox(box)    

def exp(v, n):
    t = theta(v)
    p = phi(v)

    k = power(r(v), n)

    return (k*sin(n*t)*cos(n*p), k*sin(n*t)*sin(n*p), k*cos(n*t))

def r((x, y, z)):
    return sqrt(x*x + y*y + z*z)

def phi((x, y, z)):
    return arctan(y/(x+0.000001))

def theta((x, y, z)):
    return arccos(z/(r((x, y, z)) + 0.0000001))

def add((x1, y1, z1), (x2, y2, z2)):
    return (x1+x2, y1+y2, z1+z2)
