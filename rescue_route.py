import json
from collections import deque 
import heapq

#Validate Donations
def validate_donations(donations):
    if not isinstance(donations, list):
        raise ValueError("Donations must be a list.")

    seen_ids = set()
    for donation in donations:
        if not isinstance(donation, dict):
            raise ValueError("Donation must be an object.")
        for field in (
            "donation_id",
            "donor_name",
            "food_type",
            "quantity",
            "expiry_time",
            "pickup_area",
            "ready_time",
        ):
            if field not in donation:
                raise ValueError(f"Donation is missing {field}.")
        if len(donation) != 7:
            raise ValueError("Donation must contain exactly 7 fields.")

        donation_id = donation["donation_id"]
        donor_name = donation["donor_name"]
        food_type = donation["food_type"]
        quantity = donation["quantity"]
        expiry_time = donation["expiry_time"]
        pickup_area = donation["pickup_area"]
        ready_time = donation["ready_time"]

        if not isinstance(donation_id, str) or not donation_id.strip():
            raise ValueError("Donation must have a nonempty donation_id.")

        if donation_id in seen_ids:
            raise ValueError(f"Duplicate donation ID: {donation_id}")
        seen_ids.add(donation_id)

        if not isinstance(donor_name, str) or not donor_name.strip():
            raise ValueError(f"Donation must have a nonempty donor_name.")

        if not isinstance(food_type, str) or not food_type.strip():
            raise ValueError(f"Donation must have a nonempty food_type.")

        if not isinstance(quantity, int) or isinstance(quantity, bool) or quantity <= 0:
            raise ValueError(
                f"Donation {donation_id} must have a positive integer quantity."
            )

        if not isinstance(expiry_time, int) or isinstance(expiry_time, bool) or expiry_time < 0:
            raise ValueError(
                f"Donation {donation_id} must have a non-negative integer expiry_time."
            )

        if not isinstance(pickup_area, str) or not pickup_area.strip():
            raise ValueError(f"Donation must have a nonempty pickup_area.")

        if not isinstance(ready_time, int) or isinstance(ready_time, bool) or ready_time < 0:
            raise ValueError(
                f"Donation {donation_id} must have a non-negative integer ready_time."
            )

#Validate Recipients
def validate_recipients(recipients):
    if not isinstance(recipients, list):
        raise ValueError("Recipients must be a list.")

    seen_ids = set()
    for recipient in recipients:
        if not isinstance(recipient, dict):
            raise ValueError("Recipient must be an object.")
        for field in (
            "recipient_id",
            "organization_name",
            "accepted_food_types",
            "capacity",
            "area",
            "closing_time",
        ):
            if field not in recipient:
                raise ValueError(f"Recipient is missing {field}.")
        if len(recipient) != 6:
            raise ValueError("Recipient must contain exactly 6 fields.")

        recipient_id = recipient["recipient_id"]
        organization_name = recipient["organization_name"]
        accepted_food_types = recipient["accepted_food_types"]
        capacity = recipient["capacity"]
        area = recipient["area"]
        closing_time = recipient["closing_time"]

        if not isinstance(recipient_id, str) or not recipient_id.strip():
            raise ValueError(f"Recipient must have a nonempty recipient_id.")

        if recipient_id in seen_ids:
            raise ValueError(f"Duplicate recipient ID: {recipient_id}")
        seen_ids.add(recipient_id)

        if not isinstance(organization_name, str) or not organization_name.strip():
            raise ValueError(f"Recipient must have a nonempty organization_name.")

        if not isinstance(accepted_food_types, list):
            raise ValueError("Accepted_food_types must be a list.")
        for food_type in accepted_food_types:
            if not isinstance(food_type, str) or not food_type.strip():
                raise ValueError("Accepted food types must be nonempty strings.")

        if not isinstance(capacity, int) or isinstance(capacity, bool) or capacity < 0:
            raise ValueError(
                f"Recipient {recipient_id} must have a non-negative integer capacity."
            )

        if not isinstance(area, str) or not area.strip():
            raise ValueError(f"Recipient must have a nonempty area.")

        if not isinstance(closing_time, int) or isinstance(closing_time, bool) or closing_time < 0:
            raise ValueError(
                f"Recipient {recipient_id} must have a non-negative integer closing_time."
            )

