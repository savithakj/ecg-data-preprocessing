How to Use:

1)install the requirements
    pip install -r requirements.txt

2) python3 merge_files.py <location of qrsData.mat> <location of qrsData1012Coord_sr3_corrected.mat> <master1012.xlsx>

    this will generate data.pickle file , persons.csv , master_data.mat in the current directory location.
    These files are used in the application.I have already done this step and generated the 2 files.


3)python3 gui.py

    This runs the application.
    Patient ID from 1-39 is listed along with their statistics of " not good instances".
    When you click on the patient id,all the unique pacing sites are listed.

    Pacing sites along with the Statistics is listed as buttons.Upon selection,each lead is plotted
     and the 3 options to classifiy that instance would be listed.

     Redo Record      |---> creates a file with details and
     Redo Pacing Site |      makes the option in persons.csv
     Stat Wrong       |

