# encoding=utf-8

import concurrent.futures as futures

from tkinter import *
from tkinter import ttk

import graph as chat_graph

executor = futures.ThreadPoolExecutor()
future = None


# window button actions
def close_window():
	root.destroy()

# entry mouse actions
def show_entry_popup(event):
	w = event.widget
	entry_right_click_popup.entryconfigure("Cut", command=lambda: w.event_generate("<<Cut>>"))
	entry_right_click_popup.entryconfigure("Copy", command=lambda: w.event_generate("<<Copy>>"))
	entry_right_click_popup.entryconfigure("Paste", command=lambda: w.event_generate("<<Paste>>"))
	entry_right_click_popup.tk.call("tk_popup", entry_right_click_popup, event.x_root, event.y_root)


# button actions
def entry_video_id(event):
	video_id = video_id_entry.get()
	vid_val.set(video_id)
	global executor
	global future
	if future is None or future.done():
		future = executor.submit(chat_graph.plot, video_id)
		future.add_done_callback(callback_finished_scraping_task)
		running_state_val.set("Running now")
		running_state_label.config(background="red")

def show_chat_freq_graph(event):
	chat_graph.display_graph()

def cancel_action(event):
	pass

# future callback actions
def callback_finished_scraping_task(future):
	running_state_val.set("Runnable next")
	running_state_label.config(background="green")


root = Tk()
root.title(u"live_chat_heat graph viewer")
root.geometry("400x300")
root.protocol("WM_DELETE_WINDOW", close_window)

content = ttk.Frame(root, padding="3 4 12 12")
content.grid(column=0, row=0, sticky=(N, W, E, S))
content.columnconfigure(0, weight=1)
content.rowconfigure(0, weight=1)

# Label
label = ttk.Label(content, text="v=")

vid_val = StringVar()
vid_label = ttk.Label(content, width=14, textvariable=vid_val)

running_state_val = StringVar()
running_state_val.set("No running now")
running_state_label = ttk.Label(content, width=16, textvariable=running_state_val)

# Popup Menu
entry_right_click_popup = Menu(root, tearoff=0)
entry_right_click_popup.add_command(label="Cut")
entry_right_click_popup.add_command(label="Copy")
entry_right_click_popup.add_command(label="Paste")

# Entry
video_ids = StringVar()
video_id_entry = ttk.Entry(content, width=14, textvariable=video_ids)
video_id_entry.bind("<Button-3><ButtonRelease-3>", show_entry_popup)

# Button
left_clicked = "<Button-1><ButtonRelease-1>"
run_button = ttk.Button(content, text="Run")
run_button.bind(left_clicked, entry_video_id)

show_graph_btn = ttk.Button(content, text="Graph")
show_graph_btn.bind(left_clicked, show_chat_freq_graph)

cansel_button = ttk.Button(content, text="Cansel")
cansel_button.bind(left_clicked, cancel_action)

# Layout
# column = 1
label.grid(column=1, row=1, sticky=E)
# column = 2
vid_label.grid(column=2, row=1, sticky=(W, E))
running_state_label.grid(column=2, row=2, sticky=(W, E))
# column = 3
video_id_entry.grid(column=3, row=1, sticky=(W, E))
run_button.grid(column=3, row=2, sticky=W)
cansel_button.grid(column=3, row=3, sticky=W)
show_graph_btn.grid(column=3, row=4, sticky=W)


for child in content.winfo_children(): child.grid_configure(padx=15, pady=15)

root.mainloop()
