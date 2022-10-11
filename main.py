from tkinter import *
import tkinter.messagebox
import pandas as pd
from random import randint
import winsound

# global constants and variables

BACKGROUND_COLOR = "#B1DDC6"
timer = 5
word_index = 0
words_dataframe = None
data_loaded = False
round_live = True
started = False


# functions

def load_data_button_function():
    global timer
    global started
    if data_loaded:
        if tkinter.messagebox.askokcancel("Data Loaded", "Data is already loaded. "
                                                         "Reload data? Your progress will be lost"):
            timer = 0
            started = False
            load_data()
    else:
        load_data()


def load_data():
    global words_dataframe
    global data_loaded
    try:
        words_dataframe = pd.read_csv("./data/spanish_words_saved.csv")
        tkinter.messagebox.showinfo("Success", "Data loaded successfully")
    except FileNotFoundError:
        tkinter.messagebox.showinfo("New Data", "No data found, new data file created")
        words_dataframe = pd.read_csv("./data/spanish_words.csv")
        words_dataframe.to_csv("./data/spanish_words_saved.csv", index=False)
    finally:
        data_loaded = True


def error_sound():
    winsound.PlaySound("SystemExit", winsound.SND_ALIAS | winsound.SND_ASYNC)


def start_game_button_function():
    global started
    if data_loaded:
        if not started:
            started = True
            main_game_function()
        else:
            error_sound()
    else:
        tkinter.messagebox.showinfo("No Data", "Please load data")


def main_game_function():
    if len(words_dataframe) == 0:
        tkinter.messagebox.showinfo("Error", "There are no more flash cards!")
    else:
        start_game()
        count_down()


def green_tick_function():
    global round_live
    if started:
        if round_live:
            error_sound()
        else:
            round_live = True
            words_dataframe.drop(index=word_index, inplace=True)
            words_dataframe.reset_index(inplace=True, drop=True)
            main_game_function()
    else:
        error_sound()


def red_tick_function():
    global round_live
    if started:
        if round_live:
            error_sound()
        else:
            round_live = True
            main_game_function()
    else:
        error_sound()


def start_game():
    global word_index
    if data_loaded:
        word_index = randint(0, len(words_dataframe)-1)
        random_word_es = words_dataframe.at[word_index, "Spanish"]
        card_canvas.itemconfig(image_container, image=card_front_image)
        card_canvas.itemconfig(language_text, text="español")
        card_canvas.itemconfig(word_text, text=random_word_es)


def count_down():
    global timer
    card_canvas.itemconfig(timer_text, text=timer)
    if timer > 0:
        timer -= 1
        window.after(1000, count_down)
    else:
        card_canvas.itemconfig(timer_text, text="")
        timer = 5
        flip_card()


def flip_card():
    global round_live
    random_word_en = words_dataframe.at[word_index, "English"]
    card_canvas.itemconfig(image_container, image=card_back_image)
    card_canvas.itemconfig(language_text, text="English")
    card_canvas.itemconfig(word_text, text=random_word_en)
    round_live = False


def save_and_quit_function():
    if tkinter.messagebox.askokcancel("Quit?", "Are you sure you wish to quit?"):
        if data_loaded:
            words_dataframe.to_csv("./data/spanish_words_saved.csv", index=False)
            window.destroy()
        else:
            window.destroy()


# GUI below

window = Tk()
window.title("Flash Me")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

card_front_image = PhotoImage(file="./images/card_front.png")
card_back_image = PhotoImage(file="./images/card_back.png")
tick_image = PhotoImage(file="./images/right.png")
cross_image = PhotoImage(file="./images/wrong.png")

card_canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
image_container = card_canvas.create_image(400, 263, image=card_front_image)
language_text = card_canvas.create_text(400, 160, text="español", font=("helvetica", "30", "italic"))
word_text = card_canvas.create_text(400, 263, text="", font=("helvetica", "30"))
timer_text = card_canvas.create_text(700, 426, text="", font=("helvetica", "30"))
card_canvas.grid(row=0, column=0, columnspan=3)

tick_button = Button(width=100, height=100, bg=BACKGROUND_COLOR, image=tick_image, bd=0, command=green_tick_function)
tick_button.grid(row=1, column=0)

cross_button = Button(width=100, height=100, bg=BACKGROUND_COLOR, image=cross_image, bd=0, command=red_tick_function)
cross_button.grid(row=1, column=2)

load_data_button = Button(width=20, height=3, text="Load Data", command=load_data_button_function)
load_data_button.grid(row=2, column=0, pady=(40, 0))

start_game_button = Button(width=20, height=3, text="Start Game", command=start_game_button_function)
start_game_button.grid(row=2, column=1, pady=(40, 0))

save_and_quit_button = Button(width=20, height=3, text="Save and Quit", command=save_and_quit_function)
save_and_quit_button.grid(row=2, column=2, pady=(40, 0))

window.mainloop()
