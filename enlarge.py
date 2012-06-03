# Enlarge Filter by SethBling
# Feel free to modify and reuse, but credit to SethBling would be nice.
# http://youtube.com/sethbling

inputs = (
    ("Scale Factor", (4, 1, 256)),
    ("Center on", ("Exact center",
                   "Bottom center",
                   )),
)

def perform(level, box, options):
    sf = options["Scale Factor"]
    centerOn = options["Center on"]

    blocks = [[[]]]
    dmg = [[[]]]

    centerX = (box.minx + box.maxx - 1) / 2.0
    centerZ = (box.minz + box.maxz - 1) / 2.0
    if centerOn == "Exact center":
        centerY = (box.miny + box.maxy - 1) / 2.0
    elif centerOn == "Bottom center":
        centerY = box.miny

    width = box.maxx - box.minx
    height = box.maxy - box.miny
    depth = box.maxz - box.minz
    
    for x in xrange(width):
        blocks.append([])
        dmg.append([])
        for y in xrange(height):
            blocks[x].append([])
            dmg[x].append([])
            for z in xrange(depth):
                blocks[x][y].append(level.blockAt(box.minx + x, box.miny + y, box.minz + z))
                dmg[x][y].append(level.blockDataAt(box.minx + x, box.miny + y, box.minz + z))

    if len(blocks) == 0:
        return

    for x in xrange(width):
        for y in xrange(height):
            for z in xrange(depth):
                dx = x + 0.5 - width / 2.0
                if centerOn == "Exact center":
                    dy = y + 0.5 - height / 2.0
                elif centerOn == "Bottom center":
                    dy = y
                dz = z + 0.5 - depth / 2.0

                dx = dx * sf
                dy = dy * sf
                dz = dz * sf

                px = centerX + dx
                py = centerY + dy
                pz = centerZ + dz

                hsf = sf / 2.0

                if centerOn == "Exact center":
                    miny = int(py - hsf + 1)
                    maxy = int(py + hsf + 1)
                elif centerOn == "Bottom center":
                    miny = py
                    maxy = py + sf

                for bx in xrange(int(px - hsf + 1), int(px + hsf + 1)):
                    for by in xrange(miny, maxy):
                        for bz in xrange(int(pz - hsf + 1), int(pz + hsf + 1)):
                            level.setBlockAt(bx, by, bz, blocks[x][y][z])
                            level.setBlockDataAt(bx, by, bz, dmg[x][y][z])
                            chunk = level.getChunk(bx / 16, bz / 16)
                            chunk.dirty = True

