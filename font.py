from util import img as uimg
from PIL import Image
PatternDef = [
    [[True]],
    [[True, True, True, False], [True, False, True, True]],
    [[True, False], [False, True]],
    [[True, False, False, False], [False, False, True, False]],
    [[True, False, False, False], [False]*4,
        [False, False, True, False], [False]*4],
    [[True, False, False, False, False, False, False, False], [False]*8,
        [False, False, False, False, True, False, False, False], [False]*8]
]

letterImg = Image.open("style/letter.png")


def GetCoordIter(Size):
    import itertools as it
    c = [list(x)for x in map(range,Size)]
    return it.product(*c)

def applyPatter(img, patter=2):
    rImg = img.copy()
    transparent = (0,)*4
    myPat = PatternDef[patter]
    patterSize =(min([len(x) for x in myPat]),len(myPat))

    for coor in GetCoordIter(rImg.size):
        pc = [c%p for c,p in zip(coor,patterSize)]
        if not (myPat[pc[1]][pc[0]]):
            rImg.putpixel(coor,transparent)
        
    return rImg

def GetBaseLetterImg(index=0):
    letterSize = 5
    left = index*letterSize
    bbox = (left,0,left+letterSize,letterSize)
    lt = letterImg.crop(bbox)
    lt = lt.crop(lt.getbbox())
    nt = Image.new('RGBA', (letterSize,letterSize), color=(0, 0, 0, 0))
    uimg.PasteCenter(lt,nt)
    return nt

def ScaleCenter(img,size=(5,5)):
    nt = Image.new('RGBA', size, color=(0,)*4)
    scale = min([f//i for f,i in zip(size,img.size)])
    size_resize = tuple([x*scale for x in img.size])
    rImage = img.resize(size_resize)
    uimg.PasteCenter(rImage,nt)
    return nt

def GetLetter(txt="a",size=(5,5),pattern=0):
    baseLetter = ord("A")
    letterIndex = ord(txt.upper()[0])-baseLetter
    img = GetBaseLetterImg(letterIndex)
    img = ScaleCenter(img,size)
    return applyPatter(img,pattern)

def Test():
    from execution import Launcher
    
    def TestLetter(letter):
        r = GetLetter(letter,(100,100),0)
        s = Image.new("RGBA",r.size,(255,255,0,255))
        s.alpha_composite(r)
        uimg.Save(s,"testLetter",path="letters/",isTemp=True)
    
    Launcher.Launch(TestLetter,"Z")


if __name__ == "__main__":
    Test()