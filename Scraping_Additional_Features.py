from pyzillow.pyzillow import ZillowWrapper, GetDeepSearchResults
import pandas as pd

DF=pd.read_csv('Bronx_Zillow_Data.csv')
Street_Address = DF['Street_Address']

Index = [i for i,l in enumerate(Street_Address) if l[0].isdigit() == True]

Zip_Code = DF['Zip_Code']

Serial_Number = range(24)

Days_On_Market = DF[' Days_On_Market']
Days_On_Market = [Days_On_Market[l] for l in Index]

Bathrooms = DF['Bathrooms']
Bathrooms = [Bathrooms[l] for l in Index]

Bedrooms = DF['Bedrooms']
Bedrooms = [Bedrooms[l] for l in Index]

SQFT = DF['SQFT']
SQFT = [SQFT[l] for l in Index]

State = DF['State']
State = [State[l] for l in Index]

Street_Address = DF['Street_Address']

Monthly_Rental = DF['Monthly Rental']
Monthly_Rental = [Monthly_Rental[l] for l in Index]

Z_ID = []
Home_Type = []
Latitude = []
Longitude = []
Home_Size = []
Zest_LD = []

for i in Index:
    Address = Street_Address[i]
    ZipCode = str(Zip_Code[i])
    Zillow_Data = ZillowWrapper('X1-ZWz1fs16znu7m3_2vy2l')
    Deep_Search_Response = Zillow_Data.get_deep_search_results(Address, ZipCode)
    Result = GetDeepSearchResults(Deep_Search_Response)
    Z_ID.append(Result.zillow_id)
    Home_Type.append(Result.home_type)
    Latitude.append(Result.latitude)
    Longitude.append(Result.longitude)
    Home_Size.append(Result.home_size)
    Zest_LD.append(Result.zestimate_last_updated)
Street_Address = [Street_Address[l] for l in Index]
Zip_Code = [Zip_Code[l] for l in Index]

Columns = {'Serial_Number': Serial_Number, 'Zillow_ID':Z_ID, 'Street_Address':Street_Address, 'Home_Type': Home_Type, 'Latitude':Latitude, 'Longitude': Longitude, 'Home_Size': Home_Size, 'Bathrooms': Bathrooms, 'Bedrooms': Bedrooms, 'Zest_LD' : Zest_LD, 'State': State, 'Days_On_Market': Days_On_Market, 'Zip_Code': Zip_Code, 'Monthly_Rental': Monthly_Rental }
DF_FINAL = pd.DataFrame(Columns)
DF_FINAL.to_csv('Bronx_Zillow_Data_With_Additional_Features.csv')

