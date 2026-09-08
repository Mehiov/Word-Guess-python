import random
from customtkinter import *
from tkinter import messagebox
from Word_Guess import load_words, process_guess


# ---------------- App ----------------

app = CTk()

app.title("Word Guess")
app.geometry("900x600")
app.minsize(800, 550)

set_appearance_mode("dark")
set_default_color_theme("blue")


# ---------------- Colors ----------------

BG_COLOR = "#151923"
PANEL_COLOR = "#1D2330"

CARD_COLOR = "#242B3A"
CARD_HOVER = "#3A4D70"

PRIMARY_COLOR = "#4F8CFF"
PRIMARY_HOVER = "#78A8FF"

SUCCESS_COLOR = "#42D392"
ERROR_COLOR = "#FF667A"

KEY_COLOR = "#293244"
KEY_HOVER = "#40557A"
KEY_DISABLED = "#171C26"
KEY_DISABLED_TEXT = "#596276"

TEXT_COLOR = "#F2F4F8"
SECONDARY_TEXT = "#A9B1C3"
MUTED_TEXT = "#737D91"


# ---------------- Fonts ----------------

FONT_TITLE = ("Bahnschrift", 42, "bold")
FONT_HEADING = ("Bahnschrift", 30, "bold")

FONT_BUTTON = ("Segoe UI", 16, "bold")
FONT_NORMAL = ("Segoe UI", 16)
FONT_SMALL = ("Segoe UI", 13)

FONT_WORD = ("Bahnschrift", 52, "bold")
FONT_KEY = ("Segoe UI", 17, "bold")


# ---------------- Variables ----------------

current_word = ""
game_state = {}
game_over = False


# =========================================================
# PAGE SWITCHING
# =========================================================

def show_categories():
    main_menu.pack_forget()
    choose_category.pack(fill="both", expand=True)


def show_game_page():
    choose_category.pack_forget()
    game_frame.pack(fill="both", expand=True)


def back_to_menu():
    choose_category.pack_forget()
    main_menu.pack(fill="both", expand=True)


# =========================================================
# RESULT POPUP
# =========================================================

def show_result_popup(result, word):
    """
    Shows a custom Win/Lose popup centered relative
    to the main application window.
    """

    popup_width = 470
    popup_height = 300

    # Make sure the main window position and size are current.
    app.update_idletasks()

    app_x = app.winfo_x()
    app_y = app.winfo_y()
    app_width = app.winfo_width()
    app_height = app.winfo_height()

    x = app_x + (app_width - popup_width) // 2
    y = app_y + (app_height - popup_height) // 2

    popup = CTkToplevel(app)

    popup.resizable(False, False)
    popup.configure(
        fg_color=BG_COLOR
    )

    popup.geometry(
        f"{popup_width}x{popup_height}+{x}+{y}"
    )

    popup.transient(app)

    # ---------------- Result ----------------

    if result == "win":

        popup.title("You Win!")

        icon_label = CTkLabel(
            popup,
            text="✓",
            font=("Bahnschrift", 42, "bold"),
            text_color=SUCCESS_COLOR
        )

        icon_label.pack(
            pady=(22, 2)
        )

        title_label = CTkLabel(
            popup,
            text="YOU WIN!",
            font=("Bahnschrift", 28, "bold"),
            text_color=SUCCESS_COLOR
        )

        title_label.pack(
            pady=(0, 8)
        )

        message_label = CTkLabel(
            popup,
            text="تبریک میگم!\nشما کلمه‌ی",
            font=("Segoe UI", 16),
            text_color=TEXT_COLOR,
            justify="center"
        )

        message_label.pack(
            pady=(0, 3)
        )

        word_label_popup = CTkLabel(
            popup,
            text=word.upper(),
            font=("Bahnschrift", 30, "bold"),
            text_color=TEXT_COLOR
        )

        word_label_popup.pack(
            pady=(0, 4)
        )

        completed_label = CTkLabel(
            popup,
            text="رو با موفقیت کامل کردین!",
            font=("Segoe UI", 16),
            text_color=TEXT_COLOR
        )

        completed_label.pack(
            pady=(0, 15)
        )

    else:

        popup.title("Game Over")

        icon_label = CTkLabel(
            popup,
            text="×",
            font=("Bahnschrift", 44, "bold"),
            text_color=ERROR_COLOR
        )

        icon_label.pack(
            pady=(20, 0)
        )

        title_label = CTkLabel(
            popup,
            text="GAME OVER",
            font=("Bahnschrift", 28, "bold"),
            text_color=ERROR_COLOR
        )

        title_label.pack(
            pady=(0, 8)
        )

        message_label = CTkLabel(
            popup,
            text="بازی تموم شد!\nکلمه‌ی درست این بود:",
            font=("Segoe UI", 16),
            text_color=TEXT_COLOR,
            justify="center"
        )

        message_label.pack(
            pady=(0, 4)
        )

        word_label_popup = CTkLabel(
            popup,
            text=word.upper(),
            font=("Bahnschrift", 30, "bold"),
            text_color=TEXT_COLOR
        )

        word_label_popup.pack(
            pady=(0, 18)
        )

    # ---------------- Close Button ----------------

    close_button = CTkButton(
        popup,
        text="CONTINUE",
        width=170,
        height=44,
        font=FONT_BUTTON,
        fg_color=PRIMARY_COLOR,
        hover_color=PRIMARY_HOVER,
        corner_radius=12,
        command=popup.destroy
    )

    close_button.pack(
        pady=(0, 15)
    )

    # Enter also closes the popup.
    popup.bind(
        "<Return>",
        lambda event: popup.destroy()
    )

    # Escape also closes the popup.
    popup.bind(
        "<Escape>",
        lambda event: popup.destroy()
    )

    # Make sure popup is in front.
    popup.update_idletasks()
    popup.lift()
    popup.focus_force()

    # Prevent interaction with the game until popup closes.
    popup.grab_set()

    popup.wait_window()


