# Feel free to modify and use this filter however you wish. If you do,
# please give credit to SethBling.
# http://youtube.com/SethBling

from pymclevel import TAG_Compound
from pymclevel import TAG_Int
from pymclevel import TAG_Short
from pymclevel import TAG_Byte
from pymclevel import TAG_String
from pymclevel import TAG_Float
from pymclevel import TAG_Double
from pymclevel import TAG_List

def perform(level, box, options):
    for x in range(box.minx, box.maxx):
        for y in range(box.miny, box.maxy):
            for z in range(box.minz, box.maxz):
                if level.blockAt(x, y, z) == 54:
                    createShop(level, x, y, z)

def createShop(level, x, y, z):
    chest = level.tileEntityAt(x, y, z)
    if chest == None:
        return

    priceList = {}
    saleList = {}
    profession = 0
    riches = 0

    for item in chest["Items"]:
        slot = item["Slot"].value
        if slot >= 0 and slot <= 8:
            priceList[slot] = item
        elif slot >= 9 and slot <= 17:
            saleList[slot-9] = item
        elif slot == 18:
            if item["id"].value == 35:
                dmg = item["Damage"].value
                if dmg == 12:
                    profession = 0 #brown villager
                elif dmg == 0:
                    profession = 1 #white villager
                elif dmg == 2 or dmg == 6 or dmg == 10 or dmg == 14:
                    profession = 2 #purple villager
                elif dmg == 15 or dmg == 7:
                    profession = 3 #black apron villager
                elif dmg == 8:
                    profession = 4 #white apron villager
                elif dmg == 5 or dmg == 13:
                    profession = 5 #green villager
        else:
            riches += item["Count"].value #other slots are used to count towards the "riches" total

    villager = TAG_Compound()
    villager["OnGround"] = TAG_Byte(1)
    villager["Air"] = TAG_Short(300)
    villager["AttackTime"] = TAG_Short(0)
    villager["DeathTime"] = TAG_Short(0)
    villager["Fire"] = TAG_Short(-1)
    villager["Health"] = TAG_Short(20)
    villager["HurtTime"] = TAG_Short(0)
    villager["Age"] = TAG_Int(0)
    villager["Profession"] = TAG_Int(profession)
    villager["Riches"] = TAG_Int(riches)
    villager["FallDistance"] = TAG_Float(0)
    villager["id"] = TAG_String("Villager")
    villager["Motion"] = TAG_List()
    villager["Motion"].append(TAG_Double(0))
    villager["Motion"].append(TAG_Double(0))
    villager["Motion"].append(TAG_Double(0))
    villager["Pos"] = TAG_List()
    villager["Pos"].append(TAG_Double(x + 0.5))
    villager["Pos"].append(TAG_Double(y))
    villager["Pos"].append(TAG_Double(z + 0.5))
    villager["Rotation"] = TAG_List()
    villager["Rotation"].append(TAG_Float(0))
    villager["Rotation"].append(TAG_Float(0))

    villager["Offers"] = TAG_Compound()
    villager["Offers"]["Recipes"] = TAG_List()
    for i in range(9):
        if i in priceList and i in saleList:
            offer = TAG_Compound()
            offer["buy"] = priceList[i]
            offer["sell"] = saleList[i]
            villager["Offers"]["Recipes"].append(offer)

    level.setBlockAt(x, y, z, 0)

    chunk = level.getChunk(x / 16, z / 16)
    chunk.Entities.append(villager)
    chunk.TileEntities.remove(chest)
    chunk.dirty = True
