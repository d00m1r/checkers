from field import *

def main():
    root = Tk()
    root.title("Checkers")
    app = Field(root)
    app.pack()
    root.mainloop()

if __name__ == '__main__':
    main()