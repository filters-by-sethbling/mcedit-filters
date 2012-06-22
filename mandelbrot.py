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
            C = complex(x, z)
            Z = complex(0)

            while abs(Z) < 2 and iterations < 15:
                Z = Z*Z + C
                iterations += 1

            level.setBlockAt(box.minx + dx, box.miny, box.minz + dz, 35)
            level.setBlockDataAt(box.minx + dx, box.miny, box.minz + dz, ColorList[iterations])

    level.markDirtyBox(box)