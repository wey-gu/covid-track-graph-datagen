
## Data Schema

Vertex:
- person(id: string, name: string, is_confirmed: bool, confirmed_at: datetime)
- address(id: string, name: string, street_id: string)
- street(id: string, name: string, city_id: string)
- city(id: string, name: string, province_id: string)
- province(id: string, name: string)
- district(id: string, name: string, city_id: string)
- town(id: string, name: string, district_id: string)

Edge:
- person_live_with_person(sid, did, start_time, end_time)
- person_visit_address(sid, did, start_time, end_time)
- belong_to(sid, did) # sid could be {address, district, street, town, city} id, did could be distict, street, town, city, province id

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
├── persion.csv
├── person_livewith.csv
├── person_visit.csv
├── province.csv
├── street.csv
└── town.csv

0 directories, 9 files
```

## Import to Nebula Graph

> With Nebula Importer, TBD