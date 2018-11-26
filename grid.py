import util
from PIL import Image, ImageDraw, ImageFont

def GetGrid(gridDimension=(26, 30), lineColor = (0,)*3):
    # gridDimension=(26,30)
    pageSize = (int(8.5*300),11*300)
    maxSize = (2400, 3000)
    letterLine = "EJPUZ"
    borderSize = 5
    gridSize = min([x[0]//x[1] for x in zip(maxSize, gridDimension)])
    gridImgSize = tuple(map(lambda x: x * gridSize, gridDimension))
    imgSize = tuple(map(lambda x: x + ((borderSize-1)*2), gridImgSize))
    print(gridSize)
    grid = Image.new('RGB', gridImgSize, color=(255, 255, 255))
    draw = ImageDraw.Draw(grid)
    #lineColor = (128+64,)*3
    for i in range(gridDimension[0]):
        left = i*gridSize
        right = ((i+1)*gridSize)-1
        draw.line((left, 0, left, gridImgSize[1]), fill=lineColor)
        if GetLetterAddress(i-1)[-1:] in letterLine:
            draw.line((left+1, 0, left+1, gridImgSize[1]), fill=lineColor)
        draw.line((right, 0, right, gridImgSize[1]), fill=lineColor)
        if GetLetterAddress(i)[-1:] in letterLine:
            draw.line((right-1, 0, right-1, gridImgSize[1]), fill=lineColor)
    for i in range(gridDimension[1]):
        top = i*gridSize
        bottom = ((i+1)*gridSize)-1
        draw.line((0, top, gridImgSize[0], top), fill=lineColor)
        if (i)%5 == 0:
            draw.line((0, top+1, gridImgSize[0], top+1), fill=lineColor)
        draw.line((0, bottom, gridImgSize[0], bottom), fill=lineColor)
        if (i+1)%5 == 0:
            draw.line((0, bottom-1, gridImgSize[0], bottom-1), fill=lineColor)

    fnt = ImageFont.truetype('style/GoogleSans-Regular.ttf', 50)
    for i in range(gridDimension[0]):
        for j in range(gridDimension[1]):
            
        
            txt = "{}{:02}".format(GetLetterAddress(i), j+1)
            #txt = "{:02}".format(j+1)
            txtSize = draw.textsize(txt, font=fnt)
            txtPos = util.img.Center(txtSize, (gridSize,)*2)
            txtPos = tuple(map(lambda ite, pos: (ite*gridSize)+pos, [i, j], txtPos))
            #draw.text(txtPos, txt, font=fnt, fill=(int(0.25*255),)*3)
        pass
    im = Image.new('RGB', imgSize, color=(0, 0, 0))
    im.paste(grid, util.img.Center(gridImgSize, imgSize))
    page = Image.new('RGB', pageSize, color=(255,)*3)
    page.paste(im, util.img.Center(imgSize, pageSize))
    draw = ImageDraw.Draw(page)
    txt = str(lineColor)
    txtSize = draw.textsize(txt, font=fnt)
    topGridPos = ((pageSize[1]-imgSize[1])//2)-(txtSize[1])-20
    txtPos = util.img.Center(txtSize, (pageSize[0],)*2)
    draw.text((txtPos[0],topGridPos), txt, font=fnt, fill=(int(0),)*3)
    return page#im




def GetLetterAddress(index, nbChar=2):
    base = 26
    startLetter = 65
    bReturn = ""
    
    while True:
        bReturn = chr((index % base)+startLetter) + bReturn
        if index < base:
            break
        else:
            index = index//base

    return ("A"*(nbChar-len(bReturn)))+bReturn


def Test():


    from execution import Launcher
    def NoTest():
        util.img.Save(GetGrid(),"gridTest")

    Launcher.Launch(NoTest, )


if __name__ == "__main__":    
    Test()