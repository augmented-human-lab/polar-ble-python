import time
import string
import random

NEW_DAY_AVAILABLE = True
NEW_DATA_AVAILABLE = True

TEMPERATURE_LOW = -10
TEMPERATURE_HIGH = 40
TEMPERATURE = random.randint(TEMPERATURE_LOW, TEMPERATURE_HIGH)

temperatures_list = list()
site_and_temperature_dict = dict()

# SESSION 1
def get_daily_temperature():
    try:
        global TEMPERATURE
        TEMPERATURE = get_random_temperature(TEMPERATURE)
        generate_list_solution(TEMPERATURE)
        time.sleep(random.uniform(1, 2)) # simulate delay
        return TEMPERATURE
    except KeyboardInterrupt:
        exit()

def get_random_temperature(previous_temperature, max_change=2):
    temperature_change = random.uniform(-max_change, max_change)
    new_temperature = round(previous_temperature + temperature_change)
    return max(min(new_temperature, TEMPERATURE_HIGH), TEMPERATURE_LOW)

def generate_list_solution(temperature):
    temperatures_list.append(temperature)
    if len(temperatures_list) > 7:
        temperatures_list.pop(0)

def show_latest_7_temperatures():
    print(f"The latest 7 temperatures are {', '.join(str(temperature) for temperature in temperatures_list)}.\n")

# SESSION 2

def get_site_and_temperature_data():
    try:
        site_label = random.choice(string.ascii_uppercase)
        if site_label in site_and_temperature_dict:
            temperature_reading = get_random_temperature(site_and_temperature_dict[site_label][-1])
        else:
            temperature_reading = random.randint(TEMPERATURE_LOW, TEMPERATURE_HIGH)
        generate_dict_solution(site_label, temperature_reading)
        time.sleep(random.uniform(1, 2)) # simulate delay
        return site_label, temperature_reading
    except KeyboardInterrupt:
        exit()

def generate_dict_solution(site_label, temperature_reading):
     site_and_temperature_dict.setdefault(site_label, []).append(temperature_reading)

def show_grouped_site_and_temperature_data():
    sorted_site_labels = sorted(site_and_temperature_dict.items())
    for key, values in sorted_site_labels:
        temperatures = ', '.join(map(str, values))
        print(f"Site Label: {key} | Temperatures: {temperatures}")
    print()
