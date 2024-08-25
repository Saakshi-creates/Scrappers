import time
import pandas as pd
import helper as help


def hello_http():
    # try:
        citys=help.get_city_dict()
        list=[]
        for city in citys:
            slugs=help.get_slugs(city)
            print(slugs)
            print(f"-----------{city}--------------")
            for slug in slugs:
                dict=help.get_vegetables(slug,city)
                list.append(dict)
                time.sleep(5)
                print(slug)


        pd_list = [pd.DataFrame(d) for d in list]
        df = pd.concat(pd_list, ignore_index=True)
        df = df.drop_duplicates()
        print(df)
        # print(df.to_string())
        # df.to_excel(r"C:\Users\Hello\Downloads\bb_mb.xlsx")

        google_sheet_name = 'Scrappers_FMCG'
        sheet_name = 'bb_scrapper'
        sh = help.connect_with_sheet(google_sheet_name)
        print(sh)

        wk1 = sh.worksheet('title', sheet_name)
        wk1.clear()
        wk1.set_dataframe(df, (1, 1))
        print("success")
    # except Exception as er:
    #
    #     ty, value, traceback = sys.exc_info()
    #     stack_trace = str(traceback) + " " + str(value) + " " + str(ty)
    #     data = {"text": stack_trace + "\n--BIG-BASKET-SCRAPPER--\n--------Something went wrong--------"}
    #     help.error_slack(data)
    #     raise er


# 110048




if __name__ == '__main__':
        hello_http()