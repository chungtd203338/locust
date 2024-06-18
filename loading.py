from locust import HttpUser, task, events
import csv
import random
import time

class MyUser(HttpUser):
    # wait_time = constant(1)

    def on_start(self):
        self.inovation_count = self.read_csv("invocations_per_function_md.anon.csv")
        self.duration = self.read_csv("function_durations_percentiles.anon.csv")
        self.inovation_count_index = 0
        self.duration_index = 0

    def read_csv(self, file_path):
        data = []
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
        return data

    @task
    def execute_task(self):
        row_inovation_count = self.inovation_count[self.inovation_count_index]
        # self.inovation_count_index += 1
        row_duration = self.duration[self.duration_index]
        # self.duration_index += 1

        count = int(row_duration['Count'])
        # print(count)
        number = 1

        for x in range(1, 1441):
            times_per_minute = int(row_inovation_count[str(x)])
            print("Minute:",x)
            print("Times:", times_per_minute)
            for y in range(times_per_minute):
                random_int = self.get_random_int(number, count, row_duration)
                # print(random_int)
                self.client.get(f"/workload.php/?value={random_int}")
                number += 1
            time.sleep(1)

        if x == 1440:
            self.environment.runner.quit()

    def get_random_int(self, number, count, row):
        if number <= int(count * 0.01):
            return random.randint(int(row['percentile_Average_0']) + 1, int(row['percentile_Average_1']))
        elif number <= int(count * 0.25):
            return random.randint(int(row['percentile_Average_1']) + 1, int(row['percentile_Average_25']))
        elif number <= int(count * 0.5):
            return random.randint(int(row['percentile_Average_25']) + 1, int(row['percentile_Average_50']))
        elif number <= int(count * 0.75):
            return random.randint(int(row['percentile_Average_50']) + 1, int(row['percentile_Average_75']))
        elif number <= int(count * 0.99):
            return random.randint(int(row['percentile_Average_75']) + 1, int(row['percentile_Average_99']))
        else:
            return random.randint(int(row['percentile_Average_99']) + 1, int(row['percentile_Average_100']))

@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    print("Test finished!")
