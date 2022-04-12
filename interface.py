from concurrent.futures import thread
import PySimpleGUI as sg
import main
import threading
import sys
import subprocess
import main

sg.theme('DarkAmber')
with open(main.DEFAULT_FILE, "r") as file:
    data = file.read()
    lines = data.split("\n")
layout = [  [sg.Text('Link to check:', size=(15, 1)), sg.InputText(key='-INPUT-', size=(80, 1), do_not_clear=False)],
            [sg.Listbox(values=lines, size=(100, 10), key='-OUTPUT-')],
            [ sg.Button('Add'), sg.Button('Remove'), sg.Button('Check'), sg.Button('Exit')]]

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
            window['-OUTPUT-'].update(values=lines)
    if event == 'Check':
        #thread = threading.Thread(target=main.main(), daemon=True)
        #thread.start()
        p = subprocess.Popen("C:\Python310\python.exe C:\Repositories\Item-availability-bot\main.py", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = ''
        for line in p.stdout:    
            line = line.decode(errors='replace' if (sys.version_info) < (3, 5) else 'backslashreplace').rstrip()
            if "stock" not in line:
                continue
            output += line
            print(line)
        layout = [  [sg.Text('Link to check:', size=(15, 1)), sg.InputText(key='-INPUT-', size=(80, 1), do_not_clear=False)],
                    [sg.Listbox(values=lines, size=(100, 10), key='-OUTPUT-')],
                    [sg.Button('Add'), sg.Button('Remove'), sg.Button('Check'), sg.Button('Exit')],
                    [sg.Text(output, size=(100, 10))]]
        temp = sg.Window('Item availability bot', layout)
        window.close()
        window = temp
        #thread.join()
