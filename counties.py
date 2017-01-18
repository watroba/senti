'''
Created on Oct 27, 2016


@author: Joseph
'''
import collections
#NOTES:
#Highest pop: Pulaski, 382748
#Lowest pop:  Calhoun, 5368

    #"key":("CountyName","CountySeatName",population,lat,long),
    #note: geoJSON uses a different format for coordinates (LON,LAT)

d ={"0":("Arkansas","De Witt",19019,34.2354,-91.2891),
        "1":("Ashley","Hamburg",21853,33.1566,-91.7539),
        "2":("Baxter","Mountain Home",41513,36.3262,-92.3814),
        "3":("Benton","Bentonville",221339,36.2662,-94.4800),
        "4":("Boone","Harrison",36903,36.3119,-93.0176),
        "5":("Bradley","Warren",11508,33.5081,-92.2237),
        "6":("Calhoun","Hampton",5368,33.5021,-92.5396),
        "7":("Carroll","Berryville",27446,36.2987,-93.5003),
        "8":("Chicot","Lake Village",11800,33.3420,-91.2891),
        "9":("Clark","Arkadelphia",22995,34.0232,-93.1780),
        "10":("Clay","Piggott",16083,36.3492,-90.3748),
        "11":("Cleburne","Heber Springs",25970,35.4606,-92.0665),
        "12":("Cleveland","Rison",8689,33.8658,-92.2237),
        "13":("Columbia","Magnolia",24552,33.1285,-93.1780),
        "14":("Conway","Morrilton",21273,35.2727,-92.6984),
        "15":("Craighead","Jonesboro",96443,35.8261,-90.6773),
        "16":("Crawford","Van Buren",61948,35.5763,-94.3154),
        "17":("Crittenden","Marion",50902,35.3021,-90.3748),         
        "18":("Cross","Wynne",17870,35.2999,-90.8294),
        "19":("Dallas","Fordyce",8116,34.0347,-92.6984),
        "20":("Desha","Arkansas City",13008,33.8774,-91.4435),
        "21":("Drew","Monticello",18509,33.5156,-91.7539),
        "22":("Faulkner","Conway",113237,35.1036,-92.3814),
        "23":("Franklin","Ozark",18125,35.5928,-93.8248),
        "24":("Fulton","Salem",12245,36.3797,-91.7928),
        "25":("Garland","Hot Springs",96024,34.5559,-93.1780),
        "26":("Grant","Sheridan",17853,34.2628,-92.4209),
        "27":("Greene","Paragould",42090,36.1315, -90.5636),
        "28":("Hempstead","Hope",22609,33.6530, -93.6623),
        "29":("Hot Spring","Malvern",32923,34.3394,-92.9776),
        "30":("Howard","Nashville",13789, 34.1318,94.0287),
        "31":("Independence","Batesville",36647,35.9174,-91.5984),
        "32":("Izard","Melbourne",13696,36.1611,-91.9099),
        "33":("Jackson","Newport",17997,35.6480,-91.1353),
        "34":("Jefferson","Pine Bluff",77435,34.2274,-91.9099),
        "35":("Johnson","Clarksville",25540,35.6026,-93.5004),
        "36":("Lafayette","Lewisville",7645,33.2512,93.6218),
        "37":("Lawrence","Walnut Ridge",17415, 35.9970,-91.1353),
        "38":("Lee","Marianna",10424,34.7713,-90.8294),
        "39":("Lincoln","Star City",14134,33.9185,-91.7150),
        "40":("Little River","Ashdown",13171,33.6809,-94.1923),
        "41":("Logan","Booneville",22353,35.2475,-93.6623),
        "42":("Lonoke","Lonoke",68356,34.7592,-91.9099),
        "43":("Madison","Huntsville",15717,35.9466,-93.6623),
        "44":("Marion","Yellville",16653,36.3195,-92.6984),
        "45":("Miller","Texarkana",43462,33.3336,-93.8655),
        "46":("Mississippi","Blytheville",46480,35.8280,-90.0747),
        "47":("Monroe","Clarendon",8149,34.5919,-91.1353),
        "48":("Montgomery","Mount Ida",9487,34.5424,-93.6623),
        "49":("Nevada","Prescott",8997,33.6621,-93.3389),
        "50":("Newton","Jasper",8330,35.9604,-93.1780),
        "51":("Ouachita","Camden",26120,33.5829,-92.9376),
        "52":("Perry","Perryville",10445,34.9603,-92.8976),
        "53":("Phillips","Helena",21757,34.4611,-90.8675),
        "54":("Pike","Murfreesboro",11291,34.1877,-93.6623),
        "55":("Poinsett","Harrisburg",24583,35.6079,-90.6394),
        "56":("Polk","Mena",20662,34.5268,-94.1514),
        "57":("Pope","Russellville",61754,35.4406,-93.0176),
        "58":("Prairie","Des Arc",8715,34.7636,-91.5984),
        "59":("Pulaski","Little Rock",382748,34.7539,-92.2237),
        "60":("Randolph","Pocahontas",17969,36.3458,-90.9821),
        "61":("St. Francis","Forrest",28258,34.9927,-90.7153),
        "62":("Saline","Benton",107118,34.5708,-92.5396),
        "63":("Scott","Waldron",11233,34.8855,-93.9878),
        "64":("Searcy","Marshall",8195,35.9721,-92.6984),
        "65":("Sebastian","Fort Smith",125744,35.2260,-94.3154),
        "66":("Sevier","De Queen",17058,34.0346,-94.2744),
        "67":("Sharp","Ash Flat",17264,36.1676,-91.4435),
        "68":("Stone","Mountain View",12394,35.8075,-92.2237),
        "69":("Union","El Dorado",41639,33.1431,-92.5396),
        "70":("Van Buren","Clinton",17295,35.6266,-92.5396),
        "71":("Washington","Fayetteville",203065,35.9308,-94.1514),
        "72":("White","Searcy",77076,35.2901,-91.7539),
        "73":("Woodruff","Augusta",7260,35.1226,-91.1353),
        "74":("Yell","Dardanelle",22185,35.0811,93.3389)
        }

