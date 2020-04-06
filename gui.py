# To be GUI

import tkinter as tk

root = tk.Tk()

canvas = tk.Canvas(root, height = 700, width = 900, bg= "#263D42")
canvas.pack()

lu_frame = tk.Frame(root, bg="white")
lu_frame.place(relwidth=0.4, relheight=0.5)

lb_frame = tk.Frame(root, bg="green")
lb_frame.place(relwidth = 0.4, relheight = 0.5, rely = 0.5)


r_frame = tk.Frame(root, bg="red")
r_frame.place(relwidth = 0.6, relheight = 1, relx=0.4)

openfile = tk.Button(lb_frame, text="test", padx=10, pady=5, fg="white")
openfile.pack()


root.mainloop()


