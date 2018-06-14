# encoding=utf-8

from tkinter import *
from tkinter import ttk

import graph as chat_graph


def notice_video_id_entry(video_id):
	print(video_id)
	vid_val.set(video_id)
	chat_graph.plot(video_id)
	print("noticed")


def entry_video_id(event):
	video_id = video_id_entry.get()
	notice_video_id_entry(video_id)


def show_chat_freq_graph(event):
	chat_graph.display_graph()


def show_entry_popup(event):
	w = event.widget
	entry_right_click_popup.entryconfigure("Cut", command=lambda: w.event_generate("<<Cut>>"))
	entry_right_click_popup.entryconfigure("Copy", command=lambda: w.event_generate("<<Copy>>"))
	entry_right_click_popup.entryconfigure("Paste", command=lambda: w.event_generate("<<Paste>>"))
	entry_right_click_popup.tk.call("tk_popup", entry_right_click_popup, event.x_root, event.y_root)



root = Tk()
root.title(u"live_chat_heat graph viewer")
root.geometry("400x300")

content = ttk.Frame(root, padding="3 3 12 12")
content.grid(column=0, row=0, sticky=(N, W, E, S))
content.columnconfigure(0, weight=1)
content.rowconfigure(0, weight=1)


label = ttk.Label(content, text="v=")


vid_val = StringVar()
vid_label = ttk.Label(content, width=11, textvariable=vid_val)


entry_right_click_popup = Menu(root, tearoff=0)
entry_right_click_popup.add_command(label="Cut")
entry_right_click_popup.add_command(label="Copy")
entry_right_click_popup.add_command(label="Paste")


video_ids = StringVar()
video_id_entry = ttk.Entry(content, width=11, textvariable=video_ids)
video_id_entry.bind("<Button-3><ButtonRelease-3>", show_entry_popup)


Button = ttk.Button(content, text="Button")
Button.bind("<Button-1>", entry_video_id)


show_graph_btn = ttk.Button(content, text="Graph")
show_graph_btn.bind("<Button-1>", show_chat_freq_graph)


label.grid(column=1, row=1, sticky=E)
vid_label.grid(column=2, row=1, sticky=(W, E))
video_id_entry.grid(column=3, row=1, sticky=(W, E))
Button.grid(column=3, row=2, sticky=W)
show_graph_btn.grid(column=3, row=3, sticky=W)



for child in content.winfo_children(): child.grid_configure(padx=10, pady=15)

root.mainloop()