# =========================================================
# START GAME
# =========================================================

def start_game(filename):
    global current_word, game_state, game_over

    words = load_words(filename)
    current_word = random.choice(words)

    shown = ["-" for _ in current_word]

    game_state = {
        "word": current_word,
        "shown": shown,
        "max_attempts": len(current_word) + 1,
        "attempts": 0,
        "guessed_letters": set()
    }

    for button in keyboard_buttons.values():
        button.configure(
            state="normal",
            fg_color=KEY_COLOR,
            text_color=TEXT_COLOR
        )

    game_over = False

    shown_word = "  ".join(
        game_state["shown"]
    )

    word_label.configure(
        text=shown_word
    )

    message_label.configure(
        text="",
        text_color=SECONDARY_TEXT
    )

    attempts_label.configure(
        text=f"Attempts: 0 / {game_state['max_attempts']}"
    )

    guess_entry.delete(
        0,
        "end"
    )

    show_game_page()


# =========================================================
# BACK FROM GAME
# =========================================================

def play_again():

    answer = messagebox.askyesno(
        "Play Again",
        "Are you sure you want to leave this game\n"
        "and choose a new category?"
    )

    if answer:
        game_frame.pack_forget()
        choose_category.pack(
            fill="both",
            expand=True
        )


# =========================================================
# TUTORIAL
# =========================================================

