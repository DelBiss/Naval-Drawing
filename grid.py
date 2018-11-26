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

    basePattern = PatternDef[pattern]
    baseLines = []
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

    pass


def GetGrid(gridDimension=(26, 30), lineColor=(0,)*3, Pattern=0):
    maxSize = (2400, 3000)
    borderSize = 5
    gridSize = min([x[0]//x[1] for x in zip(maxSize, gridDimension)])
    gridImgSize = tuple(map(lambda x: x * gridSize, gridDimension))
    grid = Image.new('RGB', gridImgSize, color=(255, 255, 255))

    Width = 2
    for i in range(1, gridDimension[0]):
        left = i*gridSize
        CreateLineAcross(grid, left, lineColor, Width, Pattern, True)

    for i in range(1, gridDimension[1]):
        top = i*gridSize
        CreateLineAcross(grid, top, lineColor, Width, Pattern, False)

    return util.img.AddBorder(grid, borderSize)  # im#im


def Test():

    from execution import Launcher

    def NoTest():
        patternRange = range(6)
        for p in patternRange:
            util.img.Save(GetGrid((55, 70), (0,)*3, p), "gridTest{}".format(p))

    def Line_Test():
        import itertools
        distanceBetween = 20
        fillColor = (128,)*3
        widthRange = range(5)
        patternRange = range(6)
        all_line = list(itertools.product(patternRange, widthRange))
        print("Drawing {} lines".format(len(all_line)))
        im = Image.new('RGB', (distanceBetween*(len(all_line)+2),)*2, (255,)*3)
        for isV in [False, True]:
            for i, v in enumerate(all_line):
                p, w = v
                CreateLineAcross(im, (i+1)*distanceBetween,
                                 fillColor, w+1, p, isV)
        util.img.Save(im, "LineTest")
    Launcher.Launch(NoTest)


if __name__ == "__main__":
    Test()
