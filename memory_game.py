import tkinter as tk
import random

# ================= WINDOW =================
root = tk.Tk()
root.title("Memory Puzzle Game")
root.state("zoomed")

def exit_fullscreen(event):
    root.state("normal")

root.bind("<Escape>", exit_fullscreen)

# ================= BACKGROUND =================
canvas = tk.Canvas(root)
canvas.pack(fill="both", expand=True)

colors = ["#1e3c72", "#2a5298", "#ff7e5f", "#feb47b"]
color_index = 0

def animate_bg():
    global color_index
    canvas.configure(bg=colors[color_index])
    color_index = (color_index + 1) % len(colors)
    root.after(2000, animate_bg)

animate_bg()

# ================= GAME FRAME =================
frame = tk.Frame(canvas, bg="white", bd=5, relief="ridge")
frame.place(relx=0.5, rely=0.5, anchor="center", width=700, height=700)

# ================= VARIABLES =================
symbols = ["🍎","🍌","🍇","🍒","🍉","🥝","🍍","🍑"]
cards = []
buttons = []
first = None
second = None
lock = False
time_left = 60
matches = 0
timer_id = None   # 🔥 important fix

# ================= TIMER =================
timer_label = tk.Label(frame, text="", font=("Arial", 22, "bold"), bg="white")
timer_label.grid(row=0, column=0, columnspan=4, pady=10)

def update_timer():
    global time_left, timer_id

    if time_left > 0:
        time_left -= 1
        timer_label.config(text=f"⏱ Time: {time_left}s")
        timer_id = frame.after(1000, update_timer)
    else:
        game_over()

# ================= HOVER =================
def on_enter(e):
    if e.widget["state"] == "normal":
        e.widget.config(bg="#add8e6")

def on_leave(e):
    if e.widget["state"] == "normal":
        e.widget.config(bg="#d3d3d3")

# ================= ANIMATION =================
def flip_animation(btn):
    for size in range(5, 25, 2):
        frame.after(size * 5, lambda s=size: btn.config(font=("Arial", s)))

# ================= CLICK =================
def on_click(btn, index):
    global first, second, lock

    if lock or btn["text"] != "?":
        return

    btn.config(text=cards[index], bg="#90ee90")
    flip_animation(btn)

    if not first:
        first = (btn, index)
    else:
        second = (btn, index)
        lock = True
        frame.after(700, check_match)

# ================= MATCH =================
def check_match():
    global first, second, lock, matches

    btn1, i1 = first
    btn2, i2 = second

    if cards[i1] == cards[i2]:
        btn1.config(bg="#4CAF50", state="disabled")
        btn2.config(bg="#4CAF50", state="disabled")
        matches += 1

        if matches == 8:
            win_game()
    else:
        btn1.config(text="?", bg="#d3d3d3")
        btn2.config(text="?", bg="#d3d3d3")

    first = None
    second = None
    lock = False

# ================= STATES =================
def game_over():
    for btn in buttons:
        btn.config(state="disabled")
    timer_label.config(text="❌ Game Over!")

def win_game():
    for btn in buttons:
        btn.config(state="disabled")
    timer_label.config(text="🎉 You Won!")

# ================= START / RESTART =================
def start_game():
    global cards, buttons, first, second, time_left, matches, timer_id

    # 🔥 STOP OLD TIMER
    if timer_id:
        frame.after_cancel(timer_id)

    # Remove old buttons only (keep timer + restart)
    for btn in buttons:
        btn.destroy()

    buttons.clear()

    # Reset variables
    cards = symbols * 2
    random.shuffle(cards)

    first = None
    second = None
    time_left = 60
    matches = 0
    lock = False

    timer_label.config(text=f"⏱ Time: {time_left}s")

    # Create cards
    for i in range(16):
        btn = tk.Button(frame, text="?", font=("Arial", 20),
                        bg="#d3d3d3",
                        command=lambda i=i: on_click(buttons[i], i))

        btn.grid(row=1 + i//4, column=i%4, sticky="nsew", padx=5, pady=5)

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

        buttons.append(btn)

    # Grid resize
    for i in range(4):
        frame.grid_rowconfigure(i+1, weight=1)
        frame.grid_columnconfigure(i, weight=1)

    update_timer()

# ================= RESTART BUTTON =================
restart_btn = tk.Button(frame, text="🔄 Restart", font=("Arial", 14),
                        bg="#ffcc00", command=start_game)
restart_btn.grid(row=5, column=0, columnspan=4, pady=10)

# ================= RUN =================
start_game()
root.mainloop()