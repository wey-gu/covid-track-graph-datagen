import csv
import re

from faker import Faker
from random import randint, random

PERSON_COUNT = 10000
CONFIRMED_PROBABILITY = 0.001
CONFIRMED_START_DATE = "-100d"
ADDR_COUNT = 1000
STREET_COUNT = 667910
PERSON_LIVEWITH_COUNT = 20000
PERSON_VISIT_COUNT = 20000
CORP_REL_COUNT = 100
CORP_SHAREHOLD_COUNT = 200
PERSON_REL_COUNT = 1000
PERSON_ROLE_COUNT = 5000

WRITE_BATCH = 1000


def csv_writer(file_path, row_count, row_generator, index=False, index_prefix=""):
    with open(file_path, mode='w') as file:
        if index:
            cursor = 0
        writer = csv.writer(
            file, delimiter=',', quotechar="'", quoting=csv.QUOTE_MINIMAL)
        csv_buffer = list()
        for row in range(row_count):
            if index:
                csv_buffer.append((f"{index_prefix}{cursor}",) + row_generator())
                cursor += 1
            else:
                csv_buffer.append(row_generator())
            if len(csv_buffer) > WRITE_BATCH:
                writer.writerows(csv_buffer)
                del csv_buffer[:]
        if csv_buffer:
            writer.writerows(csv_buffer)
            del csv_buffer[:]


faker = Faker("zh_CN")

# PERSON
def person_generator():
    """
    (name, is_confirmed, confirmed_time)
    """
    is_confirmed = random() < CONFIRMED_PROBABILITY
    confirmed_time = "" if not is_confirmed else faker.date_time_between(
        start_date=CONFIRMED_START_DATE, end_date='now').timestamp()
    return (
        faker.name(),
        is_confirmed,
        confirmed_time)

csv_writer(
    'data/person.csv',
    PERSON_COUNT,
    person_generator,
    index=True,
    index_prefix="p_")

# ADDRESS
def address_generator():
    """
    (name, street)
    """
    return (
        re.split('市|县', faker.address())[-1],
        f"s_{randint(1, STREET_COUNT)}")

csv_writer(
    'data/address.csv',
    ADDR_COUNT,
    address_generator,
    index=True,
    index_prefix="a_")

# PERSON live_with RELATION
def person_livewith_generator():
    """
    (pid, pid, start_time, end_time)
    """
    t1 = faker.date_time_between(
        start_date=CONFIRMED_START_DATE, end_date='now').timestamp()
    t2 = faker.date_time_between(
        start_date=CONFIRMED_START_DATE, end_date='now').timestamp()
    start_time = min(t1, t2)
    end_time = max(t1, t2)
    return (
        'p_'+str(randint(0, PERSON_COUNT-1)),
        'p_'+str(randint(0, PERSON_COUNT-1)),
        start_time,
        end_time)

csv_writer(
    'data/person_livewith.csv',
    PERSON_LIVEWITH_COUNT,
    person_livewith_generator)

# PERSON visit RELATION
def person_visit_generator():
    """
    (pid, aid, start_time, end_time)
    """
    t1 = faker.date_time_between(
        start_date=CONFIRMED_START_DATE, end_date='now').timestamp()
    t2 = faker.date_time_between(
        start_date=CONFIRMED_START_DATE, end_date='now').timestamp()
    start_time = min(t1, t2)
    end_time = max(t1, t2)
    return (
        'p_'+str(randint(0, PERSON_COUNT-1)),
        'a_'+str(randint(0, ADDR_COUNT-1)),
        start_time,
        end_time)

csv_writer(
    'data/person_visit.csv',
    PERSON_VISIT_COUNT,
    person_visit_generator)
