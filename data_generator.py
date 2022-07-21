import csv
import re

from faker import Faker
from random import randint, random
from multiprocessing import Pool
from rich.console import Console
from rich.table import Table
from rich.progress import Progress
from rich.syntax import Syntax


PERSON_COUNT = 100000
CONFIRMED_PROBABILITY = 0.001
CONFIRMED_START_DATE = "-100d"
ADDR_COUNT = 10000
STREET_COUNT = 667910
PERSON_LIVEWITH_COUNT = 20000
PERSON_VISIT_COUNT = 20000

WRITE_BATCH = 1000000 # Larger requires more memory
PROCESS_COUNT = 8 # Maximum partition size, put your CPU count here

console = Console()


def log(message):
    console.print("\n[bold bright_cyan][ Info:[/bold bright_cyan]", message)


def title(title, description=None):
    table = Table(show_header=True)
    table.add_column(title, style="dim", width=96)
    if description:
        table.add_row(description)
    console.print("\n", table)


def csv_writer(file_path, row_count, row_generator, index=False, index_prefix="", init_index=0):
    with open(file_path, mode='w') as file:
        if index:
            cursor = int(init_index)
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

# ADDRESS
def address_generator():
    """
    (name, street)
    """
    return (
        re.split('市|县', faker.address())[-1],
        f"s_{randint(1, STREET_COUNT)}")

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


def gen_person(i):
    csv_writer(
        f"data/person_{i}.csv",
        PERSON_COUNT // PROCESS_COUNT,
        person_generator,
        index=True,
        index_prefix=f"p_",
        init_index=i * PERSON_COUNT)

def gen_addr(i):
    csv_writer(
        f"data/address_{i}.csv",
        ADDR_COUNT // PROCESS_COUNT,
        address_generator,
        index=True,
        index_prefix=f"a_",
        init_index=i * ADDR_COUNT)

def gen_person_livewith(i):
    csv_writer(
        f"data/person_livewith_{i}.csv",
        PERSON_LIVEWITH_COUNT // PROCESS_COUNT,
        person_livewith_generator)


def gen_person_visit(i):
    csv_writer(
        f"data/person_visit_{i}.csv",
        PERSON_VISIT_COUNT // PROCESS_COUNT,
        person_visit_generator)

if __name__ == "__main__":

    with Progress() as progress:
        task = progress.add_task("[cyan]Progress:", total=4 * PROCESS_COUNT * 2)

        with Pool(processes=PROCESS_COUNT * 4) as pool:

            title(
                "[bold blue][ Init ] [/bold blue]",
                f"Will be running with maximum {PROCESS_COUNT} processes")

            step_0 = []
            for i in range(PROCESS_COUNT):
                step_0.append(pool.map_async(gen_person, (i, )))
                progress.advance(task)


            step_1 = []
            for i in range(PROCESS_COUNT):
                step_1.append(pool.map_async(gen_addr, (i, )))
                progress.advance(task)


            step_2 = []
            for i in range(PROCESS_COUNT):
                step_2.append(pool.map_async(gen_person_livewith, (i, )))
                progress.advance(task)

            step_3 = []
            for i in range(PROCESS_COUNT):
                step_3.append(pool.map_async(gen_person_visit, (i, )))
                progress.advance(task)

            for step in [step_0, step_1, step_2, step_3]:
                for p in step:
                    p.wait()
                    progress.advance(task)