od = collections.OrderedDict([('0', ('Arkansas', 'De Witt', 19019, 34.2354, -91.2891)), 
             ('1', ('Ashley', 'Hamburg', 21853, 33.1566, -91.7539)), 
             ('2', ('Baxter', 'Mountain Home', 41513, 36.3262, -92.3814)), 
             ('3', ('Benton', 'Bentonville', 221339, 36.2662, -94.48)), 
             ('4', ('Boone', 'Harrison', 36903, 36.3119, -93.0176)), 
             ('5', ('Bradley', 'Warren', 11508, 33.5081, -92.2237)), 
             ('6', ('Calhoun', 'Hampton', 5368, 33.5021, -92.5396)), 
             ('7', ('Carroll', 'Berryville', 27446, 36.2987, -93.5003)), 
             ('8', ('Chicot', 'Lake Village', 11800, 33.342, -91.2891)), 
             ('9', ('Clark', 'Arkadelphia', 22995, 34.0232, -93.178)), 
             ('10', ('Clay', 'Piggott', 16083, 36.3492, -90.3748)), 
             ('11', ('Cleburne', 'Heber Springs', 25970, 35.4606, -92.0665)), 
             ('12', ('Cleveland', 'Rison', 8689, 33.8658, -92.2237)), 
             ('13', ('Columbia', 'Magnolia', 24552, 33.1285, -93.178)), 
             ('14', ('Conway', 'Morrilton', 21273, 35.2727, -92.6984)), 
             ('15', ('Craighead', 'Jonesboro', 96443, 35.8261, -90.6773)), 
             ('16', ('Crawford', 'Van Buren', 61948, 35.5763, -94.3154)), 
             ('17', ('Crittenden', 'Marion', 50902, 35.3021, -90.3748)), 
             ('18', ('Cross', 'Wynne', 17870, 35.2999, -90.8294)), 
             ('19', ('Dallas', 'Fordyce', 8116, 34.0347, -92.6984)), 
             ('20', ('Desha', 'Arkansas City', 13008, 33.8774, -91.4435)), 
             ('21', ('Drew', 'Monticello', 18509, 33.5156, -91.7539)), 
             ('22', ('Faulkner', 'Conway', 113237, 35.1036, -92.3814)), 
             ('23', ('Franklin', 'Ozark', 18125, 35.5928, -93.8248)), 
             ('24', ('Fulton', 'Salem', 12245, 36.3797, -91.7928)), 
             ('25', ('Garland', 'Hot Springs', 96024, 34.5559, -93.178)), 
             ('26', ('Grant', 'Sheridan', 17853, 34.2628, -92.4209)), 
             ('27', ('Greene', 'Paragould', 42090, 36.1315, -90.5636)), 
             ('28', ('Hempstead', 'Hope', 22609, 33.653, -93.6623)), 
             ('29', ('Hot Spring', 'Malvern', 32923, 34.3394, -92.9776)), 
             ('30', ('Howard', 'Nashville', 13789, 34.1318, 94.0287)), 
             ('31', ('Independence', 'Batesville', 36647, 35.9174, -91.5984)), 
             ('32', ('Izard', 'Melbourne', 13696, 36.1611, -91.9099)), 
             ('33', ('Jackson', 'Newport', 17997, 35.648, -91.1353)), 
             ('34', ('Jefferson', 'Pine Bluff', 77435, 34.2274, -91.9099)), 
             ('35', ('Johnson', 'Clarksville', 25540, 35.6026, -93.5004)), 
             ('36', ('Lafayette', 'Lewisville', 7645, 33.2512, 93.6218)), 
             ('37', ('Lawrence', 'Walnut Ridge', 17415, 35.997, -91.1353)), 
             ('38', ('Lee', 'Marianna', 10424, 34.7713, -90.8294)), 
             ('39', ('Lincoln', 'Star City', 14134, 33.9185, -91.715)), 
             ('40', ('Little River', 'Ashdown', 13171, 33.6809, -94.1923)), 
             ('41', ('Logan', 'Booneville', 22353, 35.2475, -93.6623)), 
             ('42', ('Lonoke', 'Lonoke', 68356, 34.7592, -91.9099)), 
             ('43', ('Madison', 'Huntsville', 15717, 35.9466, -93.6623)), 
             ('44', ('Marion', 'Yellville', 16653, 36.3195, -92.6984)), 
             ('45', ('Miller', 'Texarkana', 43462, 33.3336, -93.8655)), 
             ('46', ('Mississippi', 'Blytheville', 46480, 35.828, -90.0747)), 
             ('47', ('Monroe', 'Clarendon', 8149, 34.5919, -91.1353)), 
             ('48', ('Montgomery', 'Mount Ida', 9487, 34.5424, -93.6623)), 
             ('49', ('Nevada', 'Prescott', 8997, 33.6621, -93.3389)), 
             ('50', ('Newton', 'Jasper', 8330, 35.9604, -93.178)), 
             ('51', ('Ouachita', 'Camden', 26120, 33.5829, -92.9376)), 
             ('52', ('Perry', 'Perryville', 10445, 34.9603, -92.8976)), 
             ('53', ('Phillips', 'Helena', 21757, 34.4611, -90.8675)), 
             ('54', ('Pike', 'Murfreesboro', 11291, 34.1877, -93.6623)), 
             ('55', ('Poinsett', 'Harrisburg', 24583, 35.6079, -90.6394)), 
             ('56', ('Polk', 'Mena', 20662, 34.5268, -94.1514)), 
             ('57', ('Pope', 'Russellville', 61754, 35.4406, -93.0176)), 
             ('58', ('Prairie', 'Des Arc', 8715, 34.7636, -91.5984)), 
             ('59', ('Pulaski', 'Little Rock', 382748, 34.7539, -92.2237)), 
             ('60', ('Randolph', 'Pocahontas', 17969, 36.3458, -90.9821)), 
             ('61', ('St. Francis', 'Forrest', 28258, 34.9927, -90.7153)), 
             ('62', ('Saline', 'Benton', 107118, 34.5708, -92.5396)), 
             ('63', ('Scott', 'Waldron', 11233, 34.8855, -93.9878)), 
             ('64', ('Searcy', 'Marshall', 8195, 35.9721, -92.6984)), 
             ('65', ('Sebastian', 'Fort Smith', 125744, 35.226, -94.3154)), 
             ('66', ('Sevier', 'De Queen', 17058, 34.0346, -94.2744)), 
             ('67', ('Sharp', 'Ash Flat', 17264, 36.1676, -91.4435)), 
             ('68', ('Stone', 'Mountain View', 12394, 35.8075, -92.2237)), 
             ('69', ('Union', 'El Dorado', 41639, 33.1431, -92.5396)), 
             ('70', ('Van Buren', 'Clinton', 17295, 35.6266, -92.5396)), 
             ('71', ('Washington', 'Fayetteville', 203065, 35.9308, -94.1514)), 
             ('72', ('White', 'Searcy', 77076, 35.2901, -91.7539)), 
             ('72', ('Woodruff', 'Augusta', 7260,35.1226,-91.1353)), 
             ('73', ('Yell', 'Dardanelle', 22185, 35.0811, 93.3389))])
