from tkinter import *
import tkinter.ttk as ttk

mainWindow = Tk()

root = ttk.Notebook(mainWindow, height=480, width=720)

featuredPage = ttk.Frame(root)
searchPage = ttk.Frame(root)
addByURL = ttk.Frame(root)
forums = ttk.Frame(root)
profile = ttk.Frame(root)
settings = ttk.Frame(root)

featuredTitle = ttk.Label(featuredPage, text="Featured", font=("Roboto", 32)).pack()

featuredPage.pack(fill=BOTH, expand=True)
searchPage.pack(fill=BOTH, expand=True)
addByURL.pack(fill=BOTH, expand=True)
forums.pack(fill=BOTH, expand=True)
profile.pack(fill=BOTH, expand=True)
settings.pack(fill=BOTH, expand=True)

root.add(featuredPage, text="Featured")
root.add(searchPage, text="Search")
root.add(addByURL, text="Add by URL")
root.add(forums, text="Forums")
root.add(profile, text="Profile")
root.add(settings, text="Settings")

root.pack(expand=True, fill=BOTH)
mainWindow.mainloop()