# Author: Milan Matousek
# Oct 2020
import os 
import tkinter as tk
from tkinter import messagebox
from pygame import mixer

#global variables
global songs
global i
global hraje
global poprve
global song_name
global volume_value
volume_value = 1
song_name = '---'
poprve = 1
hraje = 1
i = 1
songs = []

# function return print of all mp3 files in current dict
def music_in_dir():
    global songs
    global i

    #fix if first item in listbox is this str and someone added mp3
    #this str remain as first item and song is add as second
    if 'No music found' in song_list.get(0):
        song_list.delete(0)

    for file in os.listdir():
        # check if file is mp3 and not already in our app
        if ('.mp3' in file) and (file not in songs):
            song_list.insert(i, file) #new item into listbox
            songs.append(file) #remember already claimed song
            print(songs)
            i = i + 1 # for work with listbox, need newline
            print(file) #debugging
        else:
            print('Uz to tam je') #debugging
    # no song detected
    if song_list.size() == 0:
        song_list.insert(1, 'No music found')

def start_stop_func():
    global hraje
    global poprve
    global song_name

    # fix if song is choosen
    if song_name == '---':
        return

    #first play
    if poprve == 1:
        poprve = 0
        start_stop.configure(text='||')
        mixer.music.load(song_name)
        mixer.music.play()
        print('1')
    #pause
    elif hraje == 1:
        hraje = 0
        start_stop.configure(text='|>')
        mixer.music.pause()
        print('2')
    #unpause
    else:
        hraje = 1
        start_stop.configure(text='||')
        mixer.music.unpause()
        print('3')

def back_func():
    global song_name
    global poprve
    global hraje

    t = sum(song_list.curselection()) # tuple to int

    if t == 0:
        print('Zacatek seznamu')
    elif t == 0 and len(songs) == 0:
        print('No songs aviable')
    else:
        mixer.music.stop() #stop playing music
        #print('Muzeme zmenit song')
        # setup global variables
        hraje = 1 
        poprve = 1
        song_name = song_list.get(t-1) # song before our current song
        current_play.configure(text='Current playing: '+song_name) #update label
        print('----------'+song_name+'----------')
        start_stop_func()
        # this is very important! need to change index of item
        print('DEBUG')
        print(song_list.curselection())
        song_list.selection_clear(t)
        print(song_list.curselection())
        song_list.selection_set(t-1)
        print(song_list.curselection())
        print('DEBUG')

def forward_func():
    global song_name
    global poprve
    global hraje

    if song_list.size() == 0:
        #no item in list
        print('No item')
        return
    elif song_list.size() == 1 and song_list.get(0) == 'No music found':
        #no music found listbox
        print('No song in dict')
        return
    else:
        # continue work
        t = sum(song_list.curselection()) # tuple to int
        # lets fix if listbox item is choosen
        try:
            song_list.get(song_list.curselection()[0])
        except IndexError as e:
            print('No song choosen ({0})'.format(e))
            return
        # fint out if we are not at last song item
        if t < song_list.size() - 1:
            print('Muzu posunout')
            mixer.music.stop() # stop current playing music
            poprve = 1
            hraje = 1
            song_name = song_list.get(t+1) # song before our current song
            current_play.configure(text='Current playing: '+song_name) #update label
            start_stop_func()
            # this is very important! need to change index of item
            print('DEBUG')
            print(song_list.curselection())
            song_list.selection_clear(t)
            print(song_list.curselection())
            song_list.selection_set(t+1)
            print(song_list.curselection())
            print('DEBUG')
        else:
            #cant move forward
            print('Cant move forward')
            return

# function for helping how to workds with music player
def help_func():
    msg = '''Version: 0.5, just working for current dict.
Click on button for find songs then pick them and play'''
    messagebox.showinfo(title='Pomoc', message=msg)

#func for choosing music
def klik(param):
    global song_name
    global poprve
    global hraje

    #if there is song in listbox
    if song_list.get(song_list.curselection()[0]) != 'No music found':
        mixer.music.stop() # stop song before
        # reset global variables
        hraje = 1
        poprve = 1
        # setup new song name
        song_name = song_list.get(song_list.curselection()[0])
        # setup current song playing label for info
        current_play.configure(text='Current playing: '+song_name)
        start_stop.configure(text='|>') # just in case for GUI fixes

# change volume to up
def volumeChange(up=1):
    global volume_value
    
    print(mixer.music.get_volume())
    if up == 1:
        print('Zvysujeme')
        volume_value = volume_value + 0.1
        if volume_value > 1:
            volume_value = 1
        print(volume_value)
        mixer.music.set_volume(volume_value)
    else:
        print('Snizujeme')
        volume_value = volume_value - 0.1
        if volume_value < 0:
            volume_value = 0
        print(volume_value)
        mixer.music.set_volume(volume_value)

# main loop of app
def main():
    tk.mainloop()

#main things for TKINTER GUI
root = tk.Tk(className='[MMP]')
root.geometry("400x300") 
root.resizable(False, False) # no resize

#things connected to music
mixer.init()

#menu for help 
menubar = tk.Menu(root)
menubar.add_command(label='Help', command=help_func)
root.config(menu=menubar)

#label for current playing song
current_play = tk.Label(root, text='Current playing: '+song_name)
current_play.place(x=10, y=10)

#main controlling of music
back = tk.Button(root, text='|<')
back.configure(command=back_func)
back.place(x=10, y=30)

start_stop = tk.Button(root, text='|>')
start_stop.configure(command=start_stop_func)
start_stop.place(x=30, y=30)

forward = tk.Button(root, text='>|')
forward.configure(command=forward_func)
forward.place(x=50, y=30)

# volume
vol_down = tk.Button(root, text='- ')
vol_down.configure(command=lambda:volumeChange(0))
vol_down.place(x=75, y=30)
vol_up = tk.Button(root, text='+')
vol_up.configure(command=volumeChange)
vol_up.place(x=95, y=30)

#button for show all mp3 files in currend dict
current_dict = tk.Button(root, text='Search in dict')
current_dict.configure(command=music_in_dir)
current_dict.place(x=10, y=60)

#listbox for list of songs
frame = tk.Frame(root)
frame.place(x=10, y=90)
song_list = tk.Listbox(frame, height=10)
song_list.pack(side="left", fill="y")
#vertikalni scrollbar
scrollbar = tk.Scrollbar(frame, orient="vertical")
scrollbar.config(command=song_list.yview)
scrollbar.pack(side="right", fill="y")
#horizontální scrollbar
scrollbar2 = tk.Scrollbar(root, orient=tk.HORIZONTAL)
scrollbar2.config(command=song_list.xview)
scrollbar2.pack(side='bottom')
scrollbar2.place(x=10, y=255)

#what user click on
song_list.bind('<ButtonRelease-1>', klik)

#scrollbars connect to listbox
song_list.config(yscrollcommand=scrollbar.set)
song_list.config(xscrollcommand=scrollbar2.set)

if __name__ == '__main__':
    main()
