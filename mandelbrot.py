from numpy import zeros

ColorList = [0, 8, 7, 15, 14, 1, 4, 5, 13, 3, 9, 11, 10, 2, 6, 12]

def perform(level, box, options):
    width = box.maxx - box.minx
    depth = box.maxz - box.minz

    for dx in xrange(width):
        x = dx * 4.0 / width - 2.0
        for dz in xrange(depth):
            z = dz * 4.0 / depth - 2.0

            iterations = 0
            C = (x, z)
            Z = (0, 0)

            while complexAbs(Z) < 2 and iterations < 15:
                Z = complexAdd(complexMult(Z, Z), C)
                iterations = iterations + 1

            level.setBlockAt(box.minx + dx, box.miny, box.minz + dz, 35)
            level.setBlockDataAt(box.minx + dx, box.miny, box.minz + dz, ColorList[iterations])

    level.markDirtyBox(box)

def complexAbs((r, i)):
    return r*r+i*i

def complexMult((r1, i1), (r2, i2)):
    return (r1*r2 - i1*i2, r1*i2 + r2*i1)

def complexAdd((r1, i1), (r2, i2)):
    return (r1+r2, i1+i2)
