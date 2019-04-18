from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import csv
from datetime import datetime

import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
from math import trunc
import threading
import googlesearch

class GoogleKeywordSearchScraper:
    def __init__(self):
        self.sites = []
        self.searchitems = []
        self.result = []
        self.corethreadstate = False
        self.inputfiledir = ""
        self.initGUI()
    
    def initGUI(self):
        self.window = tk.Tk()
        self.window.title("Google Keyword Search Scraper")
        self.window.geometry("500x600")

        # self.file_browser = Browse(self.window, initialdir=r"C:\Users", filetypes=(('Portable Network Graphics','*.png'),("All files", "*.*")))
        # self.file_browser.place(x=10, y=25)
        self.filename = tk.StringVar()
        self.inputfile = tk.Entry(self.window, textvariable=self.filename, state=tk.DISABLED)
        self.filename.set("Select CSV File")
        self.inputfile.configure(font=("Courier", 10))
        self.inputfile.place(relx=0.03, rely=0.02, relheight=0.05, relwidth=0.6)

        # self.inputfile.place(x=10, y=25)

        self.browserButton = tk.Button(self.window, command=self.openfile)
        self.browserButton.configure(height=1, width=3)
        self.browserButton.configure(font=("Courier", 10))
        self.browserButton.configure(text='...')
        self.browserButton.place(relx=0.63, rely=0.02, relheight=0.05, relwidth=0.1)

        self.browserButton = tk.Button(self.window, command=self.start)
        self.browserButton.configure(height=1, width=3)
        self.browserButton.configure(font=("Courier", 10))
        self.browserButton.configure(text='Start')
        self.browserButton.place(relx=0.75, rely=0.02, relheight=0.05, relwidth=0.23)
        
        self.progress = ttk.Progressbar(self.window)
        self.progress.place(relx=0.03, rely=0.08, relheight=0.05, relwidth=0.95)

        self.stateText = tk.Text(self.window)
        self.stateText.configure(height=1, width=3)
        self.stateText.configure(font=("Courier", 10))
        self.stateText.place(relx=0.03, rely = 0.15, relheight=0.8, relwidth=0.95)
        
        self.stateNumInfo = tk.StringVar()
        self.stateNum = tk.Label(self.window, textvariable=self.stateNumInfo)
        
        self.stateNum.configure(height=1, width=3)
        self.stateNum.configure(font=("Courier", 10))
        self.stateNum.place(relx=0.0, rely = 0.95, relheight=0.05, relwidth=1.0)    
        
        self.window.mainloop()
        self.setStatus("Welcome!")

    def openfile(self):
        filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("csv files","*.csv"),("all files","*.*")))
        self.filename.set(filename)
        self.inputfiledir = filename
        print (filename)

    def start(self):
        if self.corethreadstate is True:
            messagebox.showinfo("Running!", "Now Running!, You can't click start button")
        else:
            self.corethread = threading.Thread(target=self.go)
            self.corethread.start()
        print("click start button")

    def go(self):
        self.corethreadstate = True
        conformstr = "Do you want to save the result?"
        
        self.readCsvFile()
        self.googlesearch = googlesearch.GoogleKeywordSearch()

        try:
            i = 2
            step = 100/(len(self.sites)*len(self.searchitems))
            self.stateNumInfo.set("0/"+str(len(self.sites)))
            for site in self.sites:
                self.stateText.insert(tk.INSERT, str(site)[:50]+" is scraping ...\n")
                for keyword in self.searchitems:
                    occurance = self.googlesearch.getSearchOccurance(site, keyword)
                    self.result[i].append(occurance)
                    self.progress.step(step)
                    self.progress.update()
                    status = "--->" + keyword + "\t:\t" + str(occurance) 
                    self.setStatus(status)
                i += 1
                self.stateNumInfo.set(str(i-2)+"/"+str(len(self.sites)))
        except Exception as e:
            print(e)

        self.googlesearch.close()
        conform = messagebox.askokcancel("Complete!", conformstr)
        if conform == 1:
            self.writeCsvFile()   
             
        self.corethreadstate = False
    
    def readCsvFile(self):
        status = "Reading CSV File..."
        self.stateText.insert(tk.INSERT, status+"\n")
        if self.inputfiledir:
            with open(self.inputfiledir, newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=',', quotechar='|')
                i = 0
                for row in reader:
                    if i == 0:
                        self.result.append(row)
                    elif i == 1:
                        self.result.append(row)
                        self.searchitems = row[1:]
                    else:
                        self.result.append([row[0]])
                        self.sites.append(row[0])
                    i = i + 1
            self.setStatus("File reading done!\n")
        else:
            self.setStatus("No Directory! Please select csv file\n")

    def writeCsvFile(self):
        self.setStatus("Saving CSV Files...")
        now = datetime.now()
        timestamp = datetime.timestamp(now)
        outfile_path = "result_"+str(timestamp)+".csv"
        with open(outfile_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter = ',', quotechar = '|', quoting=csv.QUOTE_MINIMAL)
            for row in self.result:
                writer.writerow(row)
        self.setStatus("Saved CSV File: "+outfile_path)
    
    def setStatus(self, status):
        self.stateText.insert(tk.INSERT, str(status)[:50]+"\n")
        print(status)

def main():
    try:
        s = GoogleKeywordSearchScraper()
        
    except Exception as e:
        print(e)
    else:
        print("Success!")

if __name__ == "__main__":
    main()