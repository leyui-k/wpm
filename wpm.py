import tkinter as tk
from tkinter import *
import ctypes
from faker import Faker
import time
from PIL import ImageTk, Image
fake = Faker()
ctypes.windll.shcore.SetProcessDpiAwareness(1)

root = tk.Tk()
root.title('Type Speed Test')
root.geometry('1920x1080')
root.configure(bg='#303030')
root.option_add("*Label.Font", "consolas 15")
root.option_add("*Button.Font", "consolas 30")

def get_new_text(max_nb_chars=1200):
    return fake.text(max_nb_chars=max_nb_chars).replace(".", "").replace("\n", " ").lower()

def resetWritingLabels(time_limit):
    sample_text = get_new_text(selected_max_nb_chars.get())

    global labelRight
    labelRight = Label(root, text=sample_text, fg='white', bg='#303030', wraplength=1000, justify=CENTER)
    labelRight.configure(text=sample_text)
    labelRight.place(relx=0.5, rely=0.4, anchor=CENTER)

    global currentLetterLabel
    currentLetterLabel = Label(root, text=sample_text[0], fg='white', bg='#303030')
    currentLetterLabel.place(relx=0.5, rely=0.7, anchor=N)

    global timeleftLabel
    timeleftLabel = Label(root, text=f'0 Seconds', fg='white', bg='#303030')
    timeleftLabel.place(relx=0.5, rely=0.1, anchor=S)

    global writeAble, start_time, passedSeconds, user_word_count, total_keystrokes, correct_keystrokes
    writeAble = True
    start_time = time.time()
    passedSeconds = 0
    user_word_count = 0
    total_keystrokes = 0
    correct_keystrokes = 0
    root.bind('<Key>', keyPress)

    root.after(time_limit * 1000, stopTest)
    root.after(1000, addSecond)
    

    start_button.destroy()
    time_button.place_forget()
    category_bar.place_forget()
    button.place_forget() 
    button1.place_forget() 
    button2.place_forget() 
    max_nb_chars_button.place_forget()
    max_nb_chars_button1.place_forget()
    max_nb_chars_button2.place_forget()

# Final code
def stopTest():
    global writeAble
    elapsed_time_minutes = passedSeconds / 60
    wpm = int((user_word_count / elapsed_time_minutes) if elapsed_time_minutes > 0 else 0)
    accuracy = round((correct_keystrokes / total_keystrokes) * 100, 2) if total_keystrokes > 0 else 0

    timeleftLabel.destroy()
    currentLetterLabel.destroy()
    labelRight.destroy()

    global ResultLabel
    ResultLabel = Label(root, text=f'Words per Minute: {wpm}\nAccuracy: {accuracy}%', fg='black')
    ResultLabel.place(relx=0.5, rely=0.4, anchor=CENTER)

    global ResultButton
    ResultButton = Button(root, text=f'Retry', command=restart)
    ResultButton.place(relx=0.5, rely=0.5, anchor=CENTER)

    on_category_selected("time")
    on_category_selected("words")
    create_time_with_image(category_bar, "time", img, 0.090, 0.5, lambda: on_category_selected("time"))
    category_bar.place(relx=0.5, rely=0.2, relwidth=0.5, relheight=0.1, anchor=CENTER)

# Log key pressed
def keyPress(event):
    global start_time
    global user_word_count
    global total_keystrokes
    global correct_keystrokes
    total_keystrokes += 1
    try:
        if labelRight.cget('text'):
            if event.char.lower() == labelRight.cget('text')[0].lower():
                correct_keystrokes += 1
                labelRight.configure(text=labelRight.cget('text')[1:])

                if labelRight.cget('text'):
                    currentLetterLabel.configure(text=labelRight.cget('text')[0])
                    if event.char.lower() == ' ':
                        user_word_count += 1
                else:
                    stopTest()
    except tk.TclError:
        pass

# Restart game and objets in the screen 
def restart():
    global start_time
    start_time = time.time()
    ResultLabel.destroy()
    ResultButton.destroy()
    resetWritingLabels(selected_time_limit.get())

# Seconds count
def addSecond():
    global passedSeconds
    passedSeconds = int(time.time() - start_time)
    
    if timeleftLabel.winfo_exists():
        timeleftLabel.configure(text=f'{passedSeconds} Seconds')

    if writeAble and passedSeconds < selected_time_limit.get():
        root.after(1000, addSecond)

# View button time selected
def change_selected_button(button):
    global selected_button
    if selected_button is not None:
        selected_button.config(fg='WHITE')
    button.config(fg="yellow")
    selected_button = button
selected_button = None

# View button word selected
def change_selected_button_max(button_max):
    global selected_button_max
    if selected_button_max is not None:
        selected_button_max.config(fg='WHITE')
    button_max.config(fg="yellow")
    selected_button_max = button_max
selected_button_max = None

# View option selected
def change_selected_option(option):
    global selected_option
    if selected_option is not None:
        selected_option.config(fg='white')
    option.config(fg='yellow')
    selected_option = option
selected_option = None

#Combine 2 functions in a same config
def combine_funcs(*funcs):
    def inner_combined_func(*args, **kwargs): 
        for f in funcs:
            f(*args, **kwargs)
    return inner_combined_func

