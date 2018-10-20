from tkinter import *
from tkinter import Tk, Label, Button
from plotter import plotter
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import patientIds
import tkinter as tk
# import yaml
import os.path
import patient
import plotter
import pickle
import csv

COLOR = 'BLACK'


class Application(Frame):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.dynamicFrames = []
        self.dynamicPlots = []
        self.initIndexes()
        self.coord = None
        self.label = None

    def initIndexes(self):
        self.coordIdx = 0
        self.pId = 0

    def patientObjects(self):
        patientObjects = None
        with open("data.pickle", 'rb') as f:
            unpickler = pickle.Unpickler(f)
            patientObjects = unpickler.load()
        return patientObjects

    def initializeGrid(self):
        self.grid(row=0, column=0, sticky=N + S + E + W)
        for row in range(0, 13):
            Grid.rowconfigure(self, row, weight=1)
        for column in range(0, 27):
            Grid.columnconfigure(self, column, weight=1)

    def initUI(self):
        self.master.title("ECG Validator")
        self.initializeGrid()
        patientIdFrame = patientIds.patientButtonFrame(self,
                                                       self.patientObjects())
        patientIdFrame.grid(row=0,
                            column=0,
                            columnspan=6,
                            rowspan=7,
                            sticky=W + E + N + S)

    def onClickPatient(self, patient):
        self.initIndexes()
        self.clearDynamicFrames(self.dynamicFrames)

        pacingSiteFrame = patientIds.pacingSiteFrame(self, patient)
        pacingSiteFrame.grid(row=7,
                             column=0,
                             columnspan=6,
                             rowspan=7,
                             sticky=W + E + N + S)

        self.dynamicFrames.append(pacingSiteFrame)

    def onClickCoordinate(self, coord):
        self.coord = None
        self.initIndexes()
        self.addButtonsBelowImage()
        self.showPlot(coord)

    def clearDynamicFrames(self, dynamicFrames):
        for frame in dynamicFrames:
            dynamicFrames.remove(frame)
            frame.grid_forget()
            frame.destroy()

    def showStat(self):
        frame = Frame(self)
        frame.grid()
        stat = Label(frame, text='hhh')
        Grid.rowconfigure(frame, 1, weight=1)
        Grid.columnconfigure(frame, 1, weight=1)
        frame.grid(row=1, column=6, rowspan=1, columnspan=21, sticky=W + E + N + S)

    def showPlot(self, coord):
        print('loading frame')
        self.showStatus(coord.samples_stat[self.coordIdx])

        self.coord = coord
        subplot, a = plotter.plotter(coord.samples[self.coordIdx])
        canvas = FigureCanvasTkAgg(subplot, master=self)
        canvas.show()
        self.clearDynamicFrames(self.dynamicPlots)
        frame = canvas.get_tk_widget()
        self.dynamicPlots.append(frame)

        Grid.rowconfigure(frame, 1, weight=1)
        Grid.columnconfigure(frame, 1, weight=1)

        frame.grid(row=1,
                   column=6,
                   columnspan=21,
                   rowspan=11,
                   sticky=W + E + N + S)
        print("done")

    def nextPlot(self):
        coord = self.coord
        if (self.coordIdx >= 0):
            if (coord.samples[self.coordIdx]):
                self.coordIdx += 1
                self.showPlot(coord)

    def prevPlot(self):
        coord = self.coord
        if (self.coordIdx >= 0):
            if (coord.samples[self.coordIdx]):
                print(coord.samples_stat[self.coordIdx])
                print(coord.samples_index)
                self.coordIdx -= 1
                self.showPlot(coord)

    def showStatus(self, ltext):
        if (self.label == None):
            frame = Frame(self)
            frame.grid()

            Grid.rowconfigure(frame, 0, pad=3, weight=1)
            Grid.columnconfigure(frame, 0, pad=3, weight=1)
            self.label = Label(frame, text=ltext)
            self.label.grid(row=0, column=0, columnspan=21)
            frame.grid(row=0, column=6, rowspan=1, columnspan=21, sticky=W + E + N + S)
        else:
            self.label.config(text=ltext)

    def addButtonsBelowImage(self):
        frame = Frame(self)
        frame.grid()

        Grid.rowconfigure(frame, 0, pad=3, weight=1)
        for col in range(0, 24):
            Grid.columnconfigure(frame, col, pad=3, weight=1)

        prevButton = Button(frame, text="prev")
        nextButton = Button(frame, text="next", command=self.nextPlot)
        redothisrecord = lambda: self.create_redo_record()
        redothispace = lambda: self.create_redo_pace()
        statwrong = lambda: self.statwrong_file()

        redoThisRecordButton = Button(frame, text="Redo This Record", command=redothisrecord)
        redoEntireButton = Button(frame, text="Redo Entire Pacing Site", command=redothispace)
        statsWrongButton = Button(frame, text="Stats Wrong", command=statwrong)

        prevButton.grid(row=0,
                        column=0,
                        columnspan=5,
                        sticky=W + E + N + S)

        redoThisRecordButton.grid(row=0,
                                  column=5,
                                  columnspan=5,
                                  sticky=W + E + N + S)

        redoEntireButton.grid(row=0,
                              column=10,
                              columnspan=5,
                              sticky=W + E + N + S)

        statsWrongButton.grid(row=0,
                              column=15,
                              columnspan=5,
                              sticky=W + E + N + S)

        nextButton.grid(row=0,
                        column=20,
                        columnspan=5,
                        sticky=W + E + N + S)

        frame.grid(row=12, column=6, rowspan=2, columnspan=21, sticky=W + E + N + S)

    def create_redo_record(self):
        directory = './pacingsite'
        if not os.path.exists(directory):
            os.makedirs(directory)

        coord = self.coord
        filename = str(coord.file_name) + '.txt'
        with open(os.path.join(directory, filename), 'w') as f:
            f.write("Pacing Site :{}\n".format(coord.pacingSite))
            f.write("File Name : file{}.big\n".format(coord.file_name))
            f.write("Record : {}\n".format(coord.samples_stat[self.coordIdx]))
            f.write(' Record Index :{} \n'.format(coord.samples_index[self.coordIdx]))

        f.close()
        print(filename + ' created')
        newfile = []
        with open('persons.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if int(row[2]) == int(coord.samples_index[self.coordIdx]):
                    row.pop(4)
                    row.append('Redo Record')
                    newfile.append(row)

                else:
                    newfile.append(row)

        with open('persons.csv', 'w') as csvfile:

            filewriter = csv.writer(csvfile, delimiter=',',
                                    lineterminator='\n')
            for row in newfile:
                filewriter.writerow(row)
        print("csv wrote")

    def create_redo_pace(self):
        directory = './record'
        if not os.path.exists(directory):
            os.makedirs(directory)
        coord = self.coord
        filename = str(coord.file_name) + '.txt'
        with open(os.path.join(directory, filename), 'w') as f:
            f.write("Pacing Site :{}\n".format(coord.pacingSite))
            f.write("File Name : file{}.big\n".format(coord.file_name))
            f.write('Stat:{}\n'.format(coord.stats))
            f.write('Pace Start Index :{} \n'.format(coord.samples_index[self.coordIdx] - self.coordIdx))
            f.write('Pace End Index : {} \n'.format(
                (coord.samples_index[self.coordIdx] - self.coordIdx) + len(coord.samples_index) - 1))
        f.close()

        newfile = []
        with open('persons.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if int(row[2]) in list(range(coord.samples_index[self.coordIdx] - self.coordIdx,
                                             coord.samples_index[self.coordIdx] - self.coordIdx + len(
                                                 coord.samples_index))):
                    row.pop(4)
                    row.append('Redo Pacing Site')
                    newfile.append(row)

                else:
                    newfile.append(row)

        with open('persons.csv', 'w') as csvfile:

            filewriter = csv.writer(csvfile, delimiter=',',
                                    lineterminator='\n')
            for row in newfile:
                filewriter.writerow(row)
            print("csv wrote")

            print(filename + ' created')

    def statwrong_file(self):
        directory = './statwrong'
        if not os.path.exists(directory):
            os.makedirs(directory)
        coord = self.coord
        filename = str(coord.file_name) + '.txt'
        with open(os.path.join(directory, filename), 'w') as f:
            f.write("Pacing Site :{}\n".format(coord.pacingSite))
            f.write("File Name : file{}.big\n".format(coord.file_name))
            f.write('Stat:{}\n'.format(coord.stats))
            f.write("Record : {}\n".format(coord.samples_stat[self.coordIdx]))
            f.write('Pace Start Index :{} \n'.format(coord.samples_index[self.coordIdx]))

        f.close()
        print(filename + ' created')
        newfile = []
        with open('persons.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if int(row[2]) == int(coord.samples_index[self.coordIdx]):
                    row.pop(4)
                    row.append('Stat wrong')
                    newfile.append(row)

                else:
                    newfile.append(row)

        with open('persons.csv', 'w') as csvfile:

            filewriter = csv.writer(csvfile, delimiter=',',
                                    lineterminator='\n')
            for row in newfile:
                filewriter.writerow(row)
        print("csv wrote")


def main():
    root = Tk()
    Grid.rowconfigure(root, 0, weight=1)
    Grid.columnconfigure(root, 0, weight=1)
    app = Application()
    root.mainloop()


if __name__ == '__main__':
    main()
