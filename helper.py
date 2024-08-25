import time

import requests
import pygsheets
import cfscrape
def get_city_dict():
    city={
        'Gurgoan':"MjguNDQ5ODQ5NHw3Ny4wNTY2ODg3",
        # 'Noida':"MjguNTc3Mzc5OXw3Ny4zMTQ0OTM1OTk5OTk5OQ==",
        'Mumbai':"MTkuMjE4MzMwN3w3Mi45NzgwODk3",
        # 'Delhi':"MjguNTU1NTc2OTE4NTl8NzcuMjMzNTkwMjI1Mzcy"
    }
    return city
def get_city_lat_long(city):
    city_dict = {
        'Gurgoan': "MjguNDQ5ODQ5NHw3Ny4wNTY2ODg3",
        # 'Noida': "MjguNTc3Mzc5OXw3Ny4zMTQ0OTM1OTk5OTk5OQ==",
        'Mumbai': "MTkuMjE4MzMwN3w3Mi45NzgwODk3",
        # 'Delhi':"MjguNTU1NTc2OTE4NTl8NzcuMjMzNTkwMjI1Mzcy"
    }
    return city_dict.get(city)
def get_slugs(city):
    return ['bakery-cakes-dairy', 'snacks-branded-foods','eggs-meat-fish', 'gourmet-world-food','foodgrains-oil-masala', 'beverages','kitchen-garden-pets']
    return ["eggs","milk","paneer-tofu-cream","butter-margarine","buttermilk-lassi","cheese","curd","atta-flours-sooji","atta-whole-wheat","rice-other-flours","sooji-maida-besan","rice-rice-products","basmati-rice","boiled-steam-rice","poha-sabudana-murmura","raw-rice","dals-pulses","cereals-millets","toor-channa-moong-dal","urad-other-dals","edible-oils-ghee","masalas-spices","blended-cooking-oils","cold-pressed-oil","cooking-coconut-oil","cotton-seed-oil","ghee-vanaspati","groundnut-oils","olive-canola-oils","other-edible-oils","soya-mustard-oils","sunflower-rice-bran-oil","dry-fruits","almonds","cashews","mukhwas","other-dry-fruits","raisins","salt-sugar-jaggery","salts","sugar-jaggery","sugarfree-sweeteners","breads-buns","dairy","gourmet-breads","non-dairy","fresh-vegetables","fresh-fruits","organic-fruits-vegetables","cuts-sprouts","exotic-fruits-veggies","flower-bouquets-bunches"]
        # ,"cuts-sprouts","exotic-fruits-veggies","flower-bouquets-bunches","fresh-fruits","herbs-seasonings","organic-fruits-vegetables","atta-flours-sooji","atta-whole-wheat","rice-other-flours","sooji-maida-besan","rice-rice-products","basmati-rice","boiled-steam-rice","poha-sabudana-murmura","raw-rice","dals-pulses","cereals-millets","toor-channa-moong-dal","urad-other-dals","edible-oils-ghee","masalas-spices","blended-cooking-oils","cold-pressed-oil","cooking-coconut-oil","cotton-seed-oil","ghee-vanaspati","groundnut-oils","olive-canola-oils","other-edible-oils","soya-mustard-oils","sunflower-rice-bran-oil","dry-fruits","almonds","cashews","mukhwas","other-dry-fruits","raisins","salt-sugar-jaggery","salts","sugar-jaggery","sugarfree-sweeteners","breads-buns","dairy","gourmet-breads","non-dairy","eggs","milk","paneer-tofu-cream","butter-margarine","buttermilk-lassi","cheese","curd"]
