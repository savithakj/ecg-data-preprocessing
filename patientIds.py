from tkinter import *
from tkinter import Tk, W, E, N, S
from tkinter.ttk import Frame, Button, Entry, Style
import math

def patientButtonFrame(master, ids):
    frame = Frame(master)
    frame.grid()

    for row in range(0, 7):
        Grid.rowconfigure(frame, row, pad=3, weight=1)

    for col in range(0, 6):
        Grid.columnconfigure(frame, col, pad=3, weight=1)


    idx = 0
    for row in range(0, 7):
        for column in range(0, 6):
            if idx < len(ids):
                patient = ids[idx]
                idx += 1
                anonFunc = lambda patient=patient: master.onClickPatient(patient)
                button = Button(frame,
                                text="{0}, stat: {1}".format(patient.id, patient.stat),
                                command=anonFunc)
                button.grid(row=row, column=column, sticky= W+E+N+S)

    return frame

def pacingSiteFrame(master, patient):
    frame = Frame(master)
    frame.grid()
    rows = math.ceil(len(patient.pacing_coord) / 6.0)
    for row in range(0, rows):
        Grid.rowconfigure(frame, row, pad=3, weight=1)
    for col in range(0, 6):
        Grid.columnconfigure(frame, col, pad=3, weight=1)

    idx = 0
    for row in range(0, rows):
        for col in range(0, 6):
            if idx < len(patient.pacing_coord):
                coord = patient.pacing_coord[idx]
                idx += 1
                anonFunc = lambda coord=coord: master.onClickCoordinate(coord)
                button = Button(frame,
                                text="{0} stats:  {1}".format(coord.pacingSite, coord.stats),
                                command=anonFunc)
                button.grid(row=row, column=col, sticky= W+E+N+S)

    return frame
