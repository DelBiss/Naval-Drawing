import util
from PIL import Image, ImageDraw, ImageFont

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


def CreateLineAcross(img, p, fillColor=(0,)*3, width=1, pattern=0, IsVertical=False):
    if IsVertical:
        LineLenght = img.size[1]
    else:
        LineLenght = img.size[0]
    
    pixelLines = []
    baseLines = []
    basePattern = PatternDef[pattern]
    for linePattern in basePattern:
        baseLines.append(
            (linePattern*((LineLenght//len(linePattern))+1))[:LineLenght])

    pixelLines = (baseLines*((width//len(baseLines))+1))[:width]

    basePos = p

    for pos1, pl in enumerate(pixelLines):
        for pos2, pv in enumerate(pl):
            if pv:
                if IsVertical:
                    finalPos = (basePos+pos1, pos2)
                else:
                    finalPos = (pos2, basePos+pos1)

                img.putpixel(finalPos, fillColor)

def GetGrid(gridDimension=(55, 70), lineColor=(0,)*3, Pattern=0, title="Grid", pageProportion=(1, 1), mainLine=[[{"test":lambda x: False}]]):
    maxSize = (int(2400*pageProportion[0]), int(3000*pageProportion[1]))
    borderSize = 5
    Width = 2

    gridSize = min([x[0]//x[1] for x in zip(maxSize, gridDimension)])
    gridImgSize = tuple(map(lambda x: x * gridSize, gridDimension))
    grid = Image.new('RGBA', gridImgSize, color=(255, 255, 255, 255))

    if len(mainLine) == 1:
        mainLine = mainLine*2

    for ori, d in enumerate(gridDimension):
        
            
        for i in range(1, d):
            stop = i*gridSize
            l_pattern = Pattern
            l_width = Width
            l_lineColor = lineColor
            for mainL in mainLine[ori]:
                if mainL["test"](i):
                    if "pattern" in mainL:
                        l_pattern = mainL["pattern"]
                    if "width" in mainL:
                        l_width = mainL["width"]
                    if "color" in mainL:
                        l_lineColor = mainL["color"]
            CreateLineAcross(grid, stop, l_lineColor, l_width, l_pattern, IsVertical = ori == 0)


    grid = util.img.AddBorder(grid, borderSize)

    if len(title) > 0:
        t1 = util.img.GetTxtImg(title, (grid.size[0], 100))
        grid = util.img.ComposeImg(t1, grid)
    return grid   # im#im


def Test():

    from execution import Launcher
    def FullGrid():
        col_black = (0,)*3
        col_grey = (127,)*3
        pattern  ="pattern"
        width = "width"
        color = "color"
        #lineColor=(0,)*3,Pattern=0 == pattern, width, color test mainLine
        mainLine = [{   "test": lambda x: True,
            pattern:4,
            width:4,
            color: col_grey,},
        {   "test": lambda x: x%5 == 0,
            pattern:3,
            width:4,
            color: col_grey,},
        {   "test": lambda x: x%10 == 0,
            pattern:3,
            width:4,
            color: col_black,}]
        full = GetGrid(title="", mainLine=[mainLine])
        util.img.Save(full, "FullGrid", (300, 300), "grid/", True, border=0)
        pass

    def NoTest():
        patternRange = range(6)
        allImg = []
        resizePattern = 5
        mainLine = [lambda x: x%4==0]
        for p in patternRange:
            patImg = []
            for c in [("Black", (0,)*3, (127,)*3), ("Grey", (127,)*3, (0,)*3)]:
                l = "{} - pattern {}".format(c[0], p)

                #grid = util.img.ComposeImg(t1,grid)
                grid = GetGrid((12, 12), c[1], p, "", (1/2, 1/3),mainLine=mainLine)
                t1 = util.img.GetTxtImg(l, (grid.size[0]//2, 100))
                im1 = Image.new(
                    'RGBA', ((grid.size[0]//2)//resizePattern, 80//resizePattern), (255,)*4)
                CreateLineAcross(im1, 0, c[1], 80//resizePattern, p)
                im1 = im1.resize(
                    (im1.size[0]*resizePattern, im1.size[1]*resizePattern))
                im1 = util.img.AddBorder(im1, 1, c[2])
                t1 = util.img.ComposeImg(t1, im1, IsV=False)
                grid = util.img.ComposeImg(t1, grid)
                patImg.append(grid)
            #im2 = GetGrid((12, 12), (127,)*3, p,"Grey - pattern {}".format(p),(1/2,1/3))
            allImg.append(util.img.ComposeImg(*patImg, IsV=False))
        full = util.img.ComposeImg(*(allImg))
        #full = util.img.AddBorder(full,100,(255,255,255,255))
        util.img.Save(full, "DifGrid", (300, 300), "grid/", True)

    def Line_Test():
        
        fillColor = (127,)*3
        #widthRange = range(5)
        patternRange = range(6)
        allImg = []
        for p in patternRange:
            im1 = Image.new('RGBA', (10, 10), (255,)*4)
            im2 = Image.new('RGBA', (10, 10), (255,)*4)
            CreateLineAcross(im1, 0, (0,)*3, 10, p)
            CreateLineAcross(im2, 0, fillColor, 10, p)
            imr1 = im1.resize((im1.size[0]*3, im1.size[1]*3))
            imr2 = im2.resize((im2.size[0]*3, im2.size[1]*3))
            im1 = util.img.AddBorder(im1, 1, fillColor)
            imr1 = util.img.AddBorder(imr1, 1, fillColor)
            im2 = util.img.AddBorder(im2, 1)
            imr2 = util.img.AddBorder(imr2, 1)
            im1 = util.img.ComposeImg(imr1, im1, IsV=False)
            im2 = util.img.ComposeImg(imr2, im2, IsV=False)
            allImg.append(util.img.ComposeImg(im1, im2))
        full = util.img.ComposeImg(*(allImg))
        util.img.Save(full, "LineTest", (300, 300), "grid/", True, border=0)

    Launcher.Launch(FullGrid)
    if False:
        Launcher.Launch(NoTest)
        Launcher.Launch(Line_Test)


if __name__ == "__main__":
    Test()
