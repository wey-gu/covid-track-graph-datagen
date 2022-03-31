
## Data Schema

Vertex:
- `person(id: string, name: string, is_confirmed: bool, confirmed_at: datetime)`
- `address(id: string, name: string, street_id: string)`
- `street(id: string, name: string, city_id: string)`
- `city(id: string, name: string, province_id: string)`
- `province(id: string, name: string)`
- `district(id: string, name: string, city_id: string)`
- `town(id: string, name: string, district_id: string)`

Edge:
- `person_live_with_person(sid, did, start_time, end_time)`
- `person_visit_address(sid, did, start_time, end_time)`
- `belong_to(sid, did)`
  - > sid(source ID) could be {address, district, street, town, city} id, did(destination ID) could be {distict, street, town, city, province} id
  
    

## How to Generate Data

```bash
# install dependency
python3 -m pip install -r requirements.txt

# data generation
python3 data_generator.py

# Check files
$ tree data
data
├── address.csv
├── city.csv
├── district.csv
├── person.csv
├── person_livewith.csv
├── person_visit.csv
├── province.csv
├── street.csv
└── town.csv

0 directories, 9 files
```

### Data birdview

address.csv

```csv
a_0,翔安王街x座 420514,s_160127
a_1,房山张街V座 641042,s_605928
a_2,高坪淮安路B座 280940,s_131728
a_3,东丽太原路Y座 678891,s_292193
a_4,南溪永安街C座 960428,s_307763
```

city.csv

```csv
city_id,city_name,province_id
'1101', '市辖区', '11'
'1201', '市辖区', '12'
'1305', '邢台市', '13'
'1304', '邯郸市', '13'
```

district.csv

```csv
district_id,district_name,city_id
'110116', '怀柔区', '1101'
'110117', '平谷区', '1101'
'110114', '昌平区', '1101'
'110115', '大兴区', '1101'
```

 person.csv

```csv
p_0,焦明,False,
p_1,陈凤英,False,
p_2,金丹,False,
p_3,李婷,False,
p_4,葛娜,False,
p_5,曾璐,False,
p_6,朱秀荣,False,
```

person_livewith.csv

```csv
p_8717,p_5397,1644980628.0,1647218816.0
p_8752,p_4142,1640384466.0,1643261933.0
p_9877,p_1924,1642333831.0,1645039968.0
p_8762,p_5514,1640413494.0,1642081958.0
p_1650,p_2292,1646517804.0,1647573515.0
```

person_visit.csv

```csv
p_8429,a_142,1644193437.0,1647634538.0
p_1341,a_933,1645185598.0,1646532593.0
p_4358,a_387,1644457470.0,1644783704.0
p_9153,a_341,1642268021.0,1644437771.0
```

province.csv

```csv
province_id, province_name
'11', '北京市'
'12', '天津市'
'13', '河北省'
```

street.csv

```csv
incremental_id,street_id, street_name, town_id
s_1,'110112117236', '应寺村委会','110112117'
s_2,'110112117237', '熬硝营村委会','110112117'
s_3,'110112117238', '临沟屯村委会','110112117'
s_4,'110112105250', '苍上村委会','110112105'
```

town.csv

```csv
town_id, town_name, district_id
'110114013', '史各庄街道办事处', '110114'
'110114011', '回龙观街道办事处', '110114'
'110114012', '龙泽园街道办事处', '110114'
'110114010', '霍营街道办事处', '110114'
```



## Import to Nebula Graph

> With Nebula Importer, TBD