def show_tutorial():

    tutorial = CTkToplevel(app)

    tutorial.title("How To Play")
    tutorial.resizable(False, False)
    tutorial.configure(
        fg_color=BG_COLOR
    )

    tutorial.transient(app)

    tutorial_width = 500
    tutorial_height = 350

    app.update_idletasks()

    app_x = app.winfo_x()
    app_y = app.winfo_y()
    app_width = app.winfo_width()
    app_height = app.winfo_height()

    x = app_x + (app_width - tutorial_width) // 2
    y = app_y + (app_height - tutorial_height) // 2

    tutorial.geometry(
        f"{tutorial_width}x{tutorial_height}+{x}+{y}"
    )

    current_page = [0]

    pages = [
        (
            "WELCOME!",
            "Welcome to Word Guess!\n\n"
            "Your goal is simple:\n"
            "Guess the hidden word before you run out of attempts."
        ),
        (
            "CHOOSE A CATEGORY",
            "First, choose a category.\n\n"
            "You can choose Animals, Objects, Food,\n"
            "Countries, or Random."
        ),
        (
            "GUESS A LETTER",
            "Enter one letter at a time.\n\n"
            "If the letter is in the word,\n"
            "it will be revealed."
        ),
        (
            "WRONG GUESS",
            "A wrong letter costs one attempt.\n\n"
            "Be careful — you only have a limited\n"
            "number of attempts!"
        ),
        (
            "WIN THE GAME!",
            "Reveal all the letters before you run\n"
            "out of attempts to win.\n\n"
            "Good luck!"
        )
    ]

    title_label = CTkLabel(
        tutorial,
        text="",
        font=("Bahnschrift", 28, "bold"),
        text_color=TEXT_COLOR
    )

    title_label.pack(
        pady=(22, 8)
    )

    text_label = CTkLabel(
        tutorial,
        text="",
        font=("Segoe UI", 18),
        text_color=SECONDARY_TEXT,
        justify="center"
    )

    text_label.pack(
        expand=True,
        pady=(0, 4)
    )

    navigation_frame = CTkFrame(
        tutorial,
        fg_color="transparent"
    )

    navigation_frame.pack(
        fill="x",
        padx=22,
        pady=(2, 18)
    )

    back_button = CTkButton(
        navigation_frame,
        text="BACK",
        width=130,
        height=44,
        font=("Segoe UI", 15, "bold"),
        fg_color=CARD_COLOR,
        hover_color=CARD_HOVER,
        text_color=TEXT_COLOR,
        corner_radius=11
    )

    back_button.pack(
        side="left"
    )

    page_label = CTkLabel(
        navigation_frame,
        text="",
        font=("Segoe UI", 16, "bold"),
        text_color=MUTED_TEXT
    )

    page_label.place(
        relx=0.5,
        rely=0.5,
        anchor="center"
    )

    next_button = CTkButton(
        navigation_frame,
        text="NEXT",
        width=130,
        height=44,
        font=("Segoe UI", 15, "bold"),
        fg_color=PRIMARY_COLOR,
        hover_color=PRIMARY_HOVER,
        text_color=TEXT_COLOR,
        corner_radius=11
    )

    next_button.pack(
        side="right"
    )

    def update_page():

        title, text = pages[current_page[0]]

        title_label.configure(
            text=title
        )

        text_label.configure(
            text=text
        )

        page_label.configure(
            text=f"Page {current_page[0] + 1} / {len(pages)}"
        )

        if current_page[0] == 0:
            back_button.configure(
                state="disabled"
            )
        else:
            back_button.configure(
                state="normal"
            )

        if current_page[0] == len(pages) - 1:
            next_button.configure(
                text="GOT IT"
            )
        else:
            next_button.configure(
                text="NEXT"
            )

    def next_page():

        if current_page[0] == len(pages) - 1:
            tutorial.destroy()
            return

        current_page[0] += 1
        update_page()

    def previous_page():

        if current_page[0] > 0:
            current_page[0] -= 1
            update_page()

    back_button.configure(
        command=previous_page
    )

    next_button.configure(
        command=next_page
    )

    update_page()

    tutorial.update_idletasks()
    tutorial.lift()
    tutorial.focus_force()


# =========================================================
# GUESS FROM KEYBOARD
# =========================================================

def make_guess_from_keyboard(letter):

    guess_entry.delete(
        0,
        "end"
    )

    guess_entry.insert(
        0,
        letter.lower()
    )

    make_guess()


# =========================================================
# GUESS
# =========================================================

def make_guess():

    global game_over

    if game_over:
        return

    guess = guess_entry.get().lower()

    if len(guess) != 1 or guess not in "abcdefghijklmnopqrstuvwxyz":

        message_label.configure(
            text="You Can NOT guess more than 1 letter in a turn!",
            text_color=ERROR_COLOR
        )

        guess_entry.delete(
            0,
            "end"
        )

        return

    result = process_guess(
        game_state,
        guess
    )

    keyboard_buttons[guess.upper()].configure(
        state="disabled",
        fg_color=KEY_DISABLED,
        hover_color=KEY_DISABLED,
        text_color=KEY_DISABLED_TEXT
    )

    if result == "already_guessed":

        message_label.configure(
            text="You already guessed this letter!",
            text_color=ERROR_COLOR
        )

    elif result == "correct":

        message_label.configure(
            text="Correct!",
            text_color=SUCCESS_COLOR
        )

    elif result == "wrong":

        message_label.configure(
            text="Wrong!",
            text_color=ERROR_COLOR
        )

    elif result == "win":

        game_over = True

        # First update the word on the game screen.
        # This guarantees the final complete word is visible
        # before the result popup appears.
        shown_word = "  ".join(
            game_state["shown"]
        )

        word_label.configure(
            text=shown_word
        )

        message_label.configure(
            text="Correct!",
            text_color=SUCCESS_COLOR
        )

        attempts_label.configure(
            text=f"Attempts: {game_state['attempts']} / "
                 f"{game_state['max_attempts']}"
        )

        # Force Tkinter to draw the completed word first.
        app.update_idletasks()

        # Show custom Win popup.
        show_result_popup(
            "win",
            game_state["word"]
        )

        game_frame.pack_forget()

        choose_category.pack(
            fill="both",
            expand=True
        )

        guess_entry.delete(
            0,
            "end"
        )

        return

    elif result == "lose":

        game_over = True

        # Show the final state before opening the popup.
        shown_word = "  ".join(
            game_state["shown"]
        )

        word_label.configure(
            text=shown_word
        )

        message_label.configure(
            text="Game Over",
            text_color=ERROR_COLOR
        )

        attempts_label.configure(
            text=f"{game_state['attempts']} / "
                 f"{game_state['max_attempts']}"
        )

        app.update_idletasks()

        # Show custom Lose popup.
        show_result_popup(
            "lose",
            game_state["word"]
        )

        game_frame.pack_forget()

        choose_category.pack(
            fill="both",
            expand=True
        )

        guess_entry.delete(
            0,
            "end"
        )

        return

    shown_word = "  ".join(
        game_state["shown"]
    )

    word_label.configure(
        text=shown_word
    )

    attempts_label.configure(
        text=f"Attempts: {game_state['attempts']} / "
             f"{game_state['max_attempts']}"
    )

    guess_entry.delete(
        0,
        "end"
    )


