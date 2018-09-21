# encoding=utf-8

import concurrent.futures as futures

from tkinter import *
from tkinter import ttk

import graph as chat_graph
import scraping.live_chat_replay_scraper as chat_scraper

executor = futures.ThreadPoolExecutor()
future = None

chat_list = []
# create chat list window
def create_chat_list_window(event):
	window = Toplevel()
	window.title("Chat List")
	window.geometry("400x300")
	winfrm = ttk.Frame(window)
	winfrm.pack(fill='both', expand=True)

	columns = {}
	columns["time"] = "timestampText"
	columns["user"] = "authorName"
	columns["message"] = "message"
	chat_columns = tuple(columns.keys())
	tree = ttk.Treeview(winfrm, columns=chat_columns, show='headings')
	vsb = ttk.Scrollbar(winfrm, orient="vertical", command=tree.yview)
	hsb = ttk.Scrollbar(winfrm, orient="horizontal", command=tree.xview)
	tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
	tree.grid(column=0, row=0, sticky=(N, W, E, S))
	vsb.grid(column=1, row=0, sticky=(N, S))
	hsb.grid(column=0, row=1, sticky=(W, E))
	winfrm.grid_columnconfigure(0, weight=1)
	winfrm.grid_rowconfigure(0, weight=1)
	for col in chat_columns:
		w=len(col)*10
		tree.column(col, width=w)
		tree.heading(col, text=col)

	for chat in chat_list:
		record = tuple([chat.data[v] for v in columns.values()])
		try:
			tree.insert("", "end", tags=chat_columns, values=record)
		except Exception as e:
			pass

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
		future = executor.submit(chat_scraper.make_chat_list, video_id)
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
	global chat_list
	chat_list = future.result()
	chat_graph.set_chat_data(chat_list)
	if chat_graph.is_graph_drawable() :
		graph_drawable_state_val.set("Drawable")
		graph_drawable_state_label.config(background="green")


root = Tk()
root.title(u"live_chat_heat graph viewer")
root.geometry("400x300")
root.protocol("WM_DELETE_WINDOW", close_window)

content = ttk.Frame(root, padding="3 5 12 12")
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

graph_drawable_state_val = StringVar()
graph_drawable_state_val.set("Not drawable")
graph_drawable_state_label = ttk.Label(content, width=16, textvariable=graph_drawable_state_val)
graph_drawable_state_label.config(background="red")

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

create_chat_list_window_btn = ttk.Button(content, text="Show Chats")
create_chat_list_window_btn.bind(left_clicked, create_chat_list_window)

#cansel_button = ttk.Button(content, text="Cansel")
#cansel_button.bind(left_clicked, cancel_action)

# Layout
# column = 1
label.grid(column=1, row=1, sticky=E)
# column = 2
vid_label.grid(column=2, row=1, sticky=(W, E))
running_state_label.grid(column=2, row=2, sticky=(W, E))
graph_drawable_state_label.grid(column=2, row=4, sticky=(W, E))
# column = 3
video_id_entry.grid(column=3, row=1, sticky=(W, E))
run_button.grid(column=3, row=2, sticky=W)
#cansel_button.grid(column=3, row=3, sticky=W)
show_graph_btn.grid(column=3, row=4, sticky=W)
create_chat_list_window_btn.grid(column=3, row=5, sticky=W)

for child in content.winfo_children(): child.grid_configure(padx=15, pady=15)

root.mainloop()
