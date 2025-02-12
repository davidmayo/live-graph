import datetime
from pathlib import Path
import random
import time

MAX_VALUE = 100
MIN_VALUE = 50

DELAY_MIN_SECONDS = .1
DELAY_MAX_SECONDS = .1

rand = random.Random(40351)

DATA_PATH = Path("./sample_data.csv")

start_time = time.monotonic()

def random_walk_generator(start=0, step=1):
    value = start
    while True:
        value += rand.gauss(0, step)
        yield value

generator = random_walk_generator(start=75, step=1)

def generate_data():
    print(f"Generating data to {DATA_PATH}")
    with open(DATA_PATH, "w") as f:
        f.write("timestamp,seconds,value\n")
    generator = random_walk_generator(start=75, step=1)
    counter = 0
    while True:
        timestamp = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()
        seconds = time.monotonic() - start_time
        data = next(generator)
        print(f"Writing data point {counter:,} @ {datetime.datetime.now():%X}: {data}")
        with open(DATA_PATH, "a") as f:
            f.write(f"{timestamp},{seconds},{data}\n")
        time.sleep(rand.uniform(DELAY_MIN_SECONDS, DELAY_MAX_SECONDS))
        counter += 1


if __name__ == "__main__":
    generate_data()
