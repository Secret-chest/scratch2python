from tkinter import *
import tkinter.ttk as ttk

mainWindow = Tk()

style = ttk.Style()
style.configure("TLabel", foreground="#212121", background="#ffffff", font=("Roboto", 12))
style.configure("TNotebook", font=("Roboto", 16), background="#eeeeee")
style.configure("TNotebook.tab", font=("Comic Neue", 16), background="#eeeeee")
style.configure("TFrame", font=("Roboto", 16), background="#ffffff")
style.map("TNotebook.Tab", background=[("selected", "#ffffff")], foreground=[("selected", "#212121")]);
style.configure("TNotebook.Tab", background="#eeeeee", foreground="#212121", font=("Roboto", 12), borderwidth=0);
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
