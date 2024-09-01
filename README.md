# Generate custom words-per-minute practice files for Steno Arcade

Generate a custom "song" from a text file, at a custom words-per-minute rate.
All instructions are for Windows.
tested with Python 3.10 and a RTX3070 GPU (GPU not needed, should default to CPU)

## Create a virtual environment in python 

    > python -m venv venv 
    > cd venv
    > cd Scripts
    > activate
    > cd../..

## install the requirements

    > pip install -r requirements.txt

## install the torch version that is actually compatible with your GPU's CUDA and python versions - this may not be the one TTS installed!

replace torch with the correct version for your system if the one pip installed when installing TTS does not work.
If you don't have a GPU it should automatically fall back to use your CPU, but you do still need torch. 

uninstall the one TTS installed for you
    
    > pip uninstall torch

and install the correct one (from a .whl file on my local harddisk in my case)

    > python -m pip install "torch-2.1.2+cu121-cp310-cp310-win_amd64.whl"

# How to generate the files for Steno Arcade

## Enter your words

You can manually type the words you want to practice in mytext.txt
or you can generate a  text file from the chapter lessons with [amount] words (you can set this variable in the script) from the Learning Lapwing book training files.

#### Use Lapwing lessons

In generate-training-textfile.py  change the wordcount and which chapter's lessons to include here

    #! Change these
    wordcount = 150 # Set this to how many words you want to see in StenoArcade
    startnumbers = [5, 4, 7, 8, 9] # which chapters from the Lapwing book training tests to include.

"Chapters to include" numbers correspond with the start numbers of the filenames in the **textfiles** folder

## Set your  WPM speed

in makeallfiles.py set your desired WPM and the name you want to see in StenoArcade for the  "song" - this name is also used for all filenames, probably best to not use spaces or weird symbols.

     
    # Words per minute
    wpm = 10
    # Your song title and the name of all the files
    thefilename = "practice01"


### Save your files so StenoArcade sees them

- move the .lrc file to C:\Program Files (x86)\Steam\steamapps\common\Steno Arcade\Steno Hero\Songs
- move the .png file to C:\Program Files (x86)\Steam\steamapps\common\Steno Arcade\Steno Hero\Songs\Art
- move the .ogg file to C:\Program Files (x86)\Steam\steamapps\common\Steno Arcade\Steno Hero\Songs\Audio

(you can add your own code to the script to automate this)

### Issues 

- Audio conversion is not always great (mispronounciations/garbled words, especailly with a model that allows you to clone a speaker voice.. but you can do this with the  make-all-files-custom-voice.py script) 
- Conversion is relatively slow
 
-----

#### Credits: 

/textfiles contains the original training files from https://github.com/aerickt/lapwing-for-beginners 
All Lapwing credit to AerickT