# Amount of words
def set_max_nb_chars(chars):
    selected_max_nb_chars.set(chars)
selected_max_nb_chars = IntVar()
selected_max_nb_chars.set(1200)

# Time limit
def set_time_limit(time):
    selected_time_limit.set(time)
selected_time_limit = IntVar()
selected_time_limit.set(10)

# Buttons for time 
def create_button(text, x_rel, time_limit):
    button = tk.Button(root, text=text, font='12', bg='#262626', fg='WHITE', activebackground='#262626', activeforeground='white')
    button.config(
        command=
        lambda button=button, time_limit=time_limit: (
            change_selected_button(button),
            set_time_limit(time_limit)
        ),
        border=0
    )
    return button

# Buttons for words
def create_button_max(text, x_rel, max_nb_chars):
    button_max = tk.Button(root, text=text, font='12', bg='#262626', fg='WHITE', activebackground='#262626', activeforeground='white')
    button_max.config(
        command=
        lambda button_max=button_max, max_nb_chars=max_nb_chars: (
            change_selected_button_max(button_max),
            set_max_nb_chars(max_nb_chars)
        ),
        border=0
    )
    return button_max

# Which category was choosed
def on_category_selected(category):
    if category == "time":
        button.place_forget()
        button1.place_forget()
        button2.place_forget()
        button.place(relx=0.66, rely=0.2, anchor=CENTER)
        button1.place(relx=0.69, rely=0.2, anchor=CENTER)
        button2.place(relx=0.72, rely=0.2, anchor=CENTER)
        max_nb_chars_button.place_forget()
        max_nb_chars_button1.place_forget()
        max_nb_chars_button2.place_forget()
    elif category == 'words':
        max_nb_chars_button.place_forget()
        max_nb_chars_button1.place_forget()
        max_nb_chars_button2.place_forget()
        max_nb_chars_button.place(relx=0.66, rely=0.2, anchor=CENTER)
        max_nb_chars_button1.place(relx=0.69, rely=0.2, anchor=CENTER)
        max_nb_chars_button2.place(relx=0.72, rely=0.2, anchor=CENTER)
        pass

# Image of clock
def load_and_resize_image(file_path, width, height):
    image = Image.open(file_path)
    image = image.resize((width, height))
    return ImageTk.PhotoImage(image)
img = load_and_resize_image('clock.png', 30, 30)
word = load_and_resize_image('word.png', 30, 30)

# Time button
def create_time_with_image(frame, text, image, relx, rely, command):
    option = tk.Button(frame, text=text, font=("Helvetica", 21), fg='white', bg='#262626', activebackground='#262626', activeforeground='WHITE', command=command)
    option.place(relx=relx, rely=rely, anchor=CENTER)
    option.config(
        command=lambda option=option: (
            on_category_selected("time"),
            change_selected_option(option)
        ),
        border=0)
    
    label_image = tk.Label(frame, image=image, bg='#262626')
    label_image.place(relx=relx - 0.06, rely=rely, anchor=CENTER)

    return option

# Word button
def create_words_with_image(frame, text, image, relx, rely, command):
    option1 = tk.Button(frame, text=text, font=("Helvetica", 21), fg='white', bg='#262626', activebackground='#262626', activeforeground='WHITE', command=command)
    option1.place(relx=0.23, rely=0.5, anchor=CENTER)
    option1.config(
        command=lambda option=option1: (
            on_category_selected("words"),
            change_selected_option(option)
        ),
        border=0)
    
    label_image = tk.Label(frame, image=image, bg='#262626')
    label_image.place(relx=relx - 0.06, rely=rely, anchor=CENTER)

    return option1

#### Bar
category_bar = tk.Frame(root, bg='#262626')
category_bar.place(relx=0.5, rely=0.2, relwidth=0.5, relheight=0.1, anchor=CENTER)

# Time button with its buttons
time_button = create_time_with_image(category_bar, "time", img, 0.090, 0.5, command=lambda: on_category_selected("time"))
button = create_button('𝟭𝟬', 0.66, 10)
button1 = create_button('𝟯𝟬', 0.69, 30)
button2 = create_button('𝟲𝟬', 0.72, 60)

# Word button with its buttons
words_button = create_words_with_image(category_bar, "words", word, 0.217, 0.5, lambda: on_category_selected("words"))
max_nb_chars_button = create_button_max("𝟯𝟱𝟬", 0.45, 350)
max_nb_chars_button1 = create_button_max("𝟲𝟱𝟬", 0.50, 650)
max_nb_chars_button2 = create_button_max("𝟭𝟮𝟬𝟬", 0.55, 1200)

# Start button
start_button = Button(root, text='Start Test', command=lambda: resetWritingLabels(selected_time_limit.get()))
start_button.place(relx=0.5, rely=0.4, anchor=CENTER)

root.mainloop()

# Resources used:
# https://thepythoncode.com/article/how-to-make-typing-speed-tester-in-python-using-tkinter
# https://www.youtube.com/watch?v=lt78_05hHSk&ab_channel=thenewboston
# 