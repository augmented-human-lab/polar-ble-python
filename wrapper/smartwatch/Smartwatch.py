import random
import threading 
import queue

from .WebSocketClient import *

heart_rate_list = list()
heart_and_mind_dict = dict()

buffered_queue = queue.Queue()
websocket_client = WebSocketClient(buffered_queue)
threading.Thread(target=websocket_client.create_connection, daemon=True).start()

# SESSION 1
def get_new_heart_rate_from_watch():
    try:
        heart_rate = buffered_queue.get()
        if heart_rate is None:
            exit()
        generate_list_solution(heart_rate)
        return heart_rate
    except KeyboardInterrupt:
        exit()

def generate_list_solution(heart_rate):
    heart_rate_list.append(heart_rate)
    if len(heart_rate_list) > 10:
        heart_rate_list.pop(0)

def show_latest_10_heart_rates():
    print(f"The latest 10 heart rates are {', '.join(str(heart_rate) for heart_rate in heart_rate_list)}.\n")

# SESSION 2
def get_heart_zone_and_mind_data():
    mental_state = random.choice(["Calm", "Neutral", "Active"])
    heart_rate_zone = round(int(get_new_heart_rate_from_watch()), -1)
    generate_dict_solution(heart_rate_zone, mental_state)
    return heart_rate_zone, mental_state

def generate_dict_solution(heart_rate_zone, mental_state):
     heart_and_mind_dict.setdefault(heart_rate_zone, []).append(mental_state)

def show_grouped_heart_and_mind_data():
    sorted_heart_rate_zones = sorted(heart_and_mind_dict.items())
    for key, values in sorted_heart_rate_zones:
        mental_states = ', '.join(values)
        print(f"Heart Rate Zone: {key} | Mental States: {mental_states}")
    print()
