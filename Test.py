'''
Name: Syed Qadri
Date: 09/04/2024
Assignment: Nerdle
Class: ICS4U1
'''

from tkinter import Tk, PhotoImage, Frame, Label, Button, Toplevel, LabelFrame, font, Entry, messagebox, END
import random


def close_help():
    help_window.withdraw()
    root.deiconify()


def open_help():
    help_window.deiconify()
    root.withdraw()


def open_stats():
    stats_window.deiconify()
    root.withdraw()


def close_stats():
    stats_window.withdraw()
    root.deiconify()


def reset_equations():
    equation_bank.clear()
    with open('nerdlequestions.txt', 'r') as reader:
        line = reader.readline().strip('\n')
        while line != '':
            equation_bank.append(line.upper())
            line = reader.readline().strip('\n')
    random.shuffle(equation_bank)


def start_triggered():
    global row_index

    for entry in entries[0]:
        entry.config(state='normal')
    btnStart.config(text='SUBMIT', command=submit_triggered)


def colour_footer(val: str, color: str, level: int):

    if val in operators:
        # the entry value must be an operator
        for lbl in footer_operator_labels:

            footer_status = footer_label_status.get(val)
            if footer_status is not None and level > footer_status:
                continue

            # get background color of entry
            if lbl['text'] == val:
                lbl.config(bg=color)
                footer_label_status[val] = level
    else:
        # the entry must be a number
        for lbl in footer_number_labels:

            footer_status = footer_label_status.get(val)
            if footer_status is not None and level > footer_status:
                continue

            if lbl['text'] == val:
                lbl.config(bg=color)
                footer_label_status[val] = level

def end_game():
    global selected_equation
    messagebox.showinfo('Nerdle', f'You win!\nThe answer was {selected_equation}')

def submit_triggered():
    global row_index

    for entry in entries[row_index + 1]:
        if entry.get() == '':
            messagebox.showerror("Error", "Invalid guess!\nYou need to enter values in each of the text boxes")
            return

    user_input = ''
    for entry in entries[row_index + 1]:
        user_input += entry.get()

    if '=' not in user_input:
        messagebox.showerror("Error", "Invalid!\nYour guess does not compute.")
        return
    else:
        equation, value = user_input.split('=')
        calculated_result = eval(equation)
        if row_index == 5:
            print('lost')
            return
        elif user_input == selected_equation:
            for syed, char in enumerate(user_input):
                for row in entries:
                    row[syed].config(readonlybackground='#6aaa64')
                    colour_footer(char, '#6aaa64', 1)
            for entry in entries[row_index + 1]:
                entry.config(state='readonly')
            end_game()
        else:
            if calculated_result == int(value):
                for syed, char in enumerate(user_input):
                    if char.isdigit() or char in operators:
                        if char == selected_equation[syed]:
                            for row in entries:
                                row[syed].config(readonlybackground='#6aaa64')
                                colour_footer(char, '#6aaa64', 1)

                for syed, char in enumerate(user_input):
                    if char.isdigit() or char in operators:
                        if char in selected_equation and char != selected_equation[syed]:
                            for row in entries:
                                row[syed].config(readonlybackground='#c9b458')
                                colour_footer(char, '#c9b458', 2)

                for syed, char in enumerate(user_input):
                    if char.isdigit() or char in operators:
                        if char not in selected_equation:
                            for row in entries:
                                row[syed].config(readonlybackground='#787c7e')
                                colour_footer(char, '#787c7e', 3)

                for entry in entries[row_index + 1]:
                    entry.config(state='readonly')

                row_index = row_index + 1

                for entry in entries[row_index + 1]:
                    entry.config(state='normal')

            else:
                messagebox.showerror("Error", "Invalid!\nYour guess does not compute.")
                return

def validate_input(event):
    user_input = event.widget.get()

    if len(user_input) > 1:
        messagebox.showerror("Error", "You can only enter one character!")
        event.widget.delete(1, END)
    elif user_input.isdigit() or user_input in operators:
        event.widget.delete(0, END)
        event.widget.insert(0, user_input)
    else:
        messagebox.showerror("Error", "Invalid Input!\nOnly numbers and operators are permitted.")
        event.widget.delete(0, END)


WINDOW_WIDTH, WINDOW_HEIGHT = 475, 575
HELP_WIDTH, HELP_HEIGHT = 440, 755
STATS_WIDTH, STATS_HEIGHT = 395, 450
MAX_LABEL_WIDTH = 30

row_index, word_index = -1, 0
games, wins, attempts = 0, 0, 0
start = False
winningpercentage, currentstreak, maxstreak = 0, 0, 0

# { NUMBER: LEVEL } for example: green is level 1, yellow is level 2, gray is level 3
footer_label_status: dict[str, int] = {}

