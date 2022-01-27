import pandas as pd
from selenium import webdriver
import time
import warnings
warnings.filterwarnings("ignore")


#Importing data in csv format
df = pd.read_csv("Python Quiz Input - Sheet1.csv", delimiter=',')
#this try is i case your input contains a validation column
try:
    df.pop('Validation')
except:
    pass

# for row in range(df.shape[0]):
#     print(df.iloc[row,:].values)
print(df.iloc[0,:].values)
#Driver,url and parameter declaration
#This code use Chome driver
urlProject = 'https://tools.usps.com/zip-code-lookup.htm?byaddress'
driverPath = "chromedriver.exe"
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument("--test-type")
driver = webdriver.Chrome(driverPath)
driver.get(url=urlProject)
#Creation of the verification list to add the column to the output 
#using a loop to validate all the inputs
#first all the objects are locate by id and xpath
#then the inputs are being proccessed
#Once the imputs have been entered the find buttun is clicked
# there is a validation to know if the address is valid by calculating the length of the entered-address class
#Depending of the length a value is added to the verification list
verificationList = []
for row in range(df.shape[0]):
    companyArea = driver.find_element_by_id('tCompany')
    streetAddressArea = driver.find_element_by_id('tAddress')
    cityArea = driver.find_element_by_id('tCity')
    zipCodeArea = driver.find_element_by_id('tZip-byaddress')
    findButton = driver.find_element_by_id('zip-by-address')
    fila = row
    state=df.iloc[fila,:].values[3]
    driver.find_element_by_xpath(f"//option[@value='{state}']").click()
    companyArea.send_keys(df.iloc[fila,:].values[0])
    streetAddressArea.send_keys(df.iloc[fila,:].values[1])
    cityArea.send_keys(df.iloc[fila,:].values[2])
    zipCodeArea.send_keys(df.iloc[fila,:].values[4])
    time.sleep(2)
    findButton.click()
    time.sleep(2)
    try:
        if len(driver.find_element_by_class_name("entered-address").text) == 0:
            exist = False
            verificationList.append('Nonvalid')
        else:
            exist = True
            verificationList.append('Valid')
    except:
        print('Class not found')
    time.sleep(2)
    driver.refresh()

#Browser is closed after the loop
driver.close()
#Validarion list addded to the data frame
df['Validation']= verificationList
#dataframe to csv
df.to_csv('Python Quiz Input - Sheet1.csv')
#dataframe visualization
print(df)
    

