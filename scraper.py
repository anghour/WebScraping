__author__= "Azziz ANGHOUR"
__email__= "anghour@gmail.com"
__version__= "1.0.0"

import time

from bs4 import BeautifulSoup
from selenium import webdriver

from coffshore_scraper.models.model import *
from coffshore_scraper.data_persistence.dao import *

#--------------------------------------------------------#
#------------------------ Fonctions ---------------------#
#--------------------------------------------------------#


def get_browser():
    profile = webdriver.FirefoxProfile()
    profile.set_preference("general.useragent.override",
                           "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0")
    return webdriver.Firefox(profile)

def get_html_content(browser, url):
    print("PAGE LOADING => ", url)
    try:
        browser.get(url)
    except :
        print("ERREUR DE CHARGEMENT DE L'URL : ", url)
        return None

    time.sleep(5)
    # Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0
    htmlContent = browser.execute_script("return document.body.innerHTML")
    return BeautifulSoup(htmlContent, 'lxml')

def get_country_suppy_chain(browser, url):

    html_content = get_html_content(browser, url)

    if(html_content == None):
        return None

    try:
        wind_farm_map = {}

        if(html_content != None):
            #print(html_content)

            main_div = html_content.find(id="multiOpenAccordion")

            h3_titles = main_div.find_all('h3')
            tables = main_div.find_all('table', class_="table table-striped")

            for h3_index in range(len(h3_titles)):
                wind_farm_title = h3_titles[h3_index].find('a').find('span').text.strip()
                wind_farm_table = tables[h3_index]
                print("WIND FARM : ", wind_farm_title)
                wind_fram_rows = wind_farm_table.find_all('tr')
                #print("TAB : ", len(wind_fram_rows))

                wind_farm = WindFarm(wind_farm_title)
                wind_farm_element_list = []
                if(wind_fram_rows != None and len(wind_fram_rows) > 2):

                    for row_index in range(1, len(wind_fram_rows)):
                        wind_farm_columns = wind_fram_rows[row_index].find_all('td', limit=2)

                        if(len(wind_farm_columns) > 1):
                            role_column = wind_farm_columns[0].span.text.strip()
                            organisation_infos = wind_farm_columns[1].find('div', class_="gvshOrg")
                            organisation_name = organisation_infos.a
                            if(organisation_name != None):
                                organisation_name = organisation_name.text.strip()
                            else :
                                organisation_name = organisation_infos.text.strip()
                            organisation_client = organisation_infos.span
                            if(organisation_client != None):
                                organisation_client = organisation_client.a.text.strip()
                            organisation_desc = wind_farm_columns[1].find('div', class_="gvshDesc")
                            if(organisation_desc.a != None):
                                organisation_desc = organisation_desc.a.text.strip()
                            elif(organisation_desc.span != None):
                                organisation_desc = organisation_desc.span.text.strip()
                        organisation = Organisation(organisation_name, organisation_client,
                                                    organisation_desc)
                        wind_farm_element = WindFarmElement(role_column, organisation)
                        wind_farm_element_list.append(wind_farm_element)

                wind_farm.wind_farm_element_list = wind_farm_element_list
                wind_farm_map[wind_farm_title] = wind_farm


                            #print("Role : ", role_column, "name : ", organisation_name,
                                  #" Desc : ", organisation_desc, ", Client : ", organisation_client)

                #print("TITLE => ", wind_farm_title)

                print("\n===============================\n")
        return wind_farm_map

    except :
        print("ERREUR D'EXTRACTION")
        return None


#--------------------------------------------------------#
#--------------------- PROGRAMME PRINCIPAL---------------#
#--------------------------------------------------------#


url_base = "http://www.4coffshore.com/windfarms/"
windfarms_url = "windfarms.aspx?windfarmId="
start_url = url_base + windfarms_url + "FR34"
browser = get_browser()
soup = get_html_content(browser, start_url)


countries_supply_chain = []
for elem in soup.find_all('option'):
    country_wind_farm_map = {}
    id = elem['value']
    main_link = url_base + windfarms_url + id
    supply_chain_link = None
    if(id == "FR34"):
        supply_chain_link = soup.find(id='ctl00_Body_Page_SubMenu_hypSupplychain')['href']
    else :
        print("Country ID => ", id, ' ...')
        time.sleep(4)


        country_main_page = get_html_content(browser, main_link)
        if(country_main_page != None):

            supply_chain_link = country_main_page.find(id='ctl00_Body_Page_SubMenu_hypSupplychain')

            if(supply_chain_link != None):
                supply_chain_link = supply_chain_link['href']
                country_wind_farm_map = get_country_suppy_chain(browser, url_base + supply_chain_link)


    if(supply_chain_link != None):
        supply_chain_link = url_base + supply_chain_link
    country = Country(id, elem.text, main_link, supply_chain_link)
    country_supply_chain = CountrySuppyChain(country, country_wind_farm_map)
    #print(country_supply_chain)
    countries_supply_chain.append(country_supply_chain)


# Save the result in a json file
save_in_json_format("data/countries_supply_chain.json", countries_supply_chain)

