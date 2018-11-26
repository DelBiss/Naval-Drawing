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
    def ComposeImg(*args, IsV = True):
        import itertools
        from PIL import Image
        if IsV:
            width = max([x.size[0] for x in args])
            height = sum([x.size[1] for x in args])
            
            xpos = itertools.accumulate([(width-x.size[0])//2 for x in args])
            ypos = itertools.accumulate([0]+[x.size[1] for x in args])
            
        else:
            width = sum([x.size[0] for x in args])
            height = max([x.size[1] for x in args])

            xpos = itertools.accumulate([0]+[x.size[0] for x in args])
            ypos = itertools.accumulate([(height-x.size[1])//2 for x in args])
            

        pos = list(zip(xpos,ypos))
        resultIm = Image.new('RGBA', (width,height), color=(255,255,255,255))

        for index, img in enumerate(args):
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
    def AddBorder(Img, borderSize=1):
        from PIL import Image
        NewSize =tuple([ x+(borderSize*2) for x in Img.size])
        BorderedIm = Image.new('RGBA', NewSize, color=(0,0,0,255))
        img.PasteCenter(Img,BorderedIm)
        return BorderedIm

    @staticmethod
    def Save(aPic,filename, dpi=(300, 300),path="temp/", isTemp=False, ext="png"):
        outpath = CreateOutputPath(path, isTemp)
        outputPath = "{}{}.{}".format(outpath,filename,ext)
        
        outMsg = "Image save @ {}".format(outputPath)
        aPic.save(outputPath,dpi)
        print(outMsg)
        