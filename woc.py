
# Files that will be saved after execution of the program
techarray_path = 'organisation tech names.txt'
options_file_path = 'all tech options.txt'
links_path = 'organisation page links.txt'
csv_path = 'orgs for you.csv'
# ------------------------------------------------------

#Selenium imports here
from logging import currentframe, fatal
from time import sleep, time
import urllib
from explicit.waiter import find_element
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import WebDriverWait
import itertools
#-------------------------------------------------------------


#Other imports here
import os
import sys # to exit code
import time
import datetime
import smtplib
import array
import csv

# Email imports
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from base64 import encodebytes

# Some Inisialization----------------------------------------------------------------------------

tech_array = []
tech_options = []

# ------------------------------------------------------------------------------

driver = webdriver.Chrome('E:/Chrome driver/chromedriver_win32/chromedriver.exe')
driver.get('https://summerofcode.withgoogle.com/archive/2020/organizations/')

print('\nExtracting Organisation\'s Technologies...\n')

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
driver.execute_script("window.scrollTo(0,0);")

list_org_elem = WebDriverWait(driver,10).until(EC.visibility_of_all_elements_located((By.XPATH, '/html/body/main/section/div/ul/li')))
list_links = WebDriverWait(driver,10).until(EC.visibility_of_all_elements_located((By.XPATH, '/html/body/main/section/div/ul/li/a')))

list_link_pure = []
for i in range(len(list_links)):
    list_link_pure = list_link_pure + [list_links[i].get_attribute('href')]


one_elem_address = '/html/body/main/section/div/ul/li/a/md-card/div/h4'
title_list = WebDriverWait(driver,10).until(EC.visibility_of_all_elements_located((By.XPATH, one_elem_address )))

org_names = []
for i in range(len(title_list)):
    org_names = org_names + [title_list[i].text]


for k in range(len(list_links)):
    
    print(str(k+1) + ') ' + org_names[k] + ' :')
    driver.get(list_link_pure[k])
    tech_elem_address = '//md-card/div/div[3]/ul/li'
    tech_list = WebDriverWait(driver,10).until(EC.visibility_of_all_elements_located((By.XPATH, tech_elem_address )))
    tech_array.append([])
    for j in range(len(tech_list)):
        if tech_list[j].text not in tech_options:
            tech_options = tech_options + [tech_list[j].text]
        tech_array[k] = tech_array[k] + [tech_list[j].text]
    print(tech_array[k])

driver.quit()
print('\nScraping Complete.')    

file = open(techarray_path, 'w+')
for i in range(len(tech_array)):
    file.write(org_names[i] + '\n')
    for j in range(len(tech_array[i])):
        file.write(str(tech_array[i][j]) + ' ')
    file.write('\n')    
file.close()


file = open(options_file_path, 'w+')
for i in range(len(tech_options)):
    file.write(tech_options[i] + '\n')    
file.close()


file = open(links_path,'w+')
for i in range(len(list_link_pure)):
    file.write(list_link_pure[i] + '\n')    
file.close()




while(True):

    print('\nAll Technology Options :')
    print(tech_options)
    print('\n')

    sender_email = input('Sender\'s Email id: ')
    passwrd = input('Sender account password: ')
    receiver_email = input('Receiver\'s Email id: ')
    
    print('\n')

    your_choices = []
    while(True):
        
        inpt = input('Enter what you know from the above tech stacks (or \'exit\'): ')
        if(inpt == 'exit'):
            break
        if inpt in tech_options:
            your_choices = your_choices + [inpt]
        else:
            print('TECH NOT FOUND : Please enter from the given options only')

    print('\nOrganisations with your chosen technologies:\n')
    found_index = []
    csv_list = []
    for i in range(len(your_choices)):
        for j in range(len(tech_array)):
            if your_choices[i] in tech_array[j]:
                print(org_names[j])
                print(list_link_pure[j])
                print(tech_array[j])
                csv_list.append([])
                csv_list[len(found_index)] = csv_list[len(found_index)] + [org_names[j],list_link_pure[j],tech_array[j]]
                found_index = found_index + [j]
        
    
    csv_name = 'orgs for you.csv'
    with open(csv_path, 'w+' , newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(csv_list)



    


    mesag = MIMEMultipart()
    mesag['Subject'] = 'Organisations matching your tech'
    mesag['From'] = sender_email
    mesag['To'] = receiver_email

    # ----body----

    strng = ''
    for index in range(len(your_choices)):  
        strng = strng + '<p>&bull;&nbsp' + your_choices[index] + '</p>'

    body = '''
        <p><span style="color: #0000ff;">''' + str(len(found_index)) + ''' Organisations found for your preferred technologies</span></p>
        <p>Technologies you chose:</p>
        '''+ strng +'''
    '''
    
    mesag.attach(MIMEText(body, 'html'))
    
    # ------------

    # Attach file
    fp = open(csv_path, 'rb')
    part = MIMEBase('application', "octet-stream")
    part.set_payload(encodebytes(fp.read()).decode())
    fp.close()
    part.add_header('Content-Transfer-Encoding', 'base64')
    part.add_header('Content-Disposition', 'attachment; filename="%s"' %csv_name)
    mesag.attach(part)

    # send mail

    seson = smtplib.SMTP('smtp.gmail.com', 587)
    seson.starttls()
    seson.login(sender_email,passwrd)
    final_msg = mesag.as_string()
    seson.sendmail(sender_email,receiver_email,final_msg)
    seson.quit()
    print('\nemail sent to %s\n' %receiver_email)

    while(True):
        ask = input('Want to check organisation for another set of technologies? [ yes / no ]: ')
        if ask == 'no':
            print('Program Closed')
            break
        if ask == 'yes':
            break
        else:
            print('Please enter "yes" or "no"')
    if ask == 'no':
        break
        