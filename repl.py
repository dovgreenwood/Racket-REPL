"""
@author Dov Greenwood
@date February 6, 2020
@description Opens a (quasi-)REPL for racket programming that loads the specified racket file for use.
Idk if this can be done already and I just haven't figured out how, but DrRacket is an ugly pain in the ass
and I wanted an alternative.
Please don't mess up your Racket code because I definitely have a bunch of uncaught exceptions that I haven't considered.
"""


import os
import sys


#gets the file path, if specified, else exits the program
if len(sys.argv) == 1 or len(sys.argv) > 2:
    sys.exit("Error, " + str(len(sys.argv) - 1) + " files specified.")
path = sys.argv[1]
path = str('.' if (path[0] == '\\') else '.\\') + path


#creates a backup file to work in; deleted upon closing the REPL
os.system('copy ' + path + ' functions.rkt')


vars = []                                   #stores variable names so names are not repeated
with open('functions.rkt', 'r') as get_vars:
    for ln in get_vars.readlines():
        if '(define' in ln:
            words = ln.split(' ')
            name = words[words.index('(define') + 1].strip('()')
            vars.append(name)

ln_count = 1                                #stores the number of lines inputted per block

paren_count = 0                             #stores the number of close parens still needed

definition = False

def erase():                                #erases the command(s) from the file
    with open('functions.rkt', 'r+') as f_erase:
        f_erase.seek(0, os.SEEK_END)
        pos = f_erase.tell() - 1
        for i in range(ln_count):
            while pos > 0 and f_erase.read(1) != '\n':
                pos -= 1
                f_erase.seek(pos, os.SEEK_SET)
            pos -= 1
            f_erase.seek(pos, os.SEEK_SET)
            f_erase.truncate()


while True:
    line = input('> ')                                #get line to write to repl
    if len(line) == 0:
        continue

    if line == ';exit' or line == ';quit':            #deletes the REPL file copy and exits the REPL
        os.system('del functions.rkt')
        break

    if line[:7] == '(define':                         #makes sure definitions are not deleted
        name = line.split(' ')[1].strip('()')
        if name in vars:
            print('Error: variable name already taken.')
            continue
        vars.append(name)
        definition = True

    paren_count = paren_count + line.count('(') - line.count(')') #trackes the number of parenthesis needed to close the call

    with open('functions.rkt', 'a') as f_write:        #write the REPL line to the file
        f_write.write('\n' + line)

    if paren_count == 0:
        if definition == False:
            os.system('racket functions.rkt')          #run the repl
            print('\n')

            erase()                                    #erases the command(s) from the file
            ln_count = 0

    if definition == False:                            #adds to the line count if not a definition
        ln_count += 1

    if paren_count == 0:                               #closes a definition if all parentheses are closed
        definition = False
