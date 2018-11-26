


class Test():
        
    def __init__(self):

        import execution
        import imgColor
        import imgPalette

        self.test={}
        self.test[imgPalette.__name__] = imgPalette.Test
        self.test[execution.__name__] = execution.Test
        self.test[imgColor.__name__] = imgColor.Test

    def Launch(self):
        menu = []
        menu.append("░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░")
        menu.append("Select a test to be executed:")
        for i,k in enumerate(self.test.keys()):
            menu.append("  {} - {}".format(i,k))
        menu.append("  {} - {}".format(len(self.test),"All Test"))
        #menu.append("▐▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅█░░░")
        menu.append("░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░")
        print("\n".join(menu))
        xString = (input("Enter a test: "))

        

        try:
            val = min(len(self.test),int(xString)) 
        except ValueError:
            val = 0

        if val >= len(self.test):
            for fct in self.test.values():
                fct()
        else:
            list(self.test.values())[val]()
        
        pass
    #execution.Launcher.Launch(All_Test)
    #imgPalette.Test()
    
if __name__ == "__main__":
    Test().Launch()
    
    