root = Tk()
root.title('Nerdle')
root.geometry(
    f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{root.winfo_screenwidth() // 2 - WINDOW_WIDTH // 2}+{root.winfo_screenheight() // 2 - WINDOW_HEIGHT // 2}')

help_window = Toplevel()
help_window.protocol('WM_DELETE_WINDOW', close_help)
help_window.geometry(
    f'{HELP_WIDTH}x{HELP_HEIGHT}+{root.winfo_screenwidth() // 2 - HELP_WIDTH // 2}+{root.winfo_screenheight() // 2 - HELP_HEIGHT // 2}')

help_frame = Frame(help_window, padx=5, pady=5, bg='white')
help_frame.pack()

imgHelp = PhotoImage(file='images/instructions.png')
lblHelp = Label(help_frame, image=imgHelp, border=0).pack()

help_window.withdraw()

stats_window = Toplevel()
stats_window.protocol('WM_DELETE_WINDOW', close_stats)
stats_window.geometry(
    f'{STATS_WIDTH}x{STATS_HEIGHT}+{root.winfo_screenwidth() // 2 - STATS_WIDTH // 2}+{root.winfo_screenheight() // 2 - STATS_HEIGHT // 2}')

stats_frame = Frame(stats_window, padx=5, pady=5)
stats_frame.pack()

lblStatistics = Label(stats_frame, text='STATISTICS', fg='#6aaa64',
                      font=font.Font(family='Arial Rounded MT Bold', size=28), padx=10, pady=10)
lblStatistics.grid(row=0, column=0, columnspan=4)
lblTotalPlayed = Label(stats_frame, text='0', pady=5, font=font.Font(size=28, weight='bold'), padx=20)
lblTotalPlayed.grid(row=1, column=0)
lblGamesPlayed = Label(stats_frame, text='GAMES\nPLAYED', pady=5).grid(row=2, column=0)
lblWinPercentage = Label(stats_frame, text='0%', font=font.Font(size=28, weight='bold'), padx=20)
lblWinPercentage.grid(row=1, column=1)
lblPercentage = Label(stats_frame, text='WINNING\nPERCENTAGE', pady=5).grid(row=2, column=1)
lblCurrentStreak = Label(stats_frame, text='0', font=font.Font(size=28, weight='bold'), padx=20)
lblCurrentStreak.grid(row=1, column=2)
lblCurrent = Label(stats_frame, text='CURRENT\nSTREAK', pady=5).grid(row=2, column=2)
lblMaxStreak = Label(stats_frame, text='0', font=font.Font(size=28, weight='bold'), padx=20)
lblMaxStreak.grid(row=1, column=3)
lblMax = Label(stats_frame, text='MAX\nSTREAK', pady=5).grid(row=2, column=3)
lblDistribution = Label(stats_frame, text='GUESS DISTRIBUTION', fg='#6aaa64',
                        font=font.Font(family='Arial Rounded MT Bold', size=18), padx=10, pady=10)
lblDistribution.grid(row=3, column=0, columnspan=4)

distribution_frame = Frame(stats_frame, padx=5, pady=5)

distribution_results = [0] * 6
number_labels, distribution_labels = [None] * 6, [None] * 6

for index in range(6):
    number_labels[index] = Label(distribution_frame, padx=10, font=font.Font(weight='bold'), text=str(index + 1))
    number_labels[index].grid(row=index, column=0)
    distribution_labels[index] = Label(distribution_frame, fg='white', font=font.Font(weight='bold'), anchor='e', text='0', width=distribution_results[index] // MAX_LABEL_WIDTH, padx=2, bg='#787c7e')
    distribution_labels[index].grid(row=index, column=1, sticky='w')

distribution_frame.grid(row=4, column=0, columnspan=4, sticky='w')

stats_window.withdraw()

frame = Frame(root, padx=10, pady=10)
frame.pack()

imgLogo = PhotoImage(file='images/nerdle_logo.png')
lblTitle = Label(frame, image=imgLogo, border=0).grid(row=0, column=0)

entries_frame = Frame(frame, padx=5, pady=5)
entries_frame.grid(row=1, column=0)

entries = [
    [Entry(entries_frame, width=2, state='disabled', font=('Arial Rounded MT Bold', 28), justify='center') for x in
     range(8)] for y in range(6)]
for y, row in enumerate(entries):
    for x, entry in enumerate(row):
        entry.grid(row=y, column=x, padx=2, pady=2)
for row in entries:
    for entry in row:
        entry.bind('<KeyRelease>', validate_input)

buttonFrame = Frame(frame, padx=5, pady=5)
buttonFrame.grid(row=2, column=0)

btnStart = Button(buttonFrame, text='START', width=10, padx=10, pady=5, command=start_triggered)
btnStart.grid(row=0, column=0, padx=5)
btnStats = Button(buttonFrame, text='STATS', width=10, padx=10, pady=5, command=open_stats)
btnStats.grid(row=0, column=1, padx=5)
btnHelp = Button(buttonFrame, text='HELP', width=10, padx=10, pady=5, command=open_help)
btnHelp.grid(row=0, column=2, padx=5)

lettersFrame = LabelFrame(frame, width=400, height=50, padx=5, pady=5, relief='solid', borderwidth=1,
                          font='"Arial Rounded MT Bold" 10')
lettersFrame.grid(row=3, column=0, pady=10)
equation_bank = []

with open('nerdlequestions.txt', 'r') as reader:
    line = reader.readline().strip('\n')
    while line != '':
        equation_bank.append(line.upper())
        line = reader.readline().strip('\n')
selected_equation = random.choice(equation_bank)
equation_bank.remove(selected_equation)
if len(equation_bank) == 0:
    reset_equations()
    selected_equation = random.choice(equation_bank)
    equation_bank.remove(selected_equation)
print(selected_equation)

numbers = "0123456789"
operators = "+-*/="

numbers_frame = Frame(lettersFrame)
numbers_frame.grid(row=0, column=0)

footer_number_labels = []
for number in numbers:
    label = Label(numbers_frame, text=number, relief='solid', borderwidth=1, width=4, height=2)
    label.grid(row=0, column=numbers.index(number), padx=2, pady=2)
    footer_number_labels.append(label)

operators_frame = Frame(lettersFrame)
operators_frame.grid(row=1, column=0)

footer_operator_labels = []
for operator in operators:
    label = Label(operators_frame, text=operator, relief='solid', borderwidth=1, width=9, height=2)
    label.grid(row=0, column=operators.index(operator), padx=2, pady=2)
    footer_operator_labels.append(label)

root.mainloop()
