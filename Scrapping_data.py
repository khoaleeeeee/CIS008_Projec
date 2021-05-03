import requests
from bs4 import BeautifulSoup
import re
import csv

response = requests.get('https://www.the-numbers.com/movie/budgets/all/1')

webpage = response.text
soup = BeautifulSoup(webpage, 'html.parser')

movie_tag = soup.find('table')
movie_text = movie_tag.text
lst = movie_text.split('\n')
lst.pop(0)
lst.pop(0)
for i in lst:
    if i == '':
        lst.remove(i)
lst.pop(-1)


n = 1
for i in lst:
    if get_integers_only(i) == str(n):
        lst.remove(i)
        n += 1
        

def get_integers_only(string):
    tmp = ''
    for i in string:
        if i not in '\xa0$' and i != ',':
            tmp += i
    return tmp
    
    
row_list = [['production_budget_usd', 'domestic_gross_usd', 'worldwide_gross_usd']]

begin = 0
while begin < 400:
    tmp = []
    for j in range(begin, begin + 5):
        if j != begin and j != begin + 1:    
            tmp.append(get_integers_only(lst[j]))
    row_list.append(tmp)
    begin += 5
    
with open('cost_revenue.csv', 'w', newline='') as file:
    writer = csv.writer(file, delimiter=',')
    writer.writerows(row_list)
    
    
    
site_link = 'https://www.the-numbers.com/movie/budgets/all/'


# function to retrive only the integer values for the amounts of money
def get_integers_only(string):   
    tmp = ''
    for i in string:
        if i not in '\xa0$' and i != ',':
            tmp += i
    return tmp

# preprocessing and scrapping data from site
def scrapping_data(link, page):
    response = requests.get(link) # gets full HTML
    webpage = response.text # converts HTML to string
    soup = BeautifulSoup(webpage, 'html.parser')
    
    movie_tag = soup.find('table') # gets the table tag
    movie_text = movie_tag.text
    lst = movie_text.split('\n') 
    lst.pop(0) # drops unnescessarry items
    lst.pop(0)
    for i in lst:   # drops all blank elements
        if i == '':
            lst.remove(i)
    lst.pop(-1) # drops unnescessarry items
    
    n = page   # removes unnescessarry numbers
    for i in lst:
        if get_integers_only(i) == str(n):
            lst.remove(i)
            n += 1
        
    row_list = [] 
    begin = 0 
    while begin < 400:  # gets the budgets, domestic gross, and worldwide gross only
        tmp = []
        for j in range(begin, begin + 5):
            if j != begin and j != begin + 1:    # skips dates and titles
                tmp.append(get_integers_only(lst[j]))
        row_list.append(tmp)
        begin += 5
        
    return row_list
    

    
page = 101  # starts from the 2nd page 

while page <= 6001:
    full_link = site_link + str(page)
    data_list = scrapping_data(full_link, page)
    
    # append to csv file
    with open('cost_revenue.csv', 'a', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerows(data_list)
    print(page)
    page += 100