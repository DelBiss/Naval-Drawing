from enum import Enum
import colormath.color_objects as color_obj

class Color(Enum):
    XYZ = color_obj.XYZColor
    RGB = color_obj.sRGBColor
    LAB = color_obj.LabColor
    HSV = color_obj.HSVColor
    HSL = color_obj.HSLColor


class ColorSpace():

    def __init__(self, colorClass, ImgColor=None):

        from colormath.color_conversions import _RGB_CONVERSION_DICT_TEMPLATE as Conv_Path

        clrcls = Color[colorClass].value
        className = clrcls.__name__

        if className in Conv_Path:
            from colormath.color_conversions import convert_color
            path_to_conv = [Color.RGB.value]
            #print("We need to do convertion to reach", className)

            path_to_conv = path_to_conv + \
                [c.target_type for c in Conv_Path[className]]
            convFrom = Color(path_to_conv[len(path_to_conv)-2]).name

            source_value = getattr(ImgColor, convFrom)
            self.colormath = convert_color(source_value.colormath, clrcls)
        else:
            #print("Creating RGB object.")
            self.colormath = clrcls(*ImgColor._RGB[:3])
            self.val = tuple([int(x*255)for x in ImgColor._RGB[:3]])
        self.value = self.colormath.get_value_tuple()
        band_dict = {
            band[band.find("_")+1]: band for band in self.colormath.VALUES}
        self.__dict__.update({myK: self.colormath.__dict__[
                             cmK] for myK, cmK in band_dict.items()})

    def __str__(self):
        return str(self.colormath)


class ImgColor():
    def __init__(self, RGB, count=0, colorSpace= Color.RGB, applyAlpha = False):
        self.original = RGB
        self.nb = count
        self.SetColor(RGB, colorSpace)

        if applyAlpha == True:
            self.ApplyAlpha()

    def SetColor(self, RGB, colorSpace= Color.RGB):
        #print("Setting Color:", RGB, "Max:", max(RGB))
        for ck in Color.__members__.keys():
            if ck in self.__dict__:
                del self.__dict__[ck]

        if max(RGB) > 1:
            #print("normalizing")
            RGB = [x/255 for x in RGB]

        self._RGB = RGB
        self.alpha = 1
        if len(RGB) == 4:
            self.alpha = RGB[3]

    def ApplyAlpha(self):
        #print("Applying Alpha. Current:", self.alpha, "on", self.RGB.value)
        if self.alpha < 1:
            
            self.SetColor([(band*self.alpha)+((1-self.alpha))
                           for band in self.RGB.value])

    def __getattr__(self, name):
        if name in Color.__members__:

            self.__dict__[name] = ColorSpace(name, self)
            return self.__dict__[name]

        else:
            print("Trying to asses an attribute:", name)
            raise AttributeError
    
    def __str__(self):
        return str(self.RGB)


def Test():


    from execution import Launcher
    def randomColor(): 
        import random
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    def ImgColor_Convertion(color, count=0):
        print(color)
        #print("\nCreating 'A'")
        a = ImgColor(color, count,True)
        #print("\nCreating 'C'")
        c = ImgColor(color, count)
        
        print (c)
        print (a)

    Launcher.Launch(ImgColor_Convertion, randomColor())


if __name__ == "__main__":    
    Test()
    
    
