from GUI import *

root = Tk()
app = GUI(master=root)
root.protocol("WM_DELETE_WINDOW", lambda: root.quit())
app.mainloop()
root.destroy()
