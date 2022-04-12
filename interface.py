import PySimpleGUI as sg
import main
import sys
import subprocess
import main
import pathlib
import re
import webbrowser

#initial setup
sg.theme('DarkAmber')
with open(main.DEFAULT_FILE, "r") as file:
    data = file.read()
    lines = data.split("\n")
layout = [  
            [sg.Text('Links to check:', size=(15, 1)), sg.InputText(key='-INPUT-', size=(80, 1), do_not_clear=False)],
            [sg.Listbox(values=lines, size=(100, 10), key='-OUTPUT-', no_scrollbar=True, right_click_menu=['&Right', ['Open Link', 'Copy Link']])],
            [sg.Button('Add'), sg.Button('Remove'), sg.Button('Check'), sg.Button('Exit')],
            [sg.Listbox(values='', size=(100, 10), visible=False, key="-CMDOUT-")]
        ]

window = sg.Window('Item availability bot', layout)

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == 'Exit':
        break

    # Add link to file when button is pressed
    if event == 'Add':
        # dont add if nothing is filled in
        if values['-INPUT-'] == '':
            continue
        with open(main.DEFAULT_FILE, "a") as file:
            # append with newline at the beginning so no empty line shows up in the list
            if file.tell() == 0:
                file.write(values['-INPUT-'])
            else:
                file.write(f"\n{values['-INPUT-']}")
                lines += [values['-INPUT-']]
                window['-OUTPUT-'].update(values=lines)

    # remove selected link from file and list
    if event == 'Remove':
        if values['-OUTPUT-'] == []:
            continue
        with open(main.DEFAULT_FILE, "w") as file:
            for line in lines:
                # rewrite whole file except the selected link
                if line != values['-OUTPUT-'][0]:
                    if file.tell() == 0:
                        file.write(f"{line}")
                    else:
                        file.write(f"\n{line}")
            lines.remove(values['-OUTPUT-'][0])
            # update listbox with lines
            window['-OUTPUT-'].update(values=lines)
            
    # execute check from main.py
    if event == 'Check':
        p = subprocess.Popen(f"C:\Python310\python.exe {pathlib.Path().resolve()}\main.py", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = []
        for line in p.stdout:    
            line = line.decode(errors='replace' if (sys.version_info) < (3, 5) else 'backslashreplace').rstrip()
            # remove color codes
            line = re.sub(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]' , '' , line)
            output += [line + "\n"]
        # update listbox with output
        window['-CMDOUT-'].update(values=output, visible=True)
    
    if event == 'Open Link':
        # open link in default browser
        webbrowser.open(values['-OUTPUT-'][0])