#Validate Volunteers
def validate_volunteers(volunteers):
    if not isinstance(volunteers, list):
        raise ValueError("Volunteers must be a list.")

    seen_ids = set()
    for volunteer in volunteers:
        if not isinstance(volunteer, dict):
            raise ValueError("Volunteer must be an object.")
        for field in (
            "volunteer_id",
            "vehicle_capacity",
            "area",
            "availability_start",
            "availability_end",
            "max_pickups",
        ):
            if field not in volunteer:
                raise ValueError(f"Volunteer is missing {field}.")
        if len(volunteer) != 6:
            raise ValueError("Volunteer must contain exactly 6 fields.")

        volunteer_id = volunteer["volunteer_id"]
        vehicle_capacity = volunteer["vehicle_capacity"]
        area = volunteer["area"]
        availability_start = volunteer["availability_start"]
        availability_end = volunteer["availability_end"]
        max_pickups = volunteer["max_pickups"]

        if not isinstance(volunteer_id, str) or not volunteer_id.strip():
            raise ValueError(f"Volunteer must have a nonempty volunteer_id.")

        if volunteer_id in seen_ids:
            raise ValueError(f"Duplicate volunteer ID: {volunteer_id}")
        seen_ids.add(volunteer_id)

        if not isinstance(vehicle_capacity, int) or isinstance(vehicle_capacity, bool) or vehicle_capacity < 0:
            raise ValueError(
                f"Volunteer {volunteer_id} must have a non-negative integer vehicle_capacity."
            )

        if not isinstance(area, str) or not area.strip():
            raise ValueError(f"Volunteer must have a nonempty area.")

        if not isinstance(availability_start, int) or isinstance(availability_start, bool) or availability_start < 0:
            raise ValueError(
                f"Volunteer {volunteer_id} must have a non-negative integer availability_start."
            )

        if not isinstance(availability_end, int) or isinstance(availability_end, bool) or availability_end < 0:
            raise ValueError(
                f"Volunteer {volunteer_id} must have a non-negative integer availability_end."
            )

        if not isinstance(max_pickups, int) or isinstance(max_pickups, bool) or max_pickups < 0:
            raise ValueError(
                f"Volunteer {volunteer_id} must have a non-negative integer max_pickups."
            )

        if availability_start > availability_end:
            raise ValueError("Availability_start must not exceed availability_end.")

#Print record errors and keep only valid records, in input order.
def validate_records(records, validator, id_field, label):
    if not isinstance(records, list):
        raise ValueError(f"{label} must be a list.")

    valid_records = []
    seen_ids = set()
    for position, record in enumerate(records, start=1):
        try:
            validator([record])
            record_id = record[id_field]
            if record_id in seen_ids:
                raise ValueError(f"Duplicate {id_field}: {record_id}")
        except ValueError as error:
            print(f"Error in {label} record {position}: {error} Skipping record.")
            continue

        seen_ids.add(record_id)
        valid_records.append(record)

    return valid_records


#Validate input; expired donations remain valid for explained rejection.
def validate_data(data):
    if not isinstance(data, dict):
        raise ValueError("Input must be a JSON object.")
    for collection in ("donations", "recipients", "volunteers"):
        if collection not in data:
            raise ValueError(f"Input is missing {collection}.")

#Return valid records; print and skip invalid individual records.
    return {
        "donations": validate_records(
            data["donations"], validate_donations, "donation_id", "donations"
        ),
        "recipients": validate_records(
            data["recipients"], validate_recipients, "recipient_id", "recipients"
        ),
        "volunteers": validate_records(
            data["volunteers"], validate_volunteers, "volunteer_id", "volunteers"
        ),
    }


def load_data(path):
    with open(path, encoding="utf-8") as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError as error:
            raise ValueError(f"Invalid JSON in {path}: {error.msg}") from error
    data = validate_data(data)
    donations = data["donations"]
    recipients = data["recipients"]
    volunteers = data["volunteers"]
    return donations, recipients, volunteers

def check_feasible_match(donation, recipient, volunteer, remaining_capacity, remaining_pickups):
    if not isinstance(remaining_capacity, int) or isinstance(remaining_capacity, bool) or remaining_capacity < 0:
        raise ValueError("remaining_capacity must be a non-negative integer")
    if not isinstance(remaining_pickups, int) or isinstance(remaining_pickups, bool) or remaining_pickups < 0:
        raise ValueError("remaining_pickups must be a non-negative integer")
    if donation["food_type"] not in recipient["accepted_food_types"]:
        return False, "recipient does not accept " + donation["food_type"]
    if not (donation["pickup_area"] == recipient["area"] == volunteer["area"]):
        return False, "area mismatch"
    if remaining_capacity < donation["quantity"]:
        return False, "recipient capacity exceeded"
    if volunteer["vehicle_capacity"] < donation["quantity"]:
        return False, "volunteer vehicle is too small"
    if remaining_pickups <= 0:
        return False, "volunteer has no pickups left"
    scheduled_time = max(donation["ready_time"], volunteer["availability_start"])
    if scheduled_time >= donation["expiry_time"]:
        return False, "donation expires before pickup can be completed"
    if scheduled_time > recipient["closing_time"]:
        return False, "cannot deliver before recipient closes"
    if scheduled_time > volunteer["availability_end"]:
        return False, "volunteer is not available in time"
    return True, "feasible"

