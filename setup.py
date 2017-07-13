from distutils.core import setup
import py2exe
import imageRotation

setup(console =['imageRotation.py'],
      options = {
          'py2exe':{
              'packages':['Tkinter', 'tkFileDialog']
              }
          }
       )