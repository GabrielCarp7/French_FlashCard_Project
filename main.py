from tkinter import *
import pandas
import random
import os

words_list = {}


try:
    data = pandas.read_csv("unknown_words.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("french_words.csv")
    words_list = original_data.to_dict(orient="records")
else:
    words_list = data.to_dict(orient="records")

word_chosen = ""


# Functions for Buttons
def right_button():
    global word_chosen, flip_timer
    window.after_cancel(flip_timer)
    word = random.choice(words_list)
    word_chosen = word["English"]
    canvas.itemconfig(language, text="French", fill="black")
    canvas.itemconfig(text, text=word["French"], fill="black")
    canvas.itemconfig(canvas_image, image=card_front)
    flip_timer = window.after(3000, func=change_card)

    # Deleting the word that is known to user

    try:
        words_list.remove(word)
    except pandas.errors.EmptyDataError:
        os.remove("unknown_words.csv")
    else:
        data = pandas.DataFrame(words_list)
        data.to_csv("unknown_words.csv", index=False)


def wrong_button():
    global word_chosen, flip_timer
    window.after_cancel(flip_timer)
    word = random.choice(words_list)
    word_chosen = word["English"]
    canvas.itemconfig(language, text="French", fill="black")
    canvas.itemconfig(text, text=word["French"], fill="black")
    canvas.itemconfig(canvas_image, image=card_front)
    flip_timer = window.after(3000, func=change_card)


def change_card():
    canvas.itemconfig(language, text="English", fill="white")
    canvas.itemconfig(text, text=word_chosen, fill="white")
    canvas.itemconfig(canvas_image, image=card_back)


# UI Creation

window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, background="#B1DDC6")

# After a delay of 3 sec or 3000 ms change the card to english
flip_timer = window.after(3000, func=change_card)

# Implementing the images
tick = PhotoImage(file="images/right.png")
wrong = PhotoImage(file="images/wrong.png")
card_back = PhotoImage(file="images/card_back.png")
card_front = PhotoImage(file="images/card_front.png")

# Canvas Creation >> French Card
canvas = Canvas(width=800, height=526, background="#B1DDC6", highlightthickness=0)
canvas_image = canvas.create_image(400, 263, image=card_front)
language = canvas.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"))  # text="French"
text = canvas.create_text(400, 263, text="word", font=("Ariel", 60, "bold"))  # text=french_words[POSITION]
canvas.grid(column=0, row=0, columnspan=2)

# Buttons
check_button = Button(text="", image=tick, background="#B1DDC6", highlightthickness=0, command=right_button)
check_button.grid(column=1, row=1)

x_button = Button(text="", image=wrong, background="#B1DDC6", highlightthickness=0, command=wrong_button)
x_button.grid(column=0, row=1)

right_button()

window.mainloop()
