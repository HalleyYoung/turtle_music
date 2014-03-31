import math
from music21 import *

ruleTypes = ["F", "f", "+", "-"]

print("Welcome to the turtle music generator! This program generates music based on a simple game.  Here's how the game works:")
print("There are four symbols: F, f, +, -.  The program will start with a single F, and then substitute that symbol for a list of other symbols according to rules that you specify.  It will do this four times.")
print("Then the symbols will be turned into music.  The music is based on the movement of a turtle, which starts at middle C. F means that the program moves the turtle, and then \"draws a line\" from its old to its new position by creating a note.  f makes the turtle move, but no note is added.  + and - change the direction that the turtle move.  Horizontal movement corresponds to note length, while vertical movement corresponds to note pitch.")
rules = {}
symbols = ['F', 'f', '+', '-']
for s in symbols:
    existsRule = raw_input("Do you want to include a rule for " + s + " (y/n)? ") == "y"
    if (existsRule):
        rules[s] = raw_input("What do you want your rule to be (example: FF+F+F+F+F+F-F)? ")
#rules['F'] = "FF+F+F+F+F+F-F" 
start_string = "F"

#rules['A'] = "AB"
#rules['B'] = "A"

iterations = 3

def createNote(pitch, length):
    n = note.Note()
    n.pitch.octave = pitch/12
    n.pitch.pitchClass = pitch%12
    n.duration.quarterLength = length
    return n       

def genLSystem(iterations, start_string, rules):
    if (iterations == 1):
        return start_string
    else:
        new_string = ""
        for i in range(0, len(start_string)):
            if start_string[i] in rules:
                new_string += genLSystem(iterations - 1, rules[start_string[i]], rules)
            else:
                new_string += start_string[i]
        return new_string       
        
#creates a list of notes         
def genTurtleNotes(instructions, start_note_pitch, start_direction, direction_step_size):
    cur_note_pitch = start_note_pitch
    cur_note_length = 0
    notes = []
    direction = 0 #0 is straight horizontal motion, no change in pitch    
    #pitch and length remapped so that all note lengths are multiples of 16ths and all pitches are ints
    def remap_length(x): 
        if x % 0.25 == 0:
            return x
        else:
            return x - x%0.25 
    def remap_pitch(x):
        #print(x)
        #print (int(3*x))
        return int(3*x) #may be changed later if I decide a different mapping works better
    for i in range(0, len(instructions)):
        s = instructions[i] #current symbol
        if s == 'F': #move forward and "draw" a new note
            cur_note_length += remap_length(abs(math.cos(math.pi*direction/180))) #length is "horizontal" motion
            cur_note_pitch += remap_pitch(math.sin(math.pi*direction/180)) #pitch is "vertical" motion
            n = createNote(cur_note_pitch, cur_note_length)
            notes.append(n)
            cur_note_length = 0
        elif (s == 'f'): #move forward in time/notes, but don't draw a new note
            cur_note_length += remap_length(abs(math.cos(math.pi*direction))) #remapped so that all notes are multiples of 16ths
            cur_note_pitch += remap_pitch(math.sin(math.pi*direction)) #pitch is "vertical" motion
        elif (s == '+'):
            direction += direction_step_size
        elif (s == '-'):
            direction -= direction_step_size
    return notes       
    #using modified sin/cos 60 = 
        
    
        
instructions = genLSystem(iterations, start_string, rules)
notes = genTurtleNotes(instructions, 48, 0, 60)

s = stream.Stream()
for i in range(0, len(notes)):
    s.append(notes[i])
    
midiname = raw_input("What do you want your midi file to be called? ")

mf = midi.translate.streamToMidiFile(s)
mf.open(midiname, 'wb')
mf.write()
mf.close()    

print("Your file has been created!")