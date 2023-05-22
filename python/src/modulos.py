#Módulos da interface GUI
from tkinter import *
from tkinter import ttk
from tkinter.ttk import Treeview, Scrollbar, Entry, Style
from tkinter import simpledialog
import cv2
from PIL import Image, ImageTk
import json
import base64
import unidecode
from VisionSystem import *
import threading
import numpy as np

#Bibliotecas 
from detector import *