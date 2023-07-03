from kivy.metrics import dp, sp
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.button import MDRaisedButton

import usb
import random
from datetime import datetime
import pandas as pd
from functools import partial
import databaseScripts.allTransactions as at
import databaseScripts.transactions as ts
import databaseScripts.inventory as inv
import databaseScripts.shifts as shifts
from kivyScripts.retailScreen import NumPad
from mainFunc import * 

class SettingsScreen(MDScreen):
    file_manager = None
    manager_open = False
    dialog = None
    resetdialog = None
    resetButton = None
    devices = []
    
  
    def submitPrinter(self,*args):
        if self.ids.mainButton.text != 'Select Printer':
            printerSettings["Printer_VendorID"] = self.devices[int(self.ids.mainButton.text.split(" ")[0])][2]
            printerSettings["Printer_ProductID"] = self.devices[int(self.ids.mainButton.text.split(" ")[0])][3]
            printerSettings["Cash_Drawer"] = self.ids.cashDrawer.active
            printer.connectPrinter()
            updateStoreInformation()
            if printer.printer is  None:
                MDDialog(title = "!!!   ERROR   !!!\n\nPrinter did not connect successfully",md_bg_color = [1,0,0,0.5]).open()
            else:
                MDDialog(title = "Printer Settings Successfully Updated",md_bg_color = [0,1,0,0.5]).open()

       