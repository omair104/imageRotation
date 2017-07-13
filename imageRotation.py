# -*- coding: utf-8 -*-
"""
Created on Sep 01 14:00:25 2016

@author: Babri
"""
#comment
import os
import sys
import Tkinter
#import Tkconstants
from Tkinter import Toplevel
import tkFileDialog

import re
import subprocess

import struct
import imghdr
from shutil import copyfile

#For third party libraies
try:
    our_location = os.path.realpath(os.path.abspath(os.path.dirname(__file__)))
    print(our_location)
except:
    our_location = os.path.abspath(os.path.normpath(os.path.dirname(sys.argv[0])))

__base_dir = our_location
__libs_dir = os.path.join(__base_dir, 'thirdparty')

sys.path.insert(0, __base_dir)
sys.path.insert(0, __libs_dir)

#import psutil



def countFiles(directory):
    files = []

    if os.path.isdir(directory):
        for path, dirs, filenames in os.walk(directory):
            files.extend(filenames)

    return len(files)

def makedirs(dest):
    if not os.path.exists(dest):
        os.makedirs(dest)





class Application(Tkinter.Frame):
       
    def __init__(self, directory, master=None):
        
        self.directory=directory        
        Tkinter.Frame.__init__(self, master)
        self.pack()
        self.createWidgets()



    def createWidgets(self):
        self.QUIT = Tkinter.Button(self, width=10, fg = "red", font =('bold',18))
        self.QUIT["text"] = "EXIT"
        self.QUIT["fg"]   = "red"
        self.QUIT["command"] =  self.quit

        #self.QUIT.pack({"side": "right"})
        #default is side = Top
        self.QUIT.grid(row=28, sticky = 'E', pady=10)




        #------------------------------------------- WIDGETS ON MAIN GUI -------------------------------------------

        self.convertlabel=Tkinter.Label(self, text='IMAGE ROTATION',font=('bold',16)).grid(row=16, pady=2, sticky='W')


        self.label1 = Tkinter.Label(self, text='Enter text file location:').grid(row=17, sticky='W')
        # Entry box for text file
        self.textpath = Tkinter.Entry(self, width=80)
        self.textpath.grid(row=18, sticky='W')
        #self.textpath.insert(0, 'C:/Users/BabriO/Downloads/WesternMiddleHarbourSectionC_TestBearings.txt')
        # button for askdirectory
        self.askbutton1 = Tkinter.Button(self, text='browse', command=self.askdirectory_text).grid(row=18, column=1)


        self.label2=Tkinter.Label(self, text='Enter source folder location:').grid(row=19, sticky='W')
        #Entry box for input path
        self.dpxpath=Tkinter.Entry(self, width=80)
        self.dpxpath.grid(row=20, sticky='W')
        #self.dpxpath.insert(0, 'C:/Users/BabriO/Downloads/input_images')
        #button for askdirectory
        self.askbutton3= Tkinter.Button(self, text='browse', command=self.askdirectory_input).grid(row=20, column=1)
        
        self.label4=Tkinter.Label(self, text='Enter rotated folder location:').grid(row=21, sticky='W')
        #Entry box for input path
        self.rotatedpath=Tkinter.Entry(self, width=80)
        self.rotatedpath.grid(row=22, sticky='W')
        #self.rotatedpath.insert(0, 'C:/Users/BabriO/Downloads/output_images2')
        #button for askdirectory
        self.askbutton3= Tkinter.Button(self, text='browse', command=self.askdirectory_rotated).grid(row=22, column=1)


        self.label3=Tkinter.Label(self, text='Enter destination folder location:').grid(row=23, sticky='W')
        #Entry box for output path
        self.outputpath=Tkinter.Entry(self, width=80)
        self.outputpath.grid(row=24, sticky='W')
        #self.outputpath.insert(0, 'C:/Users/BabriO/Downloads/output_images3')
        #button for askdirectory
        self.askbutton4= Tkinter.Button(self, text='browse', command=self.askdirectory_output).grid(row=24, column=1)


        self.label4=Tkinter.Label(self, text='Enter angle of rotation in degrees:').grid(row=25, sticky='W')
        #Entry box for output path
        self.degreepath=Tkinter.Entry(self, width=10)
        self.degreepath.grid(row=26, sticky='W')
        #self.degreepath.insert(0, '180')



        #button for converting
        self.convertbutton = Tkinter.Button(self, width=10, text='ROTATE',font=('bold',18), command=self.convert1)
        self.convertbutton.grid(row=27, pady=10, sticky='W')
        
        #button for converting
        self.convertbutton2 = Tkinter.Button(self, width=10, text='RESIZE',font=('bold',18), command=self.convert2)
        self.convertbutton2.grid(row=28, pady=10, sticky='W')




    def askdirectory_text(self):
        #self.directory = tkFileDialog.askdirectory(**self.dir_opt)
        self.textdirectory = tkFileDialog.askopenfilename(filetypes=[("Text files","*.txt")])
        self.textpath.delete(0,100)
        self.textpath.insert(0,self.textdirectory)


    def askdirectory_input(self):
        #self.directory = tkFileDialog.askdirectory(**self.dir_opt)
        self.dpxdirectory = tkFileDialog.askdirectory()
        self.dpxpath.delete(0,100)
        self.dpxpath.insert(0,self.dpxdirectory)
        
    def askdirectory_rotated(self):
        #self.directory = tkFileDialog.askdirectory(**self.dir_opt)
        self.rotateddirectory = tkFileDialog.askdirectory()
        self.rotatedpath.delete(0,100)
        self.rotatedpath.insert(0,self.rotateddirectory)
        
    def askdirectory_output(self):
        #self.directory = tkFileDialog.askdirectory(**self.dir_opt)
        self.outputdirectory = tkFileDialog.askdirectory()
        self.outputpath.delete(0,100)
        self.outputpath.insert(0,self.outputdirectory)



    def display_error(self, text_message):
        top = Toplevel()
        x = self.master.winfo_rootx()
        y = self.master.winfo_rooty()
        top.geometry("+%d+%d" %(x+250,y+150))
        #top.geometry("+550+350")
        top.title('Error')
        Tkinter.Label(top, text=text_message).grid(row=1, sticky='W')
        Tkinter.Button(top, text="OK", command=top.destroy).grid(row=2)



    def convert_check(self):

        textlocation=self.textpath.get()
        self.inputlocation=self.dpxpath.get()
        self.outputlocation=self.outputpath.get()
        self.rotatedlocation=self.rotatedpath.get()
        self.degreelocation = self.degreepath.get()
        
        if not textlocation:
            text_message = "Please select text file"
            self.display_error(text_message)
            return
        else:
            self.dic = {}
            for line in open(textlocation, 'U'):
                if line.startswith('IMG'):
                    a = re.split(r'\t+', line)
                    a[1]= a[1].rstrip()
                    self.dic.update({a[0]:a[1]})

        if not self.inputlocation:
            text_message = "Please select source directory"
            self.display_error(text_message)
            return
        else:
            pass

        if not self.outputlocation:
            text_message = "Please select destination directory"
            self.display_error(text_message)
            return   
        else:
            pass
        
        if not self.rotatedlocation:
            text_message = "Please select destination directory"
            self.display_error(text_message)
            return
        else:
            pass
        
        if not self.degreelocation:
            text_message = "Please select angle of rotation"
            self.display_error(text_message)
            return
        else:
            pass
    
        makedirs(self.rotatedlocation)
        makedirs(self.outputlocation)
        
    def convert1(self):
        self.convert_check()
        self.rotateFiles(self.inputlocation, self.rotatedlocation)
        
    def convert2(self):
        self.convert_check()
        self.cropFiles(self.rotatedlocation, self.outputlocation)
    

    #------------------------------------------- FUNCTION WHICH IMPLEMENTS THE ACTUAL COPYING -------------------------------------------
    def rotateFiles(self, src, dest):
        numFiles = countFiles(src)
        if numFiles > 0:
            makedirs(dest)
            
            processing = {}
            for file in os.listdir(src):
                if file.endswith(".JPG") | file.endswith(".jpg"):
                    if file in self.dic:
                        inputImage = os.path.join(src, file)
                        outputImage = dest+'/rotated_'+file
                        #inputImage=pipes.quote(inputImage)
                        #outputImage=pipes.quote(outputImage)
                        final_bearing=self.degreepath.get()
                        image_bearing = self.dic[file]
                        rotation = int(final_bearing)-int(image_bearing)
                        if rotation<0:
                            rotation = rotation +360
    
                        command = (['convert', inputImage, "-background", "black", "-rotate", str(rotation), outputImage])
                        #command2 = (['convert', inputImage, "-background", "black", "-rotate", str(rotation), outputImage])
                        print('Image {0} rotated by {1} degrees'.format(file, rotation))
                        p = subprocess.Popen(command, shell=True)
                        processing[file]= [p]
            '''
            while processing:
                for title, subps in processing.items():
                    for idx, subp in enumerate(subps):
                        poll = subp.poll()
                        if poll == None: continue
                        else: 
                            del processing[title]
                            print('Finished processing '+ str(title))
            '''
                        
    def cropFiles(self,src, dest):
        numFiles = countFiles(src)
        if numFiles > 0:
            makedirs(dest)
            
        for file in os.listdir(src):
            if file.endswith(".JPG") | file.endswith(".jpg"):
                inputImage = os.path.join(src, file)
                outputImage = dest+'/final_'+file
                
                w, h = self.get_image_size(inputImage)
                print(w,h)
                
                #tempLocation = os.path.join(src, 'border')
                #makedirs(tempLocation)
                #tempImage = os.path.join(tempLocation, file)
            
                offset1= (w-3648)/2
                offset2= (h-3648)/2
                if offset1<0:
                    print('CAME HERE')
                    offset1= -offset1
                    wi= str(offset1)+ "x0"
                    command2 = (['convert', inputImage, "-bordercolor", "black", "-border", wi, inputImage])
                    pr = subprocess.Popen(command2, shell=True)
                    pr.communicate(input)

                    
                if offset2<0:
                    print('CAME HERE')
                    offset2= -offset2
                    wi= "0x"+str(offset2)
                    command2 = (['convert', inputImage, "-bordercolor", "black", "-border", wi, inputImage])
                    pr = subprocess.Popen(command2, shell=True)
                    pr.communicate(input)

                w, h = self.get_image_size(inputImage)
                offset1= (w-3648)/2
                offset2= (h-3648)/2
                crop_string = "3648x3648+"+ str(offset1) + "+" + str(offset2)
                print(crop_string)
                
                command = (['convert', inputImage, "-crop", crop_string, outputImage])
                p = subprocess.Popen(command, shell=True)
                p.communicate()
                



    def get_size(self,start_path):
        #start_path = self.inputlocation
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(start_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
        return total_size


    def countFiles(self, directory):
        files = []
        if os.path.isdir(directory):
            for path, dirs, filenames in os.walk(directory):
                files.extend(filenames)
        return len(files)

    def sizeof_fmt(self, num, suffix='B'):
        for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
            if abs(num) < 1024.0:
                return "%3.2f %s%s" % (num, unit, suffix)
            num /= 1000.0
        return "%.1f %s%s" % (num, 'Yi', suffix)
    
    
    def get_image_size(self,fname):
        '''Determine the image type of fhandle and return its size.'''
        with open(fname, 'rb') as fhandle:
            head = fhandle.read(24)
            if len(head) != 24:
                return
            if imghdr.what(fname) == 'jpeg':
                try:
                    fhandle.seek(0) # Read 0xff next
                    size = 2
                    ftype = 0
                    while not 0xc0 <= ftype <= 0xcf:
                        fhandle.seek(size, 1)
                        byte = fhandle.read(1)
                        while ord(byte) == 0xff:
                            byte = fhandle.read(1)
                        ftype = ord(byte)
                        size = struct.unpack('>H', fhandle.read(2))[0] - 2
                    # We are at a SOFn block
                    fhandle.seek(1, 1)  # Skip `precision' byte.
                    height, width = struct.unpack('>HH', fhandle.read(4))
                except Exception: #IGNORE:W0703
                    return
            else:
                return
            return width, height



root = Tkinter.Tk()
root.geometry("800x400+300+200")
root.title("Image Rotation")
#root.configure(bg='grey')


app = Application('', master=root)

#app.configure(background='grey')
app.mainloop()
#com= comparing(app)
root.destroy()
