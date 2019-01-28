
# $$\    $$\  $$$$$$\  $$$$$$$\        $$\      $$\  $$$$$$\   $$$$$$\ $$$$$$$$\ $$$$$$$$\ $$$$$$$\         $$$$$$\   $$$$$$\   $$$$$$\   $$$$$$\  
# $$ |   $$ |$$  __$$\ $$  __$$\       $$$\    $$$ |$$  __$$\ $$  __$$\\__$$  __|$$  _____|$$  __$$\       $$ ___$$\ $$$ __$$\ $$$ __$$\ $$$ __$$\ 
# $$ |   $$ |$$ /  $$ |$$ |  $$ |      $$$$\  $$$$ |$$ /  $$ |$$ /  \__|  $$ |   $$ |      $$ |  $$ |      \_/   $$ |$$$$\ $$ |$$$$\ $$ |$$$$\ $$ |
# \$$\  $$  |$$ |  $$ |$$$$$$$  |      $$\$$\$$ $$ |$$$$$$$$ |\$$$$$$\    $$ |   $$$$$\    $$$$$$$  |        $$$$$ / $$\$$\$$ |$$\$$\$$ |$$\$$\$$ |
#  \$$\$$  / $$ |  $$ |$$  __$$<       $$ \$$$  $$ |$$  __$$ | \____$$\   $$ |   $$  __|   $$  __$$<         \___$$\ $$ \$$$$ |$$ \$$$$ |$$ \$$$$ |
#   \$$$  /  $$ |  $$ |$$ |  $$ |      $$ |\$  /$$ |$$ |  $$ |$$\   $$ |  $$ |   $$ |      $$ |  $$ |      $$\   $$ |$$ |\$$$ |$$ |\$$$ |$$ |\$$$ |
#    \$  /    $$$$$$  |$$ |  $$ |      $$ | \_/ $$ |$$ |  $$ |\$$$$$$  |  $$ |   $$$$$$$$\ $$ |  $$ |      \$$$$$$  |\$$$$$$  /\$$$$$$  /\$$$$$$  /
#     \_/     \______/ \__|  \__|      \__|     \__|\__|  \__| \______/   \__|   \________|\__|  \__|       \______/  \______/  \______/  \______/                                                                                                                                          
                                                                                                                                                                                                                                                                                             
import time
import csv
import os
import datetime
import math

#Using selenium to run a chrome instance in python that can read the Javascript generated HTML 
from selenium import webdriver

#Redbird URL where the data is sounced from
link = 'http://sim.redbirdflight.com/apps/InstructorStation/?/'

#Parameters that we want to pull 
headingString='Heading</span><span class="dashboard-stat">'
altitudeString ='Altitude</span><span class="dashboard-stat">'
IASString = 'IAS</span><span class="dashboard-stat">'

driver = webdriver.Chrome()
driver.get(link)

#Inputs from the user to write into the file and file name 
contestantName = raw_input("What is the contestant name? ")
contestantID = raw_input("What is the contestant ID? ")
School = raw_input("What is the contestant's school? ")

#Check to ensure we're not overwriting a already created contestant file 
iteration = 1
while(True):
	exists = os.path.isfile('%s_%s_Ground_Trainer_%d.csv' % (contestantID,contestantName,iteration) )
	if exists:
	    iteration += 1
	else:
	    break

file = open('%s_%s_Ground_Trainer_%d.csv' % (contestantID,contestantName,iteration) , mode='wb')

#CSV creation and headers
employee_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
employee_writer.writerow([contestantName, contestantID, School, 'Ground Trainer File' 'Region 7, 2018'])
employee_writer.writerow(['Time', 'HDG', 'ALT', 'IAS'])

#When ready, begin. Little drop down thing on the top of website with the live stats needs to be open 
raw_input("When ready, press enter to begin.  CHECK STATS ARE OPEN ON WEBPAGE!!!!!!")

#Using counter to detect the next time slice to take a datapoint. This eliminates a compounding error that would occur if we took 1 second plus whatever time the last datapoint was. 
counter = 0

starttime = time.time()

#Limiting time of data collection to 10:15 since thats the Fall 2018 NIFA Region 7 pattern 
while counter<=615:
	#Retrieve the most recent page HTML
	p_element = driver.page_source

	#If the next datapoint that should be collected has occured, collect it and increment the counter for the next time slice. 
	if time.time()-starttime >= counter:
		counterMinutes = counter/60
		counterSeconds = counter - counterMinutes*60
		counterTime = "%d:%02d" % (counterMinutes,counterSeconds)

		index = p_element.find(headingString)
		endIndex = p_element.find("<",index+len(headingString))
		heading = p_element[index+len(headingString):endIndex]

		index = p_element.find(altitudeString)
		endIndex = p_element.find("<",index+len(altitudeString))
		altitude = p_element[index+len(altitudeString):endIndex]

		index = p_element.find(IASString)
		endIndex = p_element.find("<",index+len(IASString))
		airspeed = p_element[index+len(IASString):endIndex]

		#Write it to the CSV and to the console 
		employee_writer.writerow([counterTime, heading, altitude, airspeed])
		print "Time: "+counterTime, "; Heading", heading, "; Altitude", altitude, "; Airspeed (IAS)", airspeed	

		counter += 1 

#Sanity check for the total time elapsed in the sim. 		
print time.time()-starttime
print "Flight completed."