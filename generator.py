from down import *
import json

url = 'http://download.geonames.org/export/dump/'

file1 = 'cities15000.zip'  
file2 = 'admin1CodesASCII.txt'
file3 = 'countryInfo.txt'

fcities = get_file(url,file1)
fregions = get_file(url,file2)
fcountries = get_file(url,file3) #obtain countries dict

list_cities = to_list(fcities)  # 2, 4 ,5 ,8 ,10
list_regions = to_list(fregions)  # 0 : Country.RegionNumber , 3 : RegionName
list_countries = to_list(fcountries)
#print(list1)


filter_cities = (
    ('name',        2),
    ('longitude',   4),
    ('latitude',    5),
    ('countrycode', 8),
    ('regioncode',  10),
    )
filter_regions = (
    ('name', 3),
    )

filter_countries=(
    ('code',    0),
    ('name',    4),
    ('population',    7),
    ('continent',    8),
    ('currency_code',    10),
    )



# Clean cities with wrong regions
def purge_db(list,list_regions):
    #this method is not efficient, but is more secure.
    cities_delete = 0
    print('##########  please wait for clean cities  ##########' )
    print('\n'*2)
    print('-'*50)

    for lj in list_regions:
        lj.append(0)

    for li in list:
        flag = False
        for lj in list_regions:
            code = li[8] + '.' + li[10]                                                     #this is more fast than #code = '%s.%s' % (li[8], li[10]                                                      # Flag variable
            if code == lj[0] or li[8]+':00' == lj[0]:
                flag = True
                if not lj[4]:                                                               #if lj[4] == 0  convert to 1
                    lj[4] = 1
                break
        if not flag:
            cities_delete+=1
            print('##########  delete city : '+ li[2] +' '+ li[8] )
            

            li.pop()
    



    for lj in list_regions:
        if not lj[4]:
            print('##########  delete regions '+ lj[2] +'#########')
            
    print('\n'*2)
    print('Delete '+str(cities_delete)+' cities')
    print('\n'*2)
    print('-'*50)
    print('########## cleaned cities with wrong region ##########' )



    return list


purge_db(list_cities, list_regions) 









# json_dir = os.path.dirname(os.path.abspath(__file__))+'/JSON'

# cities  =   {'cities':list_cities_final}  
# regions =   {'regions':list_regions_final}
# countries = {'countries':list_countries_final}




# def to_json_file(data, output):
#     if not os.path.isdir(json_dir):
#         os.makedirs(json_dir)
#     with open(os.path.join(json_dir,output)+'.json', 'w') as file:
#         file.write(json.dumps(data, file, indent=4))

# to_json_file(cities, 'cities')
# to_json_file(regions, 'regions')
# to_json_file(countries, 'countries')

