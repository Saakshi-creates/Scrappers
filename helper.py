import cfscrape
import pygsheets
from urllib.parse import urlparse, parse_qs
import gspread
from google.oauth2 import service_account
from google.oauth2.service_account import Credentials
import pandas as pd
def get_cities():
    return [
        {
            'city':'Gurgaon',
            'lat':'28.445291',
            'lon':'77.057038'
        }
        # {
        #     "city":"Mumbai",
        #     'lat':"19.246722",
        #     "lon":"72.975971"
        # },
        # {
        #     "city":"Noida",
        #     "lat":"28.572985",
        #     "lon":"77.324904",
        #
        # },
        # {
        #     "city": "Delhi",
        #     "lat": "28.609554",
        #     "lon": "77.330298",
        #
        # }
    ]

def get_dict():
    return {
        'Name':[],
        'Price':[],
        'MRP':[],
        'Weight':[],
        'Category':[],
        'Sub Category':[],
        'Availability':[],
        'City': [],
        'Brand':[],
        'category_1':[]
    }
def get_feed_listing(city_data):
    scraper = cfscrape.create_scraper()
    url="https://api2.grofers.com/v1/layout/feed"
    headers={
        'app_client':'consumer_android',
        'lat':city_data.get("lat"),
        'lon':city_data.get("lon"),
        'app_version':'80150510',
    }
    scraper.headers.update(headers)
    response = scraper.post(url)
    data=response.json().get("response").get("snippets")
    # print(data)
    # return
    list=[]
    for i in data:
        if i.get("widget_type")=="grid_container_vr":
            try:
                items=i.get("data").get("items")
                for j in items:
                    url=j.get("data").get("click_action").get("blinkit_deeplink").get("url")
                    parsed_url = urlparse(url)
                    query_params = parse_qs(parsed_url.query)
                    collection_uuid = query_params.get('collection_uuid', [None])[0]
                    cat = query_params.get('cat', [None])[0]
                    category=j.get("data").get("title").get("text")
                    list.append({
                        'category':category,
                        'collection_uuid':collection_uuid,
                        'cat':cat
                    })
            except Exception:
                continue

    return list

def get_category_listing(item,city_data):

        # l0_cat=item.get('l0_cat')
        # l1_cat=item.get('l1_cat')
        uuid=item.get("collection_uuid")
        cat=item.get("cat")
        url=f"https://api2.grofers.com/v1/layout/listing?collection_uuid={uuid}&cat={cat}"
        # url=f"https://api2.grofers.com/v1/layout/listing?l0_cat={l0_cat}&l1_cat={l1_cat}"
        scraper = cfscrape.create_scraper()
        headers = {
            'app_client': 'consumer_android',
            'lat': city_data.get("lat"),
            'lon': city_data.get("lon"),
            'app_version': '80150510',
        }
        scraper.headers.update(headers)
        response = scraper.post(url)
        response=response.json()
        data=response.get("response").get("snippets")
        list=[]

        for i in data:
            sub_category=i.get("data").get("selected_title").get("text")
            url=i.get("data").get("click_action").get("change_page_uri").get("api_params").get("url")
            list.append({
                'sub_category':sub_category,
                'url':url
            })
        return list
