import pprint
pp = pprint.PrettyPrinter(indent=4).pprint

def CreateOutputPath(path="temp/", isTemp=False):
    import os
    if isTemp:
        path = "temp/" + path

    outPath = "output/"+path
    os.makedirs(os.path.dirname(outPath+"test.bmp"), exist_ok=True)
    return outPath

class img():
    @staticmethod
    def ComposeImg(*args, IsV = True,SpaceBetween=5):
        import itertools
        from PIL import Image
        addedSpace = (SpaceBetween*(len(args)-1))
        if IsV:
            width = max([x.size[0] for x in args])
            height = sum([x.size[1] for x in args])+addedSpace
            
            xpos = itertools.accumulate([(width-x.size[0])//2 for x in args])
            ypos = itertools.accumulate([0]+[x.size[1]+SpaceBetween for x in args])
            
        else:
            width = sum([x.size[0] for x in args])+addedSpace
            height = max([x.size[1] for x in args])

            xpos = itertools.accumulate([0]+[x.size[0]+SpaceBetween for x in args])
            ypos = itertools.accumulate([(height-x.size[1])//2 for x in args])
            

        pos = list(zip(xpos,ypos))
        resultIm = Image.new('RGBA', (width,height), color=(255,255,255,255))
        #print("Compose Result: ", resultIm)
        for index, img in enumerate(args):
            #print("Compose Img #{} @".format(index),pos[index], img)
            resultIm.alpha_composite(img,pos[index])
        
        return resultIm
    
    @staticmethod
    def Center(ObjSize, CanvasSize):
        return tuple(map(lambda obj, canvas: (canvas-obj)//2, ObjSize, CanvasSize))

    @staticmethod
    def PasteCenter(Source,Dest):
        centerPos = img.Center(Source.size, Dest.size)
        Dest.paste(Source,centerPos)

    @staticmethod   
    def AddBorder(Img, borderSize=1, fillcolor=(0,0,0,255)):
        from PIL import ImageOps
        
        #NewSize =tuple([ x+(borderSize*2) for x in Img.size])
        #BorderedIm = Image.new('RGBA', NewSize, color=(0,0,0,255))
        #img.PasteCenter(Img,BorderedIm)
        return ImageOps.expand(Img, borderSize, fillcolor) #BorderedIm
    
    @staticmethod
    def GetTxtImg(txt, size, txtColor=(0,0,0,255),bgcolor=(255,)*4):
        from PIL import Image, ImageDraw, ImageFont
        im = Image.new('RGBA', size, color=bgcolor)
        draw = ImageDraw.Draw(im)
        fnt = ImageFont.truetype('style/GoogleSans-Regular.ttf', size[1]//2)
        txtSize = draw.textsize(txt, font=fnt)
        txtPos = img.Center(txtSize, size)
        draw.text(txtPos, txt, font=fnt, fill=txtColor)
        return im

    @staticmethod
    def Save(aPic,filename, dpi=(300, 300),path="temp/", isTemp=False, ext="png", border=10):
        outpath = CreateOutputPath(path, isTemp)
        outputPath = "{}{}.{}".format(outpath,filename,ext)
        aPic2 = img.AddBorder(aPic,border, (255,)*3)
        outMsg = "Image save @ {}, with {} border".format(outputPath,border)
        aPic2.save(outputPath,dpi=dpi)
        print(outMsg)
        