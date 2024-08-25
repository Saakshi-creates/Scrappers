import time
import helper as help
import pandas as pd
from urllib.error import HTTPError

city_data = help.get_cities()[0]
# print(city_data, type(city_data))

feed_listing = help.get_feed_listing(city_data)
# print(feed_listing)

# cat= {'category': 'Dairy & Breakfast', 'l0_cat': '14', 'l1_cat': '922'}
# print(help.get_category_listing(cat,city_data))
#
# sub_cat={'sub_category': 'Bread & Pav', 'url': '/v1/layout/listing_widgets?l0_cat=14&l1_cat=953'}
# dict=help.get_dict()
# help.get_all_items_of_subcategory(sub_cat,city_data,dict)
# df=pd.DataFrame(dict)
# print(df)

dict=help.get_dict()
city_data=help.get_cities()
for city in city_data:
    # print(city)
    # category = [
    #     {'category': 'Vegetables & Fruits', 'collection_uuid': 'OTg3NjU0MzIxMjM0NTMzNzE=', 'cat': '1489'}]
    category= [
        {'category': 'Bath & Body', 'collection_uuid': 'OTg3NjU0MzIxMjM0NTMzNDY=', 'cat': '696'},
        {'category': 'Hair', 'collection_uuid': 'OTg3NjU0MzIxMjM0NTMzNDU=', 'cat': '2447'},
        {'category': 'Skin & Face', 'collection_uuid': 'OTg3NjU0MzIxMjM0NTMzNDI=', 'cat': '752'},
        {'category': 'Beauty & Cosmetics', 'collection_uuid': 'OTg3NjU0MzIxMjM0NTMzNDE=', 'cat': '2411'},
        # {'category': 'Feminine Hygiene', 'collection_uuid': 'OTg3NjU0MzIxMjM0NTMzNDA=', 'cat': '2450'},
    # {'category': 'Baby Care', 'collection_uuid': 'OTg3NjU0MzIxMjM0NTMzMzk=', 'cat': '3218'},
    # {'category': 'Health & Pharma', 'collection_uuid': 'OTg3NjU0MzIxMjM0NTMzMzI=', 'cat': '298'},
    {'category': 'Home & Lifestyle', 'collection_uuid': 'OTg3NjU0MzIxMjM0NTMzMjk=', 'cat': '2429'},
    {'category': 'Cleaners & Repellents', 'collection_uuid': 'OTg3NjU0MzIxMjM0NTMzMjc=', 'cat': None},
    {'category': 'Atta, Rice & Dal', 'collection_uuid': 'OTg3NjU0MzIxMjM0NTMzNjk=', 'cat': '1165'},
    {'category': 'Oil, Ghee & Masala', 'collection_uuid': 'OTg3NjU0MzIxMjM0NTMzNTY=', 'cat': '917'},
    {'category': 'Dairy, Bread & Eggs', 'collection_uuid': 'OTg3NjU0MzIxMjM0NTMzNTU=', 'cat': '922'},
    {'category': 'Bakery & Biscuits', 'collection_uuid': 'OTg3NjU0MzIxMjM0NTMzNTQ=', 'cat': '28'},
    {'category': 'Dry Fruits & Cereals', 'collection_uuid': 'OTg3NjU0MzIxMjM0NTMzNTM=', 'cat': '2381'},
    {'category': 'Chips & Namkeen', 'collection_uuid': 'OTg3NjU0MzIxMjM0NTMzNjg=', 'cat': '940'},
    # {'category': 'Drinks & Juices', 'collection_uuid': 'OTg3NjU0MzIxMjM0NTMzNTE=', 'cat': '1102'},
    {'category': 'Tea, Coffee & Health Drinks', 'collection_uuid': 'OTg3NjU0MzIxMjM0NTMzNTA=', 'cat': '957'},
    # {'category': 'Sauces & Spreads', 'collection_uuid': 'OTg3NjU0MzIxMjM0NTMzNDg=', 'cat': '277'},
    {'category': 'Ice Creams & More', 'collection_uuid': 'OTg3NjU0MzIxMjM0NTMxOTg=', 'cat': '1961'},
    {'category': 'Instant Food', 'collection_uuid': 'OTg3NjU0MzIxMjM0NTMzNDk=', 'cat': '962'}]


###############################################NEW CODE##############################################

    sub_category = []
    rerun_cat = []
    rerun_subcat = []

    for cat in category:
        try:
            print(cat)
            category_listing = help.get_category_listing(cat, city)
            sub_category.extend(category_listing)
        except Exception as e:
            print(f"Error fetching category {cat}: {e}")
            rerun_cat.append(cat)
        time.sleep(2)

    for subs in sub_category:
        try:
            print(subs)
            help.get_all_items_of_subcategory(subs, city, dict)
        except Exception as e:
            print(f"Error fetching subcategory {subs}: {e}")
            rerun_subcat.append(subs)
        time.sleep(10)

    # Retry logic for rerun_cat
    for cat in rerun_cat:
        try:
            print(f"Retrying {cat}")
            category_listing = help.get_category_listing(cat, city)
            sub_category.extend(category_listing)
        except Exception as e:
            print(f"Error fetching category {cat}: {e}")
        time.sleep(2)

    # Retry logic for rerun_subcat
    time.sleep(5)
    for subs in rerun_subcat:
        try:
            print(f"Retrying {subs}")
            help.get_all_items_of_subcategory(subs, city, dict)
        except Exception as e:
            print(f"Error fetching subcategory {subs}: {e}")
        time.sleep(10)

    # Assuming the data is stored in a list of dictionaries
    data = []  # Replace with your actual data collection logic

###############################################NEW CODE##############################################



df=pd.DataFrame(dict)
# df.to_csv(r"C:\\Users\\Lenovo\\Downloads\\scfm.csv")
print(df.to_string())

google_sheet_name = 'Scrappers_FMCG'
sheet_name = 'Blinkit'
#
# google_sheet_name = 'Scrappers'
# sheet_name = 'blink_it'
sh = help.connect_with_sheet(google_sheet_name)
print(sh)

wk1 = sh.worksheet('title', sheet_name)
wk1.clear()
wk1.set_dataframe(df, (1, 1))

print("success")







































































































































































































































































































































































































































































































































































































































