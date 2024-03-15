#
#   The purpose of this project is to serve as a main interface for managing video and audio file manipulation and
#   video to audio conversions. This program serves as the interface for VideotoAudioConverter.py
#
#   How it works:
#   1:  Creates a window using tkinter
#   2:  Has a drop down menu to select what function you want to use
#   3:  Once function is selected you can confirm it with a button click
#       -   This changes the parameter text to show what is required for it to run
#   4:  Once text is inputted in the text boxes you can run the function with the next button
#   5:  The program handles the function selection and the input text from the text boxes to run the function
#
#   Future plans:
#   1:  Implement threading to allow the tkinter window to be responsive while running the underlying program
#       - Note that to reduce CPU load it would be wise to only run VideotoAudioConverter functions one at a time
#   2:  Implement a way to better handle mutagen tag input
#   3:  Implement a way to better handle chapter splitting input
#   4:  Clean code for increased efficiency and decreased clutter
#

#--------------------------------------------CODE STARTS HERE---------------------------------------------

from tkinter import *
from tkinter.ttk import *
import VideotoAudioConverter as VC

#   This part is for creating the window
root = Tk()
root.geometry("900x310")
root.title("Video to Audio Converter")

''' Changes the three parameter labels to show what the selected function requires. Null = no variable needed
    Runs when button1 is clicked
    @Params:    None
    @Returns:   None'''
def show_params():
    params = None
    if clicked.get() == "Add Tags":
        params = param_list[0]
    elif clicked.get() == "Download from YouTube (Single)":
        params = param_list[1]
    elif clicked.get() == "Download from YouTube (Playlist)":
        params = param_list[2]        
    elif clicked.get() == "Convert MP4 to MP3 (Single)":
        params = param_list[3]
    elif clicked.get() == "Convert MP4 to MP3 (Multiple)":
        params = param_list[4]
    elif clicked.get() == "Check File Extensions":
        params = param_list[5]
    elif clicked.get() == "Remove Files with Extension":
        params = param_list[6]
    elif clicked.get() == "Split Video by Chapter":
        params = param_list[7]
    elif clicked.get() == "Move File":
        params = param_list[8]
    elif clicked.get() == "The Full Package":
        params = param_list[9]
    elif clicked.get() == "Increase Volume (Single)":
        params = param_list[10]
    if params != None:
        l1.config(text = f"Parameter 1: {params[0]}")
        l2.config(text = f"Parameter 2: {params[1]}")
        l3.config(text = f"Parameter 3: {params[2]}")

''' Formats the parameters into the right variable type and runs the function from the VC object
    @Params:    None
    @Returns:   None'''
def execute():
    if clicked.get() == "Add Tags":
        formatted_params = format_params()        
        VC.add_tags(inputpath.get('1.0', 'end-1c'), formatted_params[0], formatted_params[1])
    elif clicked.get() == "Download from YouTube (Single)":
        formatted_params = format_params()        
        VC.youtube_dlp(inputpath.get("1.0", "end-1c"), formatted_params[0], formatted_params[1])
    elif clicked.get() == "Download from YouTube (Playlist)":
        formatted_params = format_params()        
        VC.youtube_dlp(inputpath.get("1.0", "end-1c"), formatted_params[0], formatted_params[1])        
    elif clicked.get() == "Convert MP4 to MP3 (Single)":
        VC.convert_video_to_audio(inputpath.get("1.0", "end-1c"))
    elif clicked.get() == "Convert MP4 to MP3 (Multiple)":
        VC.mass_convert_to_mp3(inputpath.get("1.0", "end-1c"))
    elif clicked.get() == "Check File Extensions":      
        VC.check_file_extensions(inputpath.get("1.0", "end-1c"))
    elif clicked.get() == "Remove Files with Extension":
        formatted_params = format_params()        
        VC.remove_files_with_extension(inputpath.get("1.0", "end-1c"), formatted_params[0])
    elif clicked.get() == "Split Video by Chapter":
        formatted_params = format_params()        
        VC.youtube_dlp(inputpath.get("1.0", "end-1c"), formatted_params[0], formatted_params[1])
    elif clicked.get() == "Move File":
        formatted_params = format_params()        
        VC.move_file(inputpath.get("1.0", "end-1c"), formatted_params[0])
    elif clicked.get() == "The Full Package":
        formatted_params = format_params()           
        VC.the_full_package(inputpath.get("1.0", "end-1c"),formatted_params[0], formatted_params[1])
    elif clicked.get() == "Increase Volume (Single)":        
        VC.increase_volume(inputpath.get("1.0", "end-1c"))          

''' Formats the parameters into the correct variable type
    @Params:    None
    @Returns:   formatted_params    |   List            |   Formatted parameters depending on what is required by the VideotoAudioConverter function
                parameter2          |   String or List  |   Formatted text from the second input box in the window. Type depends on the VideotoAudioConverter function
                parameter3          |   String or List  |   Formatted text from the third input box in the window. Type depends on the VideotoAudioConverter function'''
def format_params():
    parameter2 = param_2.get("1.0", "end-1c")
    if ", " in parameter2:
        parameter2 = parameter2.split(", ")
    parameter3 = param_3.get("1.0", "end-1c")
    if ", " in parameter3:
        parameter3 = parameter3.split(", ")
    return parameter2, parameter3

#   Creates all of the features to be placed in the window
l1 = Label(text = "Parameter 1:")
l2 = Label(text = "Parameter 2:")
l3 = Label(text = "Parameter 3:")
inputpath = Text(root, height = 1, width = 50, bg = "light cyan")
param_2 = Text(root, height = 2, width = 50, bg = "light cyan")
param_3 = Text(root, height = 2, width = 50, bg = "light cyan")
options = ["Nothing","Add Tags", "Check File Extensions", "Convert MP4 to MP3 (Single)", "Convert MP4 to MP3 (Multiple)", "Download from YouTube (Single)", 
           "Download from YouTube (Playlist)", "Increase Volume (Single)", "Move File", "Remove Files with Extension", "Split Video by Chapter", "The Full Package"]
clicked = StringVar()       # Datatype of menu text
clicked.set("Nothing")      # Initial menu text
drop = OptionMenu( root , clicked , *options )                      # Create Dropdown menu
button1 = Button( root , text = "Confirm" , command = show_params)  # Create button, it will change label text
button2 = Button( root , text = "Select" , command = execute)       # Create button, it will change label text
param_list = [["Path", "Tags (list)", "Order (list)"], ["Path", "Link", "Null"], ["Path", "Link", "Null"], ["Path (to MP4)", "Null", "Null"], ["Path", "Null", "Null"], 
              ["Path", "Null", "Null"], ["Path", "File_type", "Null"], ["Path", "Chapters (list)", "Names (list)"], ["Path", "Path_out", "Null"],
              ["Path", "Link", "Mode (Single/Playlist)"], ["Path (to MP3)", "Null", "Null"]]
  
# Places all of the visuals in the window
drop.place(x = 200, y = 10)
button1.place(x = 425, y = 10)
l1.place(x = 0, y = 50)
inputpath.place(x = 225, y = 50)
l2.place(x = 0, y = 90)
param_2.place(x = 225, y = 90)
l3.place(x = 0, y = 130)
param_3.place(x = 225, y = 130)
button2.place(x = 425, y = 200)
 
mainloop()
