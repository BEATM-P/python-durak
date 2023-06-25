import logic

class Tests:
    def settings():
        obj= logic.settings()
        print("Check these values with config.ini\n")
        print(obj.trump())
        print(obj.deck())
        print(obj.tickRate())
        print(obj.dbg())



if __name__=="__main__":
    Tests.settings()