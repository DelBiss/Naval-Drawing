class ImgPalette():
    
    def __init__(self,ColorList):
        import imgColor as ic
        self.colorlist = [ic.ImgColor(color, count)for color, count in ColorList]
        
    def __str__(self):
        return "\n".join([str(color) for color in self.colorlist])
    
    def GetImg(self,width,height):
        
        from PIL import Image
        self.colorlist.sort(key=lambda x: x.HSL.h)
        nbColor = len(self.colorlist)
        colorWidth = width//nbColor
        padding = (width-(colorWidth*nbColor))//2
        palette = [color.RGB.val for color in self.colorlist]
        
        firstLine = []
        for c in palette:
            firstLine = firstLine + ([c]*colorWidth)

        firstLine = ([palette[0]]*padding) + firstLine + ([palette[nbColor-1]]*padding)

        paletteIm = Image.new('RGBA', (width,height), color=(0,)*4)
        PaletteData = firstLine*height
        
        
        paletteIm.putdata(data=PaletteData)
        return paletteIm

def Test():
    import execution
    import util
    def Palette():
        colorlist = []
        for _ in range(5):
            colorlist.append([randomColor() for x in range(20)])
        #colorlist.append([((255,0,0),1)]+[randomColor() for x in range(10)]+[((0,0,255),1)])
        #util.CreateOutputPath()
        imgs = []
        
        for cl in colorlist:
            imgs.append(util.img.AddBorder(ImgPalette(cl).GetImg(96*2,30*2)))
        
        composite = util.img.ComposeImg(*imgs)
        util.img.Save(composite,"test","imgPalette/",True)
        
        pass

    def randomColor(): 
        import random
        from colormath.color_objects import HSLColor, sRGBColor
        from colormath.color_conversions import convert_color
        rCol = (random.randint(0, 360),random.randint(0, 100)/100.0,random.randint(0, 100)/100.0)
        
        return convert_color(HSLColor(*rCol), sRGBColor).get_upscaled_value_tuple() ,random.randint(0, 255)
    execution.Launcher.Launch(Palette)

if __name__ == "__main__":
    Test()