# =========================================================
# MAIN MENU
# =========================================================

main_menu = CTkFrame(
    app,
    fg_color=BG_COLOR
)

main_menu.pack(
    fill="both",
    expand=True
)


main_menu_center = CTkFrame(
    main_menu,
    fg_color="transparent"
)

main_menu_center.place(
    relx=0.5,
    rely=0.46,
    anchor="center"
)


title = CTkLabel(
    main_menu_center,
    text="WORD GUESS",
    font=FONT_TITLE,
    text_color=TEXT_COLOR
)

title.pack(
    pady=(0, 38)
)


play_button = CTkButton(
    main_menu_center,
    text="PLAY",
    width=280,
    height=58,
    font=FONT_BUTTON,
    fg_color=PRIMARY_COLOR,
    hover_color=PRIMARY_HOVER,
    corner_radius=14,
    command=show_categories
)

play_button.pack(
    pady=8
)


how_to_play_button = CTkButton(
    main_menu_center,
    text="HOW TO PLAY",
    width=280,
    height=52,
    font=FONT_BUTTON,
    fg_color=CARD_COLOR,
    hover_color=CARD_HOVER,
    corner_radius=14,
    command=show_tutorial
)

how_to_play_button.pack(
    pady=8
)


quit_button = CTkButton(
    main_menu_center,
    text="QUIT",
    width=280,
    height=52,
    font=FONT_BUTTON,
    fg_color="#2A303D",
    hover_color="#444C5D",
    corner_radius=14,
    command=app.destroy
)

quit_button.pack(
    pady=8
)


creator_label = CTkLabel(
    main_menu,
    text="© Mehiov   •   v1.0",
    font=FONT_SMALL,
    text_color=MUTED_TEXT
)

creator_label.place(
    relx=0.5,
    rely=0.96,
    anchor="center"
)


# =========================================================
# CHOOSE CATEGORY
# =========================================================

choose_category = CTkFrame(
    app,
    fg_color=BG_COLOR
)


category_title = CTkLabel(
    choose_category,
    text="SELECT A CATEGORY",
    font=FONT_HEADING,
    text_color=TEXT_COLOR
)

category_title.pack(
    pady=(38, 22)
)


# ---------------- Random / Mixed ----------------

random_category_button = CTkButton(
    choose_category,
    text="RANDOM  •  MIXED",
    width=620,
    height=82,
    font=("Bahnschrift", 23, "bold"),
    fg_color=PRIMARY_COLOR,
    hover_color=PRIMARY_HOVER,
    text_color=TEXT_COLOR,
    corner_radius=18,
    border_width=2,
    border_color="#6FA0FF",
    command=lambda: start_game("mixed.txt")
)

random_category_button.pack(
    pady=(0, 25)
)


# ---------------- Category Cards ----------------

category_grid = CTkFrame(
    choose_category,
    fg_color="transparent"
)

category_grid.pack()


category_buttons = [
    ("ANIMALS", lambda: start_game("animals.txt")),
    ("OBJECTS", lambda: start_game("objects.txt")),
    ("FOOD", lambda: start_game("food.txt")),
    ("COUNTRIES", lambda: start_game("countries.txt"))
]


for index, (text, command) in enumerate(category_buttons):

    row = index // 2
    column = index % 2

    button = CTkButton(
        category_grid,
        text=text,
        width=275,
        height=110,
        font=("Bahnschrift", 22, "bold"),
        fg_color=CARD_COLOR,
        hover_color=CARD_HOVER,
        text_color=TEXT_COLOR,
        corner_radius=18,
        border_width=1,
        border_color="#30394A",
        command=command
    )

    button.grid(
        row=row,
        column=column,
        padx=12,
        pady=12
    )


