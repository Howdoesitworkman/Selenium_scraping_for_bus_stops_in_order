from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import sys
import os
def launch_and_scrape():
    website = 'https://www.wtlivewpg.com/Pages/Timetables/2023-09-03/Runs/index.html'
    driver = webdriver.Chrome()
    driver.get(website)
    
    os.makedirs("data", exist_ok=True)
    routes_txt = open("all_routes_index.txt", "r")
    
    pre_route_id = "init"   #use "init" as the first id, which is phony
    direction_txt = open("data/"+pre_route_id, "w")
    line = routes_txt.readline()
    destn_list = []
    while(line!=None):
        line = line.strip()
        route_id_list = line.split()    #split the string by whitespace
        route_id_index_li = route_id_list[0].split("-")     #route_id_index_li is something like '10-1'
        route_id = route_id_index_li[0]
        if(route_id!=pre_route_id):     #eg, pre_route_id == 15 but route_id == 16
            destn_list_str = '\n'.join(destn_list)
            direction_txt.write(destn_list_str)  #make a list of strings be one string, linked by '\n'
            direction_txt.close()
            destn_list = []
            if(int(route_id)<100):
                os.makedirs("data/"+route_id, exist_ok=True)
                path = "data/"+route_id+"/"
                direction_txt = open(path+route_id+" directions.txt", "w")
                temp_route_id = route_id
            elif(int(route_id)==100):
                os.makedirs("data/BLUE", exist_ok=True)
                path = "data/BLUE/"
                direction_txt = open(path+"BLUE directions.txt", "w")
                temp_route_id = 'BLUE'
            else:
                os.makedirs("data/"+str(int(route_id)+500), exist_ok=True)
                path = "data/"+str(int(route_id)+500)+"/"
                direction_txt = open(path+str(int(route_id)+500)+" directions.txt", "w")
                temp_route_id = str(int(route_id)+500)
            pre_route_id = route_id
            
        route_link = driver.find_element(By.LINK_TEXT, route_id_list[0])    #we only choose the first one, which is on weekday
        route_link.click()      #click the link and go to the next page
        
        time_table = driver.find_element(By.ID, 'times')
        destn_elements = time_table.find_elements(By.ID, 'departureLine')
        count = 1
        for each_destn_element in destn_elements:
            route_part = each_destn_element.find_element(By.ID, 'route')
            destn_part = each_destn_element.find_element(By.ID, 'fakeLinkDark')
            if (destn_part.text not in destn_list) & (route_part.text==temp_route_id):
                destn_list.append(destn_part.text)
                destn_part.click()    #go to the next page
                list_stops_file = open(path+destn_part.text+".txt", "w")     #sys.path[0] helps us write in the current folder
                trip_tables = driver.find_element(By.ID, 'tripTables')
                display_table = trip_tables.find_element(By.ID, 'TripT'+str(count))
                list_of_stops = display_table.find_elements(By.ID, 'darkLink')
                list_of_stops_str = []
                for each_stop in list_of_stops:
                    if (each_stop.text!=''):
                        list_of_stops_str.append(each_stop.text)
                list_str = '\n'.join(list_of_stops_str)
                list_stops_file.write(list_str)
            count = count + 1
        driver.get(website)
        line = routes_txt.readline()  
    
launch_and_scrape()

