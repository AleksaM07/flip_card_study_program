import tkinter.scrolledtext
from tkinter import messagebox
from tkinter import *
import pandas, random, atexit
from PIL import Image, ImageTk


BACKGROUND_COLOR = "#B1DDC6"
FONT_TITLE = ("Arial", 30, "italic")
FONT_TEXT =("Arial", 15, "normal")
QUESTION = "Pitanje"
ANSWER ="Odgovor"
current_question_index = 0
current_question = ""

i = 0

#--------------------pick a random question funktion-----------------------------
def extract_question():
    global lista
    data = pandas.read_csv("data/ORK pitanja.csv", encoding='Windows-1252')
    rows = data["Pitanje"].to_dict()
    index = random.choice(lista)
    question = rows[index]
    return question, index

def get_questions_red():
    global current_question_index, current_question, lista
    current_question, current_question_index = extract_question()
    question_and_answer.configure(state='normal')
    question_and_answer.delete("1.0", "end")
    question_and_answer.tag_configure('center', justify='center')
    question_and_answer.insert("end", current_question, 'center')
    question_and_answer.configure(state='disabled')

    canvas.itemconfig(canvas_picture, image=card_front)
    question_and_answer.config(background="white")
    canvas.itemconfig(card_title, text=QUESTION)
    print(lista)

def get_questions_green():
    global lista, current_question_index
    get_questions_red()
    lista.remove(current_question_index)
    print(lista)

#--------------------flip the side of the card to answer-----------------------------
def extract_answer():
    data = pandas.read_csv("data/ORK pitanja.csv", encoding='Windows-1252')
    rows = data["Odgovor"].to_dict()
    answer = rows[current_question_index]
    return answer

def get_answer():
    global i
    if i % 2 == 0:
        canvas.itemconfig(canvas_picture, image=card_back)
        question_and_answer.config(background=BACKGROUND_COLOR)
        canvas.itemconfig(card_title, text=ANSWER)

        answer = extract_answer()

        question_and_answer.configure(state='normal')
        question_and_answer.delete("1.0", "end")
        question_and_answer.tag_configure('center', justify='center')
        question_and_answer.insert("end", answer, 'center')
        question_and_answer.configure(state='disabled')
    else:
        canvas.itemconfig(canvas_picture, image=card_front)
        question_and_answer.config(background="white")
        canvas.itemconfig(card_title, text=QUESTION)

        question_and_answer.configure(state='normal')
        question_and_answer.delete("1.0", "end")
        question_and_answer.tag_configure('center', justify='center')
        question_and_answer.insert("end", current_question, 'center')
        question_and_answer.configure(state='disabled')
    i += 1
#---------------------------------------------------------------------------------

#before we exit------------------------------------------------
def exit_handler():
    global lista
    data = pandas.DataFrame(lista)
    data.to_csv("data/saved_progress", index=False)
atexit.register(exit_handler)
#---------------------------------------------------------------

#Creating a window
window = Tk()
window.title("Flash Cards - Study Technique")
window.config(padx=50, pady=50, background=BACKGROUND_COLOR)

#creating a canvas, images, Text, and buttons
canvas = Canvas(height=526, width=800, background=BACKGROUND_COLOR)
card_back = PhotoImage(file='images/card_back.png')
card_front = PhotoImage(file='images/card_front.png')
right = PhotoImage(file='images/right.png')
wrong = PhotoImage(file='images/wrong.png')

#In Python, objects are garbage collected when there are no more references to them. When an object is garbage collected, its memory is freed and it is no longer available to the program.
#In the case of Tkinter widgets that display images, the image data is stored in a PhotoImage object. If there are no references to the PhotoImage object, it will be garbage collected, and the widget that references it will no longer display the image.
#Therefore, to ensure that the image is displayed correctly in a Tkinter widget, you need to keep a reference to the PhotoImage object for as long as the widget is being displayed. This can be achieved by assigning the PhotoImage object to an attribute of a widget, such as the image attribute of a Label, or by storing it in a global variable or an instance variable of a class. By doing so, you ensure that the PhotoImage object is not garbage collected until it is no longer needed.
flip_resized = Image.open('images/flip.png').resize((130,100))
flip = ImageTk.PhotoImage(flip_resized)

canvas_picture = canvas.create_image(400, 263, image=card_front)
canvas.config(highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=3, rowspan=2)
card_title = canvas.create_text(400, 150, text=QUESTION, font=FONT_TITLE)

button_right = Button(image=right, highlightthickness=0, command=get_questions_green)
button_right.grid(row=2, column=0)
button_wrong = Button(image=wrong, highlightthickness=0, command=get_questions_red)
button_wrong.grid(row=2, column=2)
button_flip = Button(image=flip, highlightthickness=0, command=get_answer)
button_flip.grid(row=2, column=1)

question_and_answer = tkinter.scrolledtext.ScrolledText(font=FONT_TEXT, height=7, width=60, highlightthickness=0, background="white")
question_and_answer.grid(row=1, column=0, columnspan=3)

#asking if we want to load saved progress or go again
is_ok = messagebox.askokcancel(title="window", message="Do you want to study from saved progress or go again?")
if is_ok:
        data = pandas.read_csv("data/ORK pitanja.csv", encoding='Windows-1252')
        unedited_list = data.to_dict()["Pitanje"]
        lista = list(unedited_list.keys())
        print(lista)
else:
    try:
        with open("data/saved_progress.csv", mode="r") as data:
            lista = data.read()
    except FileNotFoundError:
            data = pandas.read_csv("data/ORK pitanja.csv", encoding='Windows-1252')
            unedited_list = data.to_dict()["Pitanje"]
            lista = list(unedited_list.keys())
            print(lista)
    else:
        pass

get_questions_red()

window.mainloop()