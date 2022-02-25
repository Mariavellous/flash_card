from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
FONT_NAME = "San Francisco Font"
current_card = {}
to_learn = {}

# Run the csv file with the list of words need to learn.
# See if this file exist
try:
# Read csv file using pandas and convert to dataframe
  data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError: #if the file doesn't exist, use original file
  original_data = pandas.read_csv("data/french_words.csv")
  to_learn = original_data.to_dict(orient="records")
else:
# Convert dataframe to dictionary, changing the orient parameters to have columns using "records"
  to_learn = data.to_dict(orient="records")


# When the ❌ button get clicked, this function happens.
def next_card():
  global current_card, flip_timer
# Needs to invalidate the original timer to start over
  window.after_cancel(flip_timer)
# randomize the word from the dictionary that was converted
  current_card = random.choice(to_learn)   #to_learn is a dictionary
  canvas.itemconfig(language_title, text="French", fill="black")
  canvas.itemconfig(vocab_word, text=current_card["French"], fill="black")
# Changes the front background to white
  canvas.itemconfig(card_background, image=front_img)
# After 3 sec, the card needs to flip to the English translation
  flip_timer = window.after(3000, func=flip_card)


# Show the equivalent word in English after 3 sec of idle
def flip_card():
# Change the card to a green color
  canvas.itemconfig(card_background, image=back_img)
# Change the title of the language to English
  canvas.itemconfig(language_title, text="English", fill="white")
# Change to the equivalent of the foreign word into English
  canvas.itemconfig(vocab_word, text=current_card["English"], fill="white")

# If the ✅ button is pressed, this function happens. It removes the current card from original list & create a new need to learn file
def is_known():
# remove the current card from the dictionary (list of words)
  to_learn.remove(current_card)
  print(len(to_learn))
# Save the vocab words need to learn to another file (dict to dataframe then to csv)
  data = pandas.DataFrame(to_learn)
  data.to_csv("data/words_to_learn.csv", index=False) #doesnt add the index, just the words
# This function randomized another word from the dictionary
  next_card()


# ------------------ Create a UI -----------------

window = Tk()
window.title("Flashy")
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)

# The card waits 3000 ms or 3 sec before the func happens
flip_timer = window.after(3000, func=flip_card)


# Place the front card canvas on the window
canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
front_img = PhotoImage(file="images/card_front.png")
back_img = PhotoImage(file="images/card_back.png")

# Create image expects (x,y, image=PhotoImage())
card_background = canvas.create_image(400, 263, image=front_img)
# Create text inside canvas
language_title = canvas.create_text(400, 150, text="Title", font=(FONT_NAME, 40, "italic"))
vocab_word = canvas.create_text(400, 263, text="word", font=(FONT_NAME, 60, "bold"))
# Position of the canvas on the window
canvas.grid(row=0, column=0, columnspan=2)

# Create the ❌ button image and its position on the window
x_image = PhotoImage(file="images/wrong.png")
x_button = Button(image=x_image, highlightthickness=0, command=next_card)
x_button.grid(column=0, row=1)

# Create the ✅ button image and its position on the window
check_image = PhotoImage(file="images/right.png")
check_button = Button(image=check_image, highlightthickness=0, command=is_known)
check_button.grid(column=1, row=1)

# Run the function the first time so that the first word comes up.
next_card()

# Keeps the window from staying open and not disappearing.
window.mainloop()