def fifo_match(donations, recipients, volunteers):
    waiting_donations = deque(donations)
    assignments = []
    remaining_capacity = {}
    remaining_pickups = {}

    for recipient in recipients:
        remaining_capacity[recipient["recipient_id"]] = recipient["capacity"]

    for volunteer in volunteers:
        remaining_pickups[volunteer["volunteer_id"]] = volunteer["max_pickups"]


    while waiting_donations:
        donation = waiting_donations.popleft()
        matched = False

        rejection_reasons = []
        if not recipients:
            rejection_reasons.append("no recipients were provided")
        if not volunteers:
            rejection_reasons.append("no volunteers were provided")

        print("Processing donation:", donation["donation_id"])

        for recipient in recipients:
            print("Checking recipient:", recipient["recipient_id"])

            for volunteer in volunteers:
                print("Checking volunteer:", volunteer["volunteer_id"])

                feasible, reason = check_feasible_match(
                    donation,
                    recipient,
                    volunteer,
                    remaining_capacity[recipient["recipient_id"]],
                    remaining_pickups[volunteer["volunteer_id"]],
                )

                if not feasible:
                    if reason not in rejection_reasons:
                        rejection_reasons.append(reason)
                    continue

                if feasible:
                    scheduled_time = max( donation["ready_time"], volunteer["availability_start"])
                    assignment = {
                        "donation_id": donation["donation_id"],
                        "recipient_id": recipient["recipient_id"],
                        "volunteer_id": volunteer["volunteer_id"],
                        "scheduled_time": scheduled_time,
                        "status": "assigned",
                        "reason": (
                            f"Donation {donation['donation_id']} was assigned to "
                            f"{recipient['organization_name']} with volunteer "
                            f"{volunteer['volunteer_id']} because it expires in "
                            f"{donation['expiry_time'] - scheduled_time} minutes at pickup, "
                            f"the recipient accepts {donation['food_type'].replace('_', ' ')}, "
                            "capacity is available, and the volunteer can carry the quantity."
                        )
                    }

                    assignments.append(assignment)

                    remaining_capacity[recipient["recipient_id"]] -= donation["quantity"]
                    remaining_pickups[volunteer["volunteer_id"]] -= 1

                    matched = True
                    break

            if matched:
                break

        if not matched:
            assignment = {
                "donation_id": donation["donation_id"],
                "recipient_id": None,
                "volunteer_id": None,
                "scheduled_time": None,
                "status": "unassigned",
                "reason": "; ".join(rejection_reasons),
            }

            assignments.append(assignment)

    return assignments

def greedy_match(donations, recipients, volunteers):
    waiting_donations = deque(sorted(donations, key=greedy_priority))
  
    assignments = []
    remaining_capacity = {}
    remaining_pickups = {}
  
    for recipient in recipients:
        remaining_capacity[recipient["recipient_id"]] = recipient["capacity"]

    for volunteer in volunteers:
        remaining_pickups[volunteer["volunteer_id"]] = volunteer["max_pickups"]

    while waiting_donations:
        donation = waiting_donations.popleft()
        matched = False

        rejection_reasons = []
        if not recipients:
            rejection_reasons.append("no recipients were provided")
        if not volunteers:
            rejection_reasons.append("no volunteers were provided")

        print("Greedy processing donation:", donation["donation_id"], "| Expiry:", donation["expiry_time"])

        for recipient in recipients:
            for volunteer in volunteers:
                feasible, reason = check_feasible_match(
                    donation,
                    recipient,
                    volunteer,
                    remaining_capacity[recipient["recipient_id"]],
                    remaining_pickups[volunteer["volunteer_id"]],
                )

                if not feasible:
                    if reason not in rejection_reasons:
                        rejection_reasons.append(reason)
                    continue
                
                if feasible:
                    scheduled_time = max( donation["ready_time"], volunteer["availability_start"])
                    assignment = {
                        "donation_id": donation["donation_id"],
                        "recipient_id": recipient["recipient_id"],
                        "volunteer_id": volunteer["volunteer_id"],
                        "scheduled_time": scheduled_time,
                        "status": "assigned",
                        "reason": (
                            f"Donation {donation['donation_id']} was assigned to "
                            f"{recipient['organization_name']} with volunteer "
                            f"{volunteer['volunteer_id']} because it expires in "
                            f"{donation['expiry_time'] - scheduled_time} minutes at pickup, "
                            f"the recipient accepts {donation['food_type'].replace('_', ' ')}, "
                            "capacity is available, and the volunteer can carry the quantity."
                        )
                    }

                    assignments.append(assignment)

                    remaining_capacity[recipient["recipient_id"]] -= donation["quantity"]
                    remaining_pickups[volunteer["volunteer_id"]] -= 1

                    matched = True
                    break

            if matched:
                break

        if not matched:
            assignment = {
                "donation_id": donation["donation_id"],
                "recipient_id": None,
                "volunteer_id": None,
                "scheduled_time": None,
                "status": "unassigned",
                "reason": "; ".join(rejection_reasons),
            }

            assignments.append(assignment)

    return assignments


def greedy_priority(donation):
    return (donation["expiry_time"], -donation["quantity"], donation["ready_time"])

if __name__ == "__main__":
    donations, recipients, volunteers = load_data("data/input_sample.json")
    
    assignments = fifo_match(donations, recipients, volunteers)

    print("\n--- FIFO Assignments ---")
    for assignment in assignments:
        print(assignment)

    print("\n--- Greedy Processing Order ---")
    greedy_assignments = greedy_match(donations, recipients, volunteers)

    for assignment in greedy_assignments:
        print(assignment)