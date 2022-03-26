import requests
from bs4 import BeautifulSoup
import time
from random import randint
from pymongo import MongoClient
from pprint import pprint
import re
import json


########################
###### Question 1 ######
########################

header_my = {'User-Agent':
           'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'}

### Download the 4 pages that contains Top 40 donut shops
page_num = [0, 10, 20, 30]
for i in range(4):
    page_url = 'https://www.yelp.com/search?find_desc=donut+shop&find_loc=San+Francisco%2C+CA+94105&start=' + str(page_num[i])
    page_i = requests.get(page_url, headers = header_my)
    soup = BeautifulSoup(page_i.content, 'html.parser')

    filename = 'sf_donut_shop_search_page_' + str(page_num[i] // 10 + 1) + '.htm'
    f = open(filename, 'x')
    f = open(filename, 'w')
    f.write(str(soup))
    f.close()
    time.sleep(randint(6,10))



#####################################
###### Question 2 & Question 3 ######
#####################################

### Connect to Mongodb
client = MongoClient('localhost:27017')

### Create a new database called sf_donut_shops
database_name = "sf_donut_shops"
sf_donut_shops = client[database_name]
### Create a new collection called sf_donut_shops in the database created just now
collection_name = "sf_donut_shops"
collection = sf_donut_shops[collection_name]

print('\n\n')
print("##############################################################################")
print("############################## Store Information #############################")
print("##############################################################################")

### Loop through the 4 .htm files that contains the top 40 donut shops
for j in range(4):

    ### Open a file, parse the file with BeautifulSoup
    filename = 'sf_donut_shop_search_page_' + str(j+1) + '.htm'
    f = open(filename, "r", encoding = 'utf-8')
    soup = BeautifulSoup(f.read(), 'lxml')

    ### Initialize a variable to store the 'All Result' header node
    li_header_All_Results = 0

    ### Find the 'All Results' header (h2) node, to locate the start point of not sponsored items
    h2_list = soup.find_all('h2')
    for h2 in h2_list:
        if h2.text == 'All Results':
            li_header_All_Results = h2.parent.parent


    ### Each file contains 10 records of not sponsored items
    ### Inside of each file, loop through the 10 shops after the "All Results" header
    for i in range(10):
        result_i = li_header_All_Results.next_sibling


        ### Get the Rank and Name of Stores
        store_header_info = result_i.select('span[data-font-weight]')
        rank_and_name = store_header_info[0].text
        # Parse the ranking and name (since they are currently concatenated)
        if j == 0:
            if i < 9:
                rank = rank_and_name[:1]
                name = rank_and_name[3:]
            else:
                rank = rank_and_name[:2]
                name = rank_and_name[4:]
        else:
            rank = rank_and_name[:2]
            name = rank_and_name[4:]
        print('Store Ranking: ', rank)
        print('Store Name: ', name)


        ### Get the link of Stores
        store_link_tag = store_header_info[0].find('a', href = True)
        store_link = 'https://www.yelp.com/' + store_link_tag['href']
        print('Store Link: ', store_link)


        ### Get Star Ratings
        star_rating_tag = result_i.find('div', role = 'img')
        star_rating = star_rating_tag['aria-label']
        print('Star Rating: ', star_rating)


        ### Get Number of Reviews
        num_review_block = star_rating_tag.parent.parent.next_sibling
        num_review = num_review_block.span.text
        print('Review Number: ', num_review)


        ### Get Store Tags
        store_tag_block = num_review_block.parent.parent.parent.next_sibling.find('span')
        store_tag_buttons = store_tag_block.find_all('p')
        store_tag_list = []
        for store_tag_button in store_tag_buttons:
            store_tag_list.append(store_tag_button.text)
        print('Store Tags: ', store_tag_list)


        ### Get $ Signs
        try:
            dollar_sign_block = store_tag_block.next_sibling
            dollar_sign = dollar_sign_block.span.text
        except:
            dollar_sign = 'Null'
        print('Dollar Signs: ', dollar_sign)


        ### Get Delivery / Dine-in Informations
        accessibility_name = []
        accessibility_sign = []
        try:
            accessibility_grand_block = result_i.find('ul')
            accessibility_blocks = accessibility_grand_block.find('li').div
            for accessibility_block in accessibility_blocks:
                acc_icon = accessibility_block.find('path')['d']
                acc_name = accessibility_block.find('p').span.text
                accessibility_name.append(acc_name)
                accessibility_sign.append(acc_icon)
        except:
            accessibility_name.append('Null')
            accessibility_sign.append('Null')
        # Convert the icon (pixel string) into hunman words: Analiable / Not Avaliable
        accessibility_boolean = ['Avaliable' if x == 'M6.308 11.763a.748.748 0 01-.53-.22l-2.641-2.64a.75.75 0 011.06-1.061l2.11 2.11 5.496-5.495a.75.75 0 111.06 1.06l-6.025 6.026a.748.748 0 01-.53.22z' else 'Not Avaliable' for x in accessibility_sign]
        # Store the name-sign pairs into a dictionary
        accessibility_dict = {}
        for i in range(len(accessibility_name)):
            accessibility_dict[accessibility_name[i]] = accessibility_boolean[i]
        print('Accessibility: \n', accessibility_dict)


        ### Get Order-from-Yelp Information
        order_from_yelp = 'No'
        try:
            button_text = result_i.find_all("span", attrs={"data-font-weight":"semibold"})
            for m in button_text:
                if m.text == 'Start Order':
                    order_from_yelp = 'Yes'
                    break
        except:
            pass
        print('Avaliable Order From Yelp: ', order_from_yelp)
        print('--------------------------------------')

        ### To make result_i point to next shop in the begining of next loop
        li_header_All_Results = result_i


        ### Concat the information of each shop as one document
        ### Insert the document into the sf_donut_shop collection
        document = {'Ranking' : rank,
                    'Shop Name' : name,
                    'Shop Link': store_link,
                    'Star Rating': star_rating,
                    'Number of Reviews' : num_review,
                    'Store Tags': store_tag_list,
                    'Dollar Signs': dollar_sign,
                    'Accessibility Tags': accessibility_dict,
                    'Order Through Yelp': order_from_yelp
                   }
        collection.insert_one(document)




########################
###### Question 4 ######
########################

### Download the 40 pages for each shop
for i in range(40):
    shop_i = collection.find({'Ranking' : str(i + 1)})
    link = shop_i[0]['Shop Link']
    page = requests.get(link, headers = header_my)
    soup = BeautifulSoup(page.content, 'html.parser')

    file_name = "sf_donut_shop_" + str(i + 1) + ".htm"
    f = open(file_name, 'x')
    f = open(file_name, 'w')
    f.write(str(soup))
    f.close()

    time.sleep(randint(6,10))




#####################################
###### Question 5 & Question 6 ######
#####################################

### Initialize Global lists to store the information
shop_websites = []
phone_numbers = []
address = []
longitude = []
latitude = []

print('\n\n')
print('##############################################################################')
print("####################### New Inforamtion for Each Store #######################")
print("##############################################################################\n")

### Loop through 40 files
for i in range(40):
    file_name = "sf_donut_shop_" + str(i + 1) + ".htm"
    f = open(file_name, "r", encoding = 'utf-8')
    soup = BeautifulSoup(f.read(), 'lxml')


    ### Get the Website of the shop
    try:
        for elem in soup(text=re.compile(r'Business website')):
            shop_websites.append(elem.parent.next_sibling.a.text)
    except:
        shop_websites.append('Null')


    ### Get the Address of the shop
    address_block = " "
    try:
        for elem in soup(text=re.compile(r'Get Directions')):
            if elem.parent.parent.next_sibling.text > '':
                address.append(elem.parent.parent.next_sibling.text)
                address_block = elem.parent
    except:
        address.append('Null')


    ### Get the Phone Number of the shop
    shop_information_block = address_block.parent.parent.parent.parent.parent
    if len(soup(text=re.compile(r'Phone number'))) == 1:
        phone_numbers.append('Null')
    else:
        all_p_in_the_block = shop_information_block.find_all('p')
        for p in all_p_in_the_block:
            if p.text[0] == '(':
                phone_numbers.append(p.text)


    ### Get the geolocation of the shop
    api_link = "http://api.positionstack.com/v1/forward?access_key=2a9e9f4b291f2306d70ee0ff3d70d945&query=" + address[i]
    geoinfo = requests.get(api_link, headers = header_my)
    soup = BeautifulSoup(geoinfo.content, 'html.parser')
    content = json.loads(str(soup))
    latitude = content['data'][0]['latitude']
    longitude = content['data'][0]['longitude']


    ### Print the informations for each store
    print('------ Store ', i+1, '------')
    print('Phone Number: ', phone_numbers[i])
    print('Website: ', shop_websites[i])
    print('Address: ', address[i])
    print('Longitude: ', longitude)
    print('Latitude: ', latitude)


    ### Load Phone Number, Website, Address, Longitude, Latitude into the collection
    query = {"Ranking": str(i+1)}
    new_info_phone_num = {"$set": {"Phone Number": phone_numbers[i]}}
    new_info_website = {"$set": {"Website": shop_websites[i]}}
    new_info_address = {"$set": {"Address": address[i]}}
    new_info_long = {"$set": {"Longitude": longitude}}
    new_info_lati = {"$set": {"Latitude": latitude}}

    collection.update_one(query, new_info_phone_num)
    collection.update_one(query, new_info_website)
    collection.update_one(query, new_info_address)
    collection.update_one(query, new_info_long)
    collection.update_one(query, new_info_lati)


### Set index on the Ranking column
collection.create_index('Ranking')


### Print the final collection
print('\n\n')
print('##############################################################################')
print("#################### The Final 'sf_donut_shop' Collection ####################")
print('##############################################################################\n')

for document in collection.find():
    pprint(document)
    print()

