from pathlib import Path
from queue import Queue
import threading


class ReadCsvThread(threading.Thread):
    def __init__(self, csv_file: Path, data_queue: Queue | None):
        threading.Thread.__init__(self, daemon=True)
        self.csv_file = csv_file
        self.data_queue = data_queue or Queue()

    def run(self):
        with open(self.csv_file, 'r') as f:
            for line in f:
                self.data_queue.put(line)


if __name__ == "__main__":
    DATA_PATH = Path("./sample_data.csv")
    read_thread = ReadCsvThread(DATA_PATH)
    read_thread.start()
    import time
    time.sleep(5)