# 'foodgrains-oil-masala', 'bakery-cakes-dairy', 'beverages', 'snacks-branded-foods', 'beauty-hygiene', 'cleaning-household', 'kitchen-garden-pets', 'eggs-meat-fish', 'gourmet-world-food', 'baby-care', 'paan-corner'
# 'bakery-cakes-dairy', 'snacks-branded-foods','eggs-meat-fish', 'gourmet-world-food','foodgrains-oil-masala', 'beverages'
# fruits-vegetables
# 'bakery-cakes-dairy', 'snacks-branded-foods','eggs-meat-fish', 'gourmet-world-food','foodgrains-oil-masala', 'beverages'
def get_vegetables(slug,city):
    dict={
        'Name':[],
        'MRP':[],
        'Selling Price':[],
        'Weight':[],
        'Category':[],
        'Sub-Category':[],
        'Availability':[],
        'City':[],
        'approx_quant':[],
        'Brand':[]
    }
    pageNo=1
    count=0
    # u = "https://www.bigbasket.com/listing-svc/v2/products?bucket_id=16&ec_id=100&page={}&type=pc&slug=dairy"
    while True:
        url = f"https://www.bigbasket.com/listing-svc/v2/products?type=pc&slug={slug}&page={pageNo}"
        # url = u.format(pageNo)
        cookies = {
            '_bb_vid': "NTA3NDMzNTYwNA==",
            '_bb_mid': "MzEwNDE4MzY2OA==",
            "_bb_lat_long":get_city_lat_long(city)
        }
        headers = {
            'user-agent':'Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.136 Mobile Safari/537.36',
        }
        scraper = cfscrape.create_scraper()
        scraper.headers.update(headers)
        response = scraper.get(url,cookies=cookies)
        # response=requests.get(url=url,headers=headers,cookies=cookies)
        try:
            data=response.json()
            products = data.get("tabs")[0].get("product_info").get("products")
        except Exception as e:
            print("Responsse",response.text)
            print("Exception ",e)
            break
        for product in products:
            brand=product.get("brand").get("name")
            name=product.get("desc")
            quantity=product.get("pack_desc")
            mrp=product.get("pricing").get("discount").get("mrp")
            sp=product.get("pricing").get("discount").get("prim_price").get("sp")
            weight=product.get("w")
            category=product.get("category").get("tlc_name")
            sub_category=product.get("category").get("mlc_name")
            children=product.get("children")
            stock='InStock' if product.get("availability").get("avail_status")=='001' else 'Out Of Stock'
            # print(f"{name} {mrp} {sp} {weight} {category} {sub_category} {stock}")
            dict['Name'].append(name)
            dict['MRP'].append(mrp)
            dict['Selling Price'].append(sp)
            dict['Weight'].append(weight)
            dict['Category'].append(category)
            dict['Sub-Category'].append(sub_category)
            dict['Availability'].append(stock)
            dict['City'].append(city)
            dict['approx_quant'].append(quantity)
            dict['Brand'].append(brand)
            for child in children:
                cbrand=child.get("brand").get("name")
                cname = child.get("desc")
                cquantity=child.get("pack_desc")
                cmrp = child.get("pricing").get("discount").get("mrp")
                csp = child.get("pricing").get("discount").get("prim_price").get("sp")
                cweight = child.get("w")
                ccategory = child.get("category").get("tlc_name")
                csub_category = child.get("category").get("mlc_name")
                cstock = 'InStock' if child.get("availability").get("avail_status") == '001' else 'Out of Stock'
                dict['Name'].append(cname)
                dict['MRP'].append(cmrp)
                dict['Selling Price'].append(csp)
                dict['Weight'].append(cweight)
                dict['Category'].append(ccategory)
                dict['Sub-Category'].append(csub_category)
                dict['Availability'].append(cstock)
                dict['City'].append(city)
                dict['approx_quant'].append(cquantity)
                dict['Brand'].append(cbrand)
            count=count+1
        time.sleep(1)
        pageNo=pageNo+1
        print("Page No. ",pageNo)

    return dict
    # print(data)


def connect_with_sheet(sheet_name):
  gc = pygsheets.authorize(service_file='google_sheet_credentials.json')
  sh = gc.open(sheet_name)
  return sh

# def upload_data(df, Location):
#     # data = json_data[query]
#     # data = read_from_bigquery(data)
#     # data = pd.DataFrame.from_records(data)
#     google_sheet_name = 'Scrappers1'
#     sh = connect_with_sheet(google_sheet_name)
#     wk1 = sh.worksheet('title', Location)
#     wk1.clear()
#     wk1.set_dataframe(df, (1, 1))
#     return


