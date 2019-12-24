from field import *

def main():
    root = Tk()
    root.geometry("820x840")#create root window
    app = Field(1, root)
    root.mainloop()


if __name__ == '__main__':
    main()