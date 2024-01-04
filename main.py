import PySimpleGUI as sg
import json
from tkinter import ttk
import matplotlib.pyplot as plt
import random

file = open('set.json')
data = json.load(file)


# sorts the questions from most incorrect to least

def listdata(list1, endlist):
    f = sorted(list1)
    for i in f:
        endlist.append(list1.index(i))
        list1[list1.index(i)] = -1
    endlist.reverse()
    return endlist


# checks if the reorder list has any questions have been truly mastered, if so they are removed

def validate_reorder(reorder_output, max_q_no_in_file, true_mastery, reorder_validating):
    for index in range(0, max_q_no_in_file + 1):
        if true_mastery[reorder_output[index]] == 1:
            pass
        else:
            reorder_validating.append(reorder_output[index])
    return reorder_validating


def main():  # initialise the variables from the JSON file
    question = data['question']
    answers = data['answers']
    automark = data['automark']
    markscheme = data['markscheme']
    mastery = data['mastery']
    incorrect = data['incorrect']
    correct = data['correct']
    partiallycorrect = data['partiallycorrect']
    current_incorrect = data['current_incorrect']
    true_mastery = data['true_mastery']
    max_q_no = data['maximum_question_number']
    max_q_no_in_file = data['maximum_question_number_in_file']
    reorder = data['reorder']
    reorder_present = data['reorder_present']
    images = data['images']
    image_default = data['image_default']
    index = 0  # used to iterate through the question set array
    allow = True  # stops user from answering questions after they have answered it wrong
    submit_button_clicked = 0  # tracks how many times the enter buttons has been pressed
    sg.theme('Reddit')  # Adding colour
    lock = False  # used to lock the question screen
    total_true_mastery = 0  # used to create infographics
    total_correct = 0  # used to create infographics
    total_incorrect = 0  # used to create infographics
    total_partially_correct = 0  # used to create infographics
    endlist = []  # number in the list represent question number
    reorder_validating = []
    default = []
    total_correct_in_file = 0
    total_partially_correct_in_file = 0
    total_incorrect_in_file = 0
    # Stuff in side the window

    # checks if the user has used the program before, and gives out a custom set of questions
    if reorder_present[0] == 0:
        default = list(range(0, max_q_no + 1))
    else:
        for index in range(0, 3):
            default.append(reorder[index])

        while len(default) != 5:
            n = random.randint(0, max_q_no_in_file)  # choose random number
            if n in default or true_mastery[n] == 1:  # checks if random number already
                pass  # exists in the array and has been truly mastered
            else:
                default.append(n)

    print(default)

    # creates the layout where elements are stored
    layout = [
        [
            sg.TabGroup(
                [[
                    sg.Tab(
                        'Main Menu',
                        [[sg.Text('Main Menu', pad=(260, 20), font=('Calibri', 13))],
                         [sg.Button('Questions', pad=(268, 20))],
                         [sg.Button('Statistics', pad=(268, 20), key='s1')]],

                        key='tab_1'),

                    sg.Tab(
                        'Questions',
                        [[sg.Text(size=(23, 1), key='-MASTERY-'),
                          sg.Text(size=(60, 1), key='-OUTPUT-', font=('Calibri', 12))],
                         [sg.Text(size=(7, 1)),
                          sg.Text(size=(56, 1), key='-OUTPUT2-', justification='center', font=('Calibri', 12))],
                         [sg.Text(size=(7, 1)),
                          sg.Text(size=(56, 1), key='-OUTPUT3-', justification='center', font=('Calibri', 12))],
                         [sg.Text(size=(7, 1)),
                          sg.Text(size=(56, 1), key='-OUTPUT4-', justification='center', font=('Calibri', 12))],
                         [sg.Text(size=(15, 1)),
                          sg.Image(key='-IMAGE-')],
                         [sg.Text(size=(60, 1), font=('Calibri', 1))],
                         [sg.Text(size=(60, 9))],
                         [sg.Text("       correct answer:"), sg.Text(size=(60, 1), key='-OUTPUTA-')],
                         [sg.Text("     automark allows:"), sg.Text(size=(60, 1), key='-OUTPUTB-')],
                         [sg.Text("                you said:"), sg.Text(size=(60, 1), key='-OUTPUTC-')],
                         [sg.Text("                 marked:"), sg.Text(size=(60, 1), key='-OUTPUTD-')],
                         [sg.Text("      Answer here:   "),
                          sg.InputText(size=(60, 1), key='-INPUT-', do_not_clear=False)],
                         [sg.Text(size=(26, 0)), sg.Button('Submit', key='b1', bind_return_key=True),
                          sg.Button('Cancel'), sg.Button('Skip')],
                         ],
                        key='tab_2'),
                    sg.Tab(
                        'Completed screen',
                        [[sg.Text('Completed all questions', pad=(219, 20), font=('Calibri', 13))],
                         [sg.Button('Statistics', pad=(268, 20), key='s2')]],
                        key='tab_3')

                ]],
                key='tabgroup',
                enable_events=True)
        ],
    ]
    # Create the Window
    window = sg.Window('Rerevise', layout, finalize=True, size=(655, 565))
    style = ttk.Style()
    style.layout('TNotebook.Tab', [])
    # Event Loop to process "events" and get the "values" of the inputs
    window['tabgroup'].Widget.select(0)
    selected = 0

    question_length = len(question[default[index]])

    # checks if the first question has an image attached and if yes, it shows the image on screen

    if images[default[index]] == "":
        filepath = image_default[0]
        window['-IMAGE-'].update(filename=filepath)  # shows blank image on screen
    else:
        filepath = images[default[index]]
        window['-IMAGE-'].update(filename=filepath)  # shows image that corresponds to the question on screen

    # loads in the first question and checks the length, to see if it needs to be adjusted to fit on screen

    if question_length <= 30:
        window['-OUTPUT-'].update(question[default[index]])
        window['-OUTPUT2-'].update('')
        window['-OUTPUT3-'].update('')
        window['-OUTPUT4-'].update('')
    elif 30 < question_length < 86:
        window['-OUTPUT-'].update(question[default[index]][0:30])
        window['-OUTPUT2-'].update(question[default[index]][30:question_length])
        window['-OUTPUT3-'].update('')
        window['-OUTPUT4-'].update('')
    elif 86 < question_length < 142:
        window['-OUTPUT-'].update(question[default[index]][0:30])
        window['-OUTPUT2-'].update(question[default[index]][30:86])
        window['-OUTPUT3-'].update(question[default[index]][86:142])
        window['-OUTPUT4-'].update('')
    else:
        window['-OUTPUT-'].update(question[default[index]][0:30])
        window['-OUTPUT2-'].update(question[default[index]][30:86])
        window['-OUTPUT3-'].update(question[default[index]][86:142])
        window['-OUTPUT4-'].update(question[default[index]][142:question_length])

    mastery_output = "mastery:" + str(mastery[default[index]]) + "/3"

    window['-MASTERY-'].update(mastery_output)  # outputs the mastery of the question to the GUI

    while True:
        event, values = window.read()  # creates the GUI

        if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel, while loop ends
            break

        if selected == 0:
            if event == 'Questions':
                window['tabgroup'].Widget.select(1)  # selects the question tab
                selected = 1
            if event == 's1':  # shows statistics of every question
                for index in range(0, max_q_no_in_file + 1):
                    total_correct_in_file += correct[index]
                    total_partially_correct_in_file += partiallycorrect[index]
                    total_incorrect_in_file += incorrect[index]
                index = 0

                if total_incorrect_in_file == 0 and total_correct_in_file == 0 and total_incorrect_in_file == 0:  # checks if user has an data before creating infographics
                    pass
                else:
                    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
                    labels = 'Correct', 'Incorrect', 'Partially correct'  # creates the labels that will appear on the pie chart
                    sizes = [total_correct_in_file, total_partially_correct_in_file, total_incorrect_in_file]
                    explode = (0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

                    # add colors
                    colors = ['#99ff99', '#ff9999', '#66b3ff']
                    fig1, ax1 = plt.subplots()
                    ax1.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
                            shadow=True, startangle=90)  # Equal aspect ratio ensures that pie is drawn as a circle
                    ax1.axis('equal')
                    plt.tight_layout()
                    plt.show()  # creates the pie chart window

        if selected == 1:
            # adjusts the question to fit on screen

            question_length = len(question[default[index]])

            if question_length <= 30:
                window['-OUTPUT-'].update(question[default[index]])
                window['-OUTPUT2-'].update('')
                window['-OUTPUT3-'].update('')
                window['-OUTPUT4-'].update('')
            elif 30 < question_length < 86:
                window['-OUTPUT-'].update(question[default[index]][0:30])
                window['-OUTPUT2-'].update(question[default[index]][30:question_length])
                window['-OUTPUT3-'].update('')
                window['-OUTPUT4-'].update('')
            elif 86 < question_length < 142:
                window['-OUTPUT-'].update(question[default[index]][0:30])
                window['-OUTPUT2-'].update(question[default[index]][30:86])
                window['-OUTPUT3-'].update(question[default[index]][86:142])
                window['-OUTPUT4-'].update('')
            else:
                window['-OUTPUT-'].update(question[default[index]][0:30])
                window['-OUTPUT2-'].update(question[default[index]][30:86])
                window['-OUTPUT3-'].update(question[default[index]][86:142])
                window['-OUTPUT4-'].update(question[default[index]][142:question_length])

            # checks if the question has an image attached and if yes, it shows the image on screen

            if images[default[index]] == "":
                filepath = image_default[0]
                window['-IMAGE-'].update(filename=filepath)  # shows blank image on screen
            else:
                filepath = images[default[index]]
                window['-IMAGE-'].update(filename=filepath)  # shows image that corresponds to the question on screen

            select_not_mastered_question = True

            # creates a lock on the keybinded enter button
            if not lock:
                if allow is False and event == 'b1':
                    submit_button_clicked += 1
            else:
                allow = False  # once questions have been answered user cannot return to the same page

            # bans access to marking algorithm if user has answered a question wrong or is on a different part of the program
            if allow:
                if event == 'b1':
                    submit_button_clicked += 1  # if enter is button is pressed this variable is incremented by one

                    if values['-INPUT-'].lower() == answers[default[index]]:  # checks if input matches mark scheme exactly
                        mastery[default[index]] += 1  # increases mastery of this question by one
                        correct[default[index]] += 1  # increases mastery of this question by one
                        print(mastery)
                        index += 1
                        if index > max_q_no:  # resets index if index is past the size of the array
                            index = 0

                        counter = 0
                        for index2 in range(0, max_q_no + 1):  # checks if all the questions have a mastery of three
                            if mastery[default[index2]] == 3:
                                counter += 1  # if counter reaches 5 all questions have been mastered

                        if counter == 5:  # answer question screen ends if all questions have been mastered
                            if reorder_present[0] == 0:  # allow the reorder algorithm to run
                                reorder_present[0] += 1
                            window['tabgroup'].Widget.select(2)  # changes screen to completed screen
                            lock = True  # bans inputs via keyboard
                            selected = 2

                            list1 = incorrect.copy()  # creates a copy of the list
                            reorder_output = listdata(list1, endlist)  # function is called and return value is passed into reorder output

                            # totals all the data before saving to JSON file

                            for index in range(0, max_q_no + 1):
                                if current_incorrect[default[index]] == 0 and true_mastery[default[index]] == 0:
                                    true_mastery[default[index]] += 1

                                total_true_mastery += true_mastery[default[index]]
                                total_correct += correct[default[index]]
                                total_partially_correct += partiallycorrect[default[index]]
                                total_incorrect += incorrect[default[index]]
                                mastery[default[index]] = 0
                                current_incorrect[default[index]] = 0

                            reorder_validated = validate_reorder(reorder_output, max_q_no_in_file, true_mastery,
                                                                 reorder_validating)
                            if len(reorder_validated) == 0:
                                pass
                            else:
                                for index in range(0, len(reorder_validated)):
                                    reorder[index] = reorder_validated[index]

                            with open('set.json', 'w', encoding='utf-8') as f:  # JSON file is opened to write in
                                json.dump(data, f, ensure_ascii=False, indent=4)  # data is written into the JSON file
                            f.close()  # file is closed

                        else:
                            while select_not_mastered_question:  # finds a question that has not already been mastered
                                if index > max_q_no:
                                    index = 0
                                else:
                                    if mastery[default[index]] == 3:
                                        index += 1
                                    else:
                                        select_not_mastered_question = False

                            question_length = len(question[default[index]])

                            # adjusts the question to fit on screen

                            if question_length <= 30:
                                window['-OUTPUT-'].update(question[default[index]])
                                window['-OUTPUT2-'].update('')
                                window['-OUTPUT3-'].update('')
                                window['-OUTPUT4-'].update('')
                            elif 30 < question_length < 86:
                                window['-OUTPUT-'].update(
                                    question[default[index]][0:30])
                                window['-OUTPUT2-'].update(question[default[index]][30:question_length])
                                window['-OUTPUT3-'].update('')
                                window['-OUTPUT4-'].update('')
                            elif 86 < question_length < 142:
                                window['-OUTPUT-'].update(
                                    question[default[index]][0:30])
                                window['-OUTPUT2-'].update(question[default[index]][30:86])
                                window['-OUTPUT3-'].update(question[default[index]][86:142])
                                window['-OUTPUT4-'].update('')
                            else:
                                window['-OUTPUT-'].update(
                                    question[default[index]][0:30])
                                window['-OUTPUT2-'].update(question[default[index]][30:86])
                                window['-OUTPUT3-'].update(question[default[index]][86:142])
                                window['-OUTPUT4-'].update(question[default[index]][142:question_length])

                        # clears all the text elements on screen

                        window['-OUTPUTA-'].update('')
                        window['-OUTPUTB-'].update('')
                        window['-OUTPUTC-'].update('')
                        window['-OUTPUTD-'].update('')

                        if selected == 2:
                            index = 0  # index is reset to 0 to stop index error from occurring
                        if images[default[index]] == "":
                            filepath = image_default[0]
                            window['-IMAGE-'].update(filename=filepath)  # shows blank image on screen
                        else:
                            filepath = images[default[index]]
                            window['-IMAGE-'].update(filename=filepath)  # shows image that corresponds to the question on screen

                        mastery_output = "mastery:" + str(mastery[default[index]]) + "/3"

                        window['-MASTERY-'].update(mastery_output)

                    elif all(answer in values['-INPUT-'].lower() for answer in automark[default[index]]):
                        mastery[default[index]] += 1
                        correct[default[index]] += 1
                        print(mastery)
                        index += 1
                        if index > max_q_no:
                            index = 0

                        counter = 0
                        for index2 in range(0, max_q_no + 1):
                            if mastery[default[index2]] == 3:
                                counter += 1

                        if counter == 5:
                            if reorder_present[0] == 0:
                                reorder_present[0] += 1
                            window['tabgroup'].Widget.select(2)
                            lock = True
                            selected = 2

                            list1 = incorrect.copy()
                            reorder_output = listdata(list1, endlist)

                            for index in range(0, max_q_no + 1):
                                if current_incorrect[default[index]] == 0 and true_mastery[default[index]] == 0:
                                    true_mastery[default[index]] += 1

                                total_true_mastery += true_mastery[default[index]]
                                total_correct += correct[default[index]]
                                total_partially_correct += partiallycorrect[default[index]]
                                total_incorrect += incorrect[default[index]]
                                mastery[default[index]] = 0
                                current_incorrect[default[index]] = 0

                            reorder_validated = validate_reorder(reorder_output, max_q_no_in_file, true_mastery,
                                                                 reorder_validating)
                            if len(reorder_validated) == 0:
                                pass
                            else:
                                for index in range(0, len(reorder_validated)):
                                    reorder[index] = reorder_validated[index]

                            with open('set.json', 'w', encoding='utf-8') as f:
                                json.dump(data, f, ensure_ascii=False, indent=4)
                            f.close()
                        else:
                            while select_not_mastered_question:  # make sures the next question has not already been mastered
                                if index > max_q_no:
                                    index = 0
                                else:
                                    if mastery[default[index]] == 3:
                                        index += 1
                                    else:
                                        select_not_mastered_question = False

                        question_length = len(question[default[index]])

                        # adjusts the question to fit on screen

                        if question_length <= 30:
                            window['-OUTPUT-'].update(question[default[index]])
                            window['-OUTPUT2-'].update('')
                            window['-OUTPUT3-'].update('')
                            window['-OUTPUT4-'].update('')
                        elif 30 < question_length < 86:
                            window['-OUTPUT-'].update(question[default[index]][0:30])
                            window['-OUTPUT2-'].update(question[default[index]][30:question_length])
                            window['-OUTPUT3-'].update('')
                            window['-OUTPUT4-'].update('')
                        elif 86 < question_length < 142:
                            window['-OUTPUT-'].update(question[default[index]][0:30])
                            window['-OUTPUT2-'].update(question[default[index]][30:86])
                            window['-OUTPUT3-'].update(question[default[index]][86:142])
                            window['-OUTPUT4-'].update('')
                        else:
                            window['-OUTPUT-'].update(question[default[index]][0:30])
                            window['-OUTPUT2-'].update(question[default[index]][30:86])
                            window['-OUTPUT3-'].update(question[default[index]][86:142])
                            window['-OUTPUT4-'].update(question[default[index]][142:question_length])

                        window['-OUTPUTA-'].update('')
                        window['-OUTPUTB-'].update('')
                        window['-OUTPUTC-'].update('')
                        window['-OUTPUTD-'].update('')

                        if selected == 2:
                            index = 0

                        mastery_output = "mastery:" + str(mastery[default[index]]) + "/3"

                        window['-MASTERY-'].update(mastery_output)

                        if images[default[index]] == "":
                            filepath = image_default[0]
                            window['-IMAGE-'].update(filename=filepath)  # shows blank image on screen
                        else:
                            filepath = images[default[index]]
                            window['-IMAGE-'].update(filename=filepath)  # shows image that corresponds to the question on screen

                    elif any(answer in values['-INPUT-'].lower() for answer in
                             automark[default[index]]):  # shows the answer was correct but missing some key points
                        window['-OUTPUTA-'].update(answers[default[index]])
                        window['-OUTPUTB-'].update(markscheme[default[index]])
                        window['-OUTPUTC-'].update(values['-INPUT-'].lower())
                        window['-OUTPUTD-'].update('partially correct')
                        window['-INPUT-'].update(disabled=True)
                        window['b1'].update(disabled=True)

                        mastery_output = "mastery:" + str(mastery[default[index]]) + "/3"

                        window['-MASTERY-'].update(mastery_output)

                        partiallycorrect[default[index]] += 1

                        allow = False

                    else:
                        window['-OUTPUTA-'].update(
                            answers[default[index]])  # shows that the answer is incorrect and displays the right answer
                        window['-OUTPUTB-'].update(markscheme[default[index]])
                        window['-OUTPUTC-'].update(values['-INPUT-'].lower())
                        window['-OUTPUTD-'].update('incorrect')
                        window['-INPUT-'].update(disabled=True)
                        window['b1'].update(disabled=True)

                        mastery_output = "mastery:" + str(mastery[default[index]]) + "/3"

                        window['-MASTERY-'].update(mastery_output)  # outputs mastery to the screen

                        incorrect[default[index]] += 1
                        current_incorrect[default[index]] += 1

                        if mastery[default[index]] == 0:
                            print(mastery)
                        else:
                            mastery[default[index]] -= 1
                            print(mastery)

                        allow = False

                    submit_button_clicked = 0

            if event == 'Skip' or submit_button_clicked == 1:
                index += 1
                if index > max_q_no:
                    index = 0

                while select_not_mastered_question:  # make sures the next question has not already been mastered
                    if index > max_q_no:
                        index = 0
                    else:
                        if mastery[default[index]] == 3:
                            index += 1
                        else:
                            select_not_mastered_question = False

                question_length = len(question[default[index]])

                # adjusts the question to fit on screen

                if question_length <= 30:
                    window['-OUTPUT-'].update(question[default[index]])
                    window['-OUTPUT2-'].update('')
                    window['-OUTPUT3-'].update('')
                    window['-OUTPUT4-'].update('')
                elif 30 < question_length < 86:
                    window['-OUTPUT-'].update(question[default[index]][0:30])
                    window['-OUTPUT2-'].update(question[default[index]][30:question_length])
                    window['-OUTPUT3-'].update('')
                    window['-OUTPUT4-'].update('')
                elif 86 < question_length < 142:
                    window['-OUTPUT-'].update(question[default[index]][0:30])
                    window['-OUTPUT2-'].update(question[default[index]][30:86])
                    window['-OUTPUT3-'].update(question[default[index]][86:142])
                    window['-OUTPUT4-'].update('')
                else:
                    window['-OUTPUT-'].update(question[default[index]][0:30])
                    window['-OUTPUT2-'].update(question[default[index]][30:86])
                    window['-OUTPUT3-'].update(question[default[index]][86:142])
                    window['-OUTPUT4-'].update(question[default[index]][142:question_length])

                window['-OUTPUTA-'].update('')
                window['-OUTPUTB-'].update('')
                window['-OUTPUTC-'].update('')
                window['-OUTPUTD-'].update('')

                mastery_output = "mastery:" + str(mastery[default[index]]) + "/3"

                window['-MASTERY-'].update(mastery_output)

                if selected == 2:
                    index = 0

                if images[default[index]] == "":
                    filepath = image_default[0]
                    window['-IMAGE-'].update(filename=filepath)  # shows blank image on screen
                else:
                    filepath = images[default[index]]
                    window['-IMAGE-'].update(filename=filepath)  # shows image that corresponds to the question on screen

                window['-INPUT-'].update(disabled=False)
                window['b1'].update(disabled=False)
                allow = True
                submit_button_clicked = 0

        if selected == 2:
            file.close()
            if event == 's2':
                index = 0

                # Pie chart, where the slices will be ordered and plotted counter-clockwise:
                labels = 'Correct', 'Incorrect', 'Partially correct'  # adds labels to the pie chart
                sizes = [total_correct, total_partially_correct, total_incorrect]
                explode = (0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

                # add colors
                colors = ['#99ff99', '#ff9999', '#66b3ff']
                fig1, ax1 = plt.subplots()
                ax1.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
                        shadow=True, startangle=90)  # Equal aspect ratio ensures that pie is drawn as a circle
                ax1.axis('equal')
                plt.tight_layout()
                plt.show()  # creates the window

    window.close()


main()
