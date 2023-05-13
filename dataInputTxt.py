# def inputdata():sale_liter
#     fueltype = input("Enter Fuel Type   ")      
#                                     # Possible types 6
#                                     # if 92 : Enter 92
#                                     # if 95 : Enter 95
#                                     # if 97 : Enter 97
#                                     # if Disel : Enter HSD
#                                     # if Premium Disel : Enter PHSD    
#     saleprice = input("Enter Sale Price  (Maximum 4 digit) eg: 2519   ")
#     saleliter = input("Enter Sale Liter (Maximum 7 digits, 3 decimal format) eg: 2313.432  ")
#     totalprice = input("Enter Total Price (Maximum 7 digit) eg: 1562452  ")
#     totalizerliter = input("Enter Totalizerliter  (Maximum 10 digit, 3 decimal format) eg: 1523457.856 ")    #store PPRD License Num  => 6449f5a9a1808c9679bbed27
#     print("6449f5a9a1808c9679bbed27")
#     #create Vocno and store  => C1/07052023/1    # autogenerate
#     print("C1/07052023/1")
#     #create time and store   => 2023-04-29T04:38:13.399+00:00    # autogenerate
#     print("2023-04-29T04:38:13.399+00:00")    #Vehicle no => may be insert from POS GUI, if not => undefined    #Purpose of use => may be insert from POS GUI, if not => undefined    print(fueltype)
#     print(saleliter)
#     print(saleprice)
#     print(totalprice)
#     print(totalizerliter)
#     #store data
#     #send data to cloudinputdata()
# # inputdata()

"""
    Every 5 seconds - new item add
    Every 10 seconds - cloud upload to recover data while connection drop
"""

from db_config.query import Query
from datetime import datetime, timezone
import requests
import json
from time import sleep
import schedule

try :
    
    # input data 
    fuel_type = 92
    sale_price = 2519
    sale_liter = 2313.432
    total_price = 1562452
    totalizer_liter = 1523457.856

    # cloud upload 
    def cloud_upload () :
        print("......... Start cloud uploading ........")
        try :
            get_filter_data = {"sync_already":{"$eq":None}}
            get_result = Query.getOne(get_filter_data)
            print("get_result => ", get_result["message"])

            if get_result["data"] :

                get_result_data = get_result["data"]
                cloud_upload_data = get_result_data.copy()
                cloud_upload_url = "https://www.google.com" # Replace with your cloud url

                if cloud_upload_data :
                    del cloud_upload_data["_id"]

                    cloud_upload_response = requests.post(url=cloud_upload_url, json=json.dumps(cloud_upload_data))
                    print("cloud_upload_response => ", cloud_upload_response.status_code)

                    if cloud_upload_response.status_code == 200:
                        update_filter_data = {"_id":get_result_data["_id"]}
                        update_result = Query.updateOne(update_filter_data)
                        print("update_result => ", update_result["message"])
            print("......... End cloud uploading ........", "\n")
        except Exception as error :
            print({"Cloud Upload Error": error})

    # local store 
    def local_store (fuel_type, sale_price, sale_liter, total_price, totalizer_liter) :
        print("________ Start local store ________")
        try :
            current_date = datetime.now().strftime("%d%m%Y")
            current_time = datetime.now().strftime("%H%M%S%f")
            # utc_dt = datetime.now()
            utc_dt = datetime.now(timezone.utc) # using timezone.utc is 6:30 late with current time 
                                                # if u don't want, above one use but iso format is different
            created_at = utc_dt.isoformat()

            new_item = {
                "fuel_type" : fuel_type,
                "sale_price" : sale_price,
                "sale_liter" : sale_liter,
                "total_price" : total_price,
                "totalizer_liter" : totalizer_liter,
                "pprd_license_number" : "6449f5a9a1808c9679bbed27",
                "voucher_number" : f"C1/{current_date}/{current_time}",
                "sync_already" : None,
                "created_at" : created_at,
                "updated_at" : None,
                "deleted_at" : None

            }
            add_result = Query.addOne(new_item)
            print("add_result => ", add_result["message"])
            print("________ End local store ________", "\n")

            cloud_upload()
        except Exception as error :
            print({"Local Store Error": error})
    local_store(fuel_type, sale_price, sale_liter, total_price, totalizer_liter)
    
    # schedule timer
    def schedule_timer () :
        try :
            schedule.every(5).seconds.do(local_store, fuel_type, sale_price, sale_liter, total_price, totalizer_liter) # testing purpose schedule job only in current time
            schedule.every(10).seconds.do(cloud_upload) 
            while True:
                schedule.run_pending()
                sleep(1)
        except Exception as error :
            print({"Schedule Timer Error": error})
    schedule_timer()

except Exception as error :
    print({"Error": error})


