from down import *
import json

url = 'http://download.geonames.org/export/dump/'

file1 = 'cities15000.zip'  
file2 = 'admin1CodesASCII.txt'
file3 = 'countryInfo.txt'

f1 = get_file(url,file1)
f2 = get_file(url,file2)
f3 = get_file(url,file3) #obtain countries dict

def to_list(f1):
    list_cities = []
    for it in f1:
        #print(it)
        list_cities.append(re.split('\t+?',it))
    return list_cities


list_cities = to_list(f1)  # 2, 4 ,5 ,8 ,10
list_regions = to_list(f2)  # 0 : Country.RegionNumber , 3 : RegionName
list_countries = to_list(f3)
#print(list1)


filter_cities = (
    ('name',        2),
    ('longitude',   4),
    ('latitude',    5),
    ('countrycode', 8),
    ('regioncode',  10),
    )

repair =[]

index_cities = 0
index_regions = index_countries = 0
registed_regions = []
registed_countries = []

list_cities_final = []
list_regions_final = []
list_countries_final = []
#populate 3 dictionaries

for it in list_cities:
    #it is city type list
    index_cities += 1
    tlkey = []
    tlvalue = [] 
    for i in filter_cities:                
        tlkey.append(i[0]) #access to name
        tlvalue.append(it[i[1]]) #access to number
    
    tlkey.append('id') #
    tlvalue.append(index_cities)
    code = it[8]+'.'+it[10]
    #print(code)
    if not code in registed_regions:
        if not it[8] in registed_countries:
            index_countries += 1
            registed_countries.append(it[8])
            reg1 = False
            for it3 in list_countries:
                if it3[0] == it[8]:
                    list_countries_final.append(dict({'id':index_countries,'name':it3[4],'countrycode':it3[0],'population':it3[7],'continent':it3[8],'currencycode':it3[10]}))
                    reg1 = True
                    break
            if not reg1:
                print('country not registred')

            
        reg = False
        index_regions += 1
        registed_regions.append(code)
        if it[10] in ['00']:  #if coderegion is 00

            list_regions_final.append(dict({"name":"Not Regions", 'id':index_regions,'id_country':index_countries}))


        else:
            
            for it2 in list_regions:
                if it2[0] == code:
                    list_regions_final.append(dict({'name':it2[2], 'id':index_regions, 'id_country':index_countries}))
                    reg = True
                    break
            if not reg:
                print(' city with id [ ' + str(index_cities)+ ' ] not register but not find region')








    tlkey.append('id_region')
    tlvalue.append(index_regions)
    tlkey.append('id_country')
    tlvalue.append(index_countries)
    list_cities_final.append(dict(zip(tlkey,tlvalue)))


json_dir = os.path.dirname(os.path.abspath(__file__))+'/JSON'

cities  =   {'cities':list_cities_final}  
regions =   {'regions':list_regions_final}
countries = {'countries':list_countries_final}




def to_json_file(data, output):
    if not os.path.isdir(json_dir):
        os.makedirs(json_dir)
    with open(os.path.join(json_dir,output)+'.json', 'w') as file:
        file.write(json.dumps(data, file, indent=4))

to_json_file(cities, 'cities')
to_json_file(regions, 'regions')
to_json_file(countries, 'countries')