back_to_menu_button = CTkButton(
    choose_category,
    text="BACK TO MENU",
    width=190,
    height=44,
    font=FONT_BUTTON,
    fg_color="transparent",
    hover_color=CARD_COLOR,
    border_width=1,
    border_color="#30394A",
    corner_radius=12,
    command=back_to_menu
)

back_to_menu_button.pack(
    pady=(16, 0)
)


# =========================================================
# GAME PAGE
# =========================================================

game_frame = CTkFrame(
    app,
    fg_color=BG_COLOR
)


game_title = CTkLabel(
    game_frame,
    text="GUESS THE WORD",
    font=FONT_HEADING,
    text_color=TEXT_COLOR
)

game_title.pack(
    pady=(28, 18)
)


# ---------------- Word Card ----------------

word_card = CTkFrame(
    game_frame,
    width=760,
    height=150,
    fg_color=PANEL_COLOR,
    corner_radius=18,
    border_width=1,
    border_color="#30394A"
)

word_card.pack(
    padx=40,
    pady=(0, 18)
)

word_card.pack_propagate(False)


word_label = CTkLabel(
    word_card,
    text="",
    font=FONT_WORD,
    text_color=TEXT_COLOR
)

word_label.place(
    relx=0.5,
    rely=0.5,
    anchor="center"
)


# ---------------- Attempts ----------------

attempts_label = CTkLabel(
    game_frame,
    text="Attempts: 0",
    font=FONT_NORMAL,
    text_color=SECONDARY_TEXT
)

attempts_label.pack(
    pady=(0, 6)
)


# ---------------- Message ----------------

message_label = CTkLabel(
    game_frame,
    text="",
    font=("Segoe UI", 17, "bold"),
    text_color=SECONDARY_TEXT
)

message_label.pack(
    pady=(0, 10)
)


# ---------------- Guess Input ----------------

input_frame = CTkFrame(
    game_frame,
    fg_color="transparent"
)

input_frame.pack(
    pady=(0, 12)
)


guess_entry = CTkEntry(
    input_frame,
    width=230,
    height=48,
    font=("Segoe UI", 17),
    placeholder_text="Enter a letter",
    corner_radius=12
)

guess_entry.pack(
    side="left",
    padx=(0, 10)
)


guess_entry.bind(
    "<Return>",
    lambda event: make_guess()
)


guess_button = CTkButton(
    input_frame,
    text="GUESS",
    width=120,
    height=48,
    font=FONT_BUTTON,
    fg_color=PRIMARY_COLOR,
    hover_color=PRIMARY_HOVER,
    corner_radius=12,
    command=make_guess
)

guess_button.pack(
    side="left"
)


# ---------------- Keyboard ----------------

keyboard_frame = CTkFrame(
    game_frame,
    fg_color="transparent"
)

keyboard_frame.pack(
    pady=(3, 12)
)


keyboard_buttons = {}

rows = [
    "QWERTYUIOP",
    "ASDFGHJKL",
    "ZXCVBNM"
]

offsets = [0, 1, 2]


for row_index, row in enumerate(rows):

    for column_index, letter in enumerate(row):

        button = CTkButton(
            keyboard_frame,
            text=letter,
            width=58,
            height=43,
            font=FONT_KEY,
            fg_color=KEY_COLOR,
            hover_color=KEY_HOVER,
            text_color=TEXT_COLOR,
            corner_radius=10,
            border_width=1,
            border_color="#354056",
            command=lambda l=letter: make_guess_from_keyboard(l)
        )

        button.grid(
            row=row_index,
            column=column_index + offsets[row_index],
            padx=3,
            pady=3
        )

        keyboard_buttons[letter] = button


# ---------------- Back ----------------

back_to_categories_button = CTkButton(
    game_frame,
    text="BACK",
    width=120,
    height=42,
    font=FONT_BUTTON,
    fg_color=CARD_COLOR,
    hover_color=CARD_HOVER,
    corner_radius=12,
    command=play_again
)

back_to_categories_button.pack(
    pady=(2, 0)
)


# ---------------- Tutorial Button ----------------

tutorial_game_button = CTkButton(
    game_frame,
    text="?",
    width=42,
    height=42,
    font=("Bahnschrift", 21, "bold"),
    fg_color=CARD_COLOR,
    hover_color=CARD_HOVER,
    text_color=TEXT_COLOR,
    corner_radius=12,
    command=show_tutorial
)

tutorial_game_button.place(
    relx=0.96,
    rely=0.94,
    anchor="se"
)

app.mainloop()