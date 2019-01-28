# VORMaster3000
Redbird Data Parser for use with web based data interfaces of Redbird flight simulators.

This program scrapes the web data viewer interface for airspeed, heaidng, and altitude data to be graded in excel. This data is then  output in CSV format for import into excel. 

Collection time will need to be edited in the future when different patterns are used. 
  Open the script and in the large while loop, enter the total number of seconds of the track by replacing the time in "while counter<=###".

Either Python 2 or 3 may be used for this. If using python 3, note the code hasn't been tested with a real Redbird website. 

Module Selenium is required to run this. Google Chrome on the machine this is run on is *likely* also required. Ensure the chrome driver for Selenium is included here and should be contained in the same dir as the .py ran. 

To use, ensure python 2 or 3 is installed. Run from the command line or double click if the .py file is already associated in your OS.  Follow the prompts and ensure the dropdown containing the data values is dropped down in the Chrome window opened by the program (we didn't automate that, sorry.) 


Written by Alessandro Galli and Mark Hsiung (https://github.com/heeshung)
