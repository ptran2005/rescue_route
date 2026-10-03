import json
from collections import deque

def load_data(path):
    with open(path) as file:
        data = json.load(file)
    donations = data["donations"]
    recipients = data["recipients"]
    volunteers = data["volunteers"]
    return donations, recipients, volunteers

def check_feasible_match(donation, recipient, volunteer, remaining_capacity, remaining_pickups):
    if donation["food_type"] not in recipient["accepted_food_types"]:
        return False, "recipienet does not accept " + donation["food_type"]
    if not (donation["pickup_area"] == recipient["area"] == volunteer["area"]):
        return False, "area mismatch"
    if remaining_capacity < donation["quantity"]:
        return False, "recipient capacity exceeded"
    if volunteer["vehicle_capacity"] < donation["quantity"]:
        return False, "volunteer vehicle is too small"
    if remaining_pickups <= 0:
        return False, "volunteer has no pickups left"
    if donation["ready_time"] > recipient["closing_time"]:
        return False, "cannot deliver before recipient closes"
    if donation["ready_time"] > volunteer["availability_end"]:
        return False, "volunteer is not available in time"
    return True, "feasible"

def fifo_match(donations, recipients, volunteers):
    waiting_donations = deque(donations)
    assignments = []

    while waiting_donations:
        donation = waiting_donations.popleft()
        print("TESTING DONATIONS || Processing donation:", donation["donation_id"])

    return assignments

### Test code for FIFO
donations, recipients, volunteers = load_data("data/input_sample.json")

fifo_match(donations, recipients, volunteers)