def get_all_items_of_subcategory(item,city_data,dict):
    import json

    flag=False
    url="https://api2.grofers.com"+item.get("url")
    while True:
        scraper = cfscrape.create_scraper()
        headers = {
            'app_client': 'consumer_android',
            'lat': city_data.get("lat"),
            'lon': city_data.get("lon"),
            'app_version': '80150510',
        }
        scraper.headers.update(headers)
        response = scraper.post(url)
        try:
            response = response.json().get("response",{})
        except Exception as e:
            print(response.text)
            # print(e)
            return

        nextUrl=None
        if response.get("pagination"):
            nextUrl=response.get("pagination").get("next_url")
        if nextUrl:
            url="https://api2.grofers.com"+nextUrl
        else:
            flag=True
        snippets=response.get("snippets",[])
        for snippet in snippets:
            try:
                if snippet.get("data").get("variant_list"):
                    for variant in snippet.get("data").get("variant_list"):
                        name = variant.get("data").get("name").get("text")
                        mrp = variant.get("tracking").get("common_attributes").get("mrp")
                        weight = variant.get("data").get("variant").get("text")
                        offer_price = variant.get("tracking").get("common_attributes").get("price")
                        cat = variant.get("tracking").get("common_attributes").get("l0_category")
                        category_1=variant.get("tracking").get("common_attributes").get("ptype")
                        sub_cat = variant.get("tracking").get("common_attributes").get("l1_category")
                        stock = "In Stock" if variant.get("tracking").get("common_attributes").get("state") == "available" else "Out of Stock"
                        brand = snippet.get("data").get("brand_name",{}).get("text")
                        city = city_data.get("city")
                        print(name,weight,mrp,offer_price,cat,sub_cat,stock,brand,city,category_1)
                        dict['Name'].append(name)
                        dict['MRP'].append(mrp)
                        dict['Price'].append(offer_price)
                        dict['Weight'].append(weight)
                        dict['Category'].append(cat)
                        dict['Sub Category'].append(sub_cat)
                        dict['Availability'].append(stock)
                        dict['City'].append(city)
                        dict['Brand'].append(brand)
                        dict['category_1'].append(category_1)
                else:
                    name=snippet.get("data").get("name").get("text")
                    mrp=snippet.get("tracking").get("common_attributes").get("mrp")
                    weight=snippet.get("data").get("variant").get("text")
                    offer_price=snippet.get("tracking").get("common_attributes").get("price")
                    cat=snippet.get("tracking").get("common_attributes").get("l0_category")
                    sub_cat = snippet.get("tracking").get("common_attributes").get("l1_category")
                    category_1 = snippet.get("tracking").get("common_attributes").get("ptype")
                    stock="In Stock" if snippet.get("tracking").get("common_attributes").get("state")=="available" else "Out of Stock"
                    brand = snippet.get("data").get("brand_name",{}).get("text")
                    city=city_data.get("city")
                    print(name, weight, mrp, offer_price, cat, sub_cat, stock, brand, city,category_1)
                    dict['Name'].append(name)
                    dict['MRP'].append(mrp)
                    dict['Price'].append(offer_price)
                    dict['Weight'].append(weight)
                    dict['Category'].append(cat)
                    dict['Sub Category'].append(sub_cat)
                    dict['Availability'].append(stock)
                    dict['City'].append(city)
                    dict['Brand'].append(brand)
                    dict['category_1'].append(category_1)
            except Exception as e:
                # raise e
                continue
        if flag:
            break
def scrape_blinkit():
    cities_data=get_cities()
    dict=get_dict()
    for city_data in cities_data:
        count = 0
        feed_listing=get_feed_listing(city_data)
        for item in feed_listing:
            print(item)
            category_listing=get_category_listing(item,city_data)
            for subs in category_listing:
                print(subs)
                get_all_items_of_subcategory(subs,city_data,dict)
            count += 1
    return dict

def scrape_blinkit1():
    cities_data=get_cities()
    dict=get_dict()
    for city_data in cities_data:
        feed_listing=get_feed_listing(city_data)
        sub_category_list=[]
        for item in feed_listing:
            category_listing=get_category_listing(item,city_data)
            for subs in category_listing:
                subs.update({
                    'category':item.get('category')
                })
                sub_category_list.append(subs)
                # get_all_items_of_subcategory(subs,city_data,dict)
        print(len(sub_category_list))
    return dict

def connect_with_sheet(sheet_name):
  gc = pygsheets.authorize(service_file='google_sheet_credentials.json')
  sh = gc.open(sheet_name)
  return sh

def get_data_from_sheet(sheet_name, i):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = service_account.Credentials.from_service_account_file(
        "google_sheet_credentials.json",
        scopes=scope)
    client = gspread.authorize(creds)
    sheet = client.open(sheet_name)
    sheet_instance = sheet.get_worksheet(i)
    records_data = sheet_instance.get_all_records()
    table = pd.DataFrame(records_data)
    return table
