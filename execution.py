
class Executer():
    def __init__(self, character="#", TextSpliter="-", textW=40, spaceW=3, marginW=2):
        self.headerCharacter = character
        self.textWidth = 40
        self.spaceWidth = 3
        self.marginWidth = 2
        self.textSpliter = " " + TextSpliter + " "

    @property
    def lineWidth(self):
        return self.textWidth + (self.marginWidth*2)

    @property
    def fullWidth(self):
        return self.lineWidth + (self.spaceWidth*2)

    @property
    def Spacer(self):
        return self.headerCharacter * self.spaceWidth

    @property
    def Margin(self):
        return " " * self.marginWidth

    def GetTimeStamp(self):
        import datetime
        return "[{:%H:%M}]".format(datetime.datetime.now())
  
    def EmptyLine(self):
        print ("")
   
    def FullLine(self):
        print (self.headerCharacter*self.fullWidth)

    def SpacerLine(self):
        print(self.Spacer + " "*self.lineWidth + self.Spacer)

    def TextLine(self, t=""):
        _twf = "{width}.{width}".format(width=self.textWidth)
        _formatedText = ("{:"+_twf+"}").format(t)
        print(self.Spacer + self.Margin + _formatedText + self.Margin + self.Spacer)

    def TimeStampLine(self,t=""):
        self.TextLine(self.GetTimeStamp() + self.textSpliter + t)

    def Start(self, name=""):
        self.EmptyLine()
        self.FullLine()
        #self.SpacerLine()
        self.TextLine(name)
        #self.SpacerLine()
        #self.TextLine("START")
        self.EmptyLine()

    def End(self,name="",duration=0):
        self.EmptyLine()
        #self.TextLine("END")
        #self.TimeStampLine(name)

        if duration>0:
            self.TimeStampLine("Took {:.3f} seconds.".format(duration))
        else:
            self.TimeStampLine()

        #self.SpacerLine()
        self.FullLine()
        self.EmptyLine()

    def Launch(self,fct, *args):
        import time
        import inspect
        from os import path
        _start_time = time.time()
        caller_file = path.basename(inspect.stack()[1].filename)
        #caller_file = caller_file.split(("\\",))[-1:][0]
        headerTitle = "[{}]".format(caller_file) + self.textSpliter + fct.__name__
        
        self.Start(headerTitle)
        fct(*args)

        duration = time.time() - _start_time
        self.End(fct.__name__,duration)



Launcher = Executer()

def Test():

    def Test_Output_Formating():
        print("This is a TEST!!!!")
    
    
    Launcher.Launch(Test_Output_Formating)

if __name__ == "__main__":
    Test()