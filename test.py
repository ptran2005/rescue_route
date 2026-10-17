import unittest

from rescue_route import (
    check_feasible_match,
    fifo_match,
    greedy_match,
    validate_donations,
    validate_data
)

def make_donation(donation_id="D-1", food_type="produce", quantity=10, expiry_time=200, ready_time=0, pickup_area="Fullerton", donor_name="locals"):
    return {
        "donation_id": donation_id,
        "donor_name": donor_name,
        "food_type": food_type,
        "quantity": quantity,
        "expiry_time": expiry_time,
        "pickup_area": pickup_area,
        "ready_time": ready_time
    }
def make_recipient(recipient_id="R-1", accepted=None, capacity=50, area="Fullerton", closing_time=300, organization_name="Shelter"):
    return {
        "recipient_id": recipient_id,
        "organization_name": organization_name,
        "accepted_food_types": accepted if accepted is not None else ["produce"],
        "capacity": capacity,
        "area": area,
        "closing_time": closing_time
    }
def make_volunteer(volunteer_id="V-1", vehicle_capacity=20, area="Fullerton", availability_start=0, availability_end=300, max_pickups=3,):
    return {
        "volunteer_id": volunteer_id,
        "vehicle_capacity": vehicle_capacity,
        "area": area,
        "availability_start": availability_start,
        "availability_end": availability_end,
        "max_pickups": max_pickups,
    }

class TestFeasibleCheck(unittest.TestCase):
    def setUp(self):
        self.donation = {
            "donation_id": "D-1",
            "donor_name": "Local Market",
            "expiry_time": 180,
            "food_type": "produce",
            "quantity": 10,
            "pickup_area": "Fullerton",
            "ready_time": 0
        }
        self.recipient = {
            "recipient_id": "R-1",
            "organization_name": "Shelter",
            "accepted_food_types": ["produce"],
            "capacity": 50,
            "area": "Fullerton",
            "closing_time": 300
        }
        self.volunteer = {
            "volunteer_id": "V-1",
            "vehicle_capacity": 20,
            "area": "Fullerton",
            "availability_start": 0,
            "availability_end": 300,
            "max_pickups": 3
        }

    def test_feasible_match(self):
        ok, reason = check_feasible_match(self.donation, self.recipient, self.volunteer, 50, 3)
        self.assertTrue(ok)
        self.assertEqual(reason, "feasible")

    def test_capacity_exceeded(self):
        ok, reason = check_feasible_match(self.donation, self.recipient, self.volunteer, 5, 3)
        self.assertFalse(ok)
        self.assertEqual(reason, "recipient capacity exceeded")

    def test_no_pickup_left(self):
        ok, reason = check_feasible_match(self.donation, self.recipient, self.volunteer, 50, 0)
        self.assertFalse(ok)
        self.assertEqual(reason, "volunteer has no pickups left")

    def test_food_type_accepted(self):
        self.donation["food_type"] = "produce"
        ok, reason = check_feasible_match(self.donation, self.recipient, self.volunteer, 50, 2)
        self.assertTrue(ok)
        self.assertEqual(reason, "feasible")

    def test_vehicle_toosmall(self):
        self.donation["quantity"] = 30
        ok, reason = check_feasible_match(self.donation, self.recipient, self.volunteer, 50, 3)
        self.assertFalse(ok)
        self.assertEqual(reason, "volunteer vehicle is too small")

class TestValidation(unittest.TestCase):
    def test_duplicate_donation_id(self):
        donations = [
              make_donation(donation_id="D-1"),
              make_donation(donation_id="D-1"),
        ]
        with self.assertRaises(ValueError):
            validate_donations(donations)
    def test_empty_lists_valid(self):
            validate_data({"donations": [], "recipients": [], "volunteers": []})

class TestFeasibleRejection(unittest.TestCase):
    def test_expired_donation(self):
        donation = make_donation(expiry_time=0, ready_time=0)
        recipient = make_recipient()
        volunteer = make_volunteer()
        ok, reason = check_feasible_match(donation, recipient, volunteer, 50, 3)
        self.assertFalse(ok)
        self.assertEqual(reason, "donation expires before pickup can be completed")
    def test_food_type_not_accepted(self):
        donation = make_donation(food_type= "meat")
        recipient = make_recipient(accepted=["produce"])
        volunteer = make_volunteer()
        ok, reason = check_feasible_match(donation, recipient, volunteer, 50, 3)
        self.assertFalse(ok)
        self.assertEqual(reason, "recipient does not accept meat")

class TestStrategies(unittest.TestCase):
    def test_two_donations_comp_for_cap(self):
        donations = [
            make_donation(donation_id="D-1", quantity=10),
            make_donation(donation_id="D-2", quantity=10)
        ]
        recipient = make_recipient(capacity=10)
        volunteer = make_volunteer(max_pickups=5)

        assignments = fifo_match(donations, [recipient], [volunteer])
        statuses = {a["donation_id"]: a["status"] for a in assignments}

        self.assertEqual(statuses["D-1"], "assigned")
        self.assertEqual(statuses["D-2"], "unassigned")
    def test_fifo_empty_donations(self):
        assignments = fifo_match([], [make_recipient()], [make_volunteer()])
        self.assertEqual(assignments, [])
    def test_fifo_vs_greedy_dif(self):
        donation_early = make_donation(donation_id= "D-1", expiry_time=250, quantity=10)
        donation_urgent = make_donation(donation_id= "D-2", expiry_time=50, quantity=10)
        recipient = make_recipient(capacity=10)
        volunteer = make_volunteer(max_pickups=1)

        fifo = fifo_match([donation_early, donation_urgent], [recipient], [volunteer])
        greedy = greedy_match([donation_early, donation_urgent], [recipient], [volunteer])

        assigned_fifo = next(a["donation_id"] for a in fifo if a["status"] == "assigned")
        assigned_greedy = next(a["donation_id"] for a in greedy if a["status"] == "assigned")

        self.assertEqual(assigned_fifo, "D-1")  #arrive order
        self.assertEqual(assigned_greedy, "D-2")    #urgent first
        self.assertNotEqual(assigned_fifo, assigned_greedy)
    def test_greedy_fairness_starvation(self):
        slow_donation = make_donation(donation_id= "D-s", expiry_time=500, quantity=10)
        urgent1_donation = make_donation(donation_id= "D-u1", expiry_time=30, quantity=10)
        urgent2_donation = make_donation(donation_id= "D-u2", expiry_time=40, quantity=10)

        recipient = make_recipient(capacity=10)
        volunteer = make_volunteer(max_pickups=1)

        greedy = greedy_match([slow_donation, urgent1_donation, urgent2_donation], [recipient], [volunteer])
        status = {a["donation_id"]: a["status"] for a in greedy}

        self.assertEqual(status["D-u1"], "assigned")
        self.assertEqual(status["D-s"], "unassigned")
    def test_greedy_quantity_priority(self):
        donations = [
            make_donation(donation_id="D-1", quantity=5, expiry_time=100),
            make_donation(donation_id="D-2", quantity=10, expiry_time=100)
        ]

        recipient = make_recipient(capacity=10)
        volunteer = make_volunteer(max_pickups=2)

        greedy = greedy_match(donations, [recipient], [volunteer])

        self.assertEqual(greedy[0]["donation_id"], "D-2")
        self.assertEqual(greedy[0]["status"], "assigned")
        self.assertEqual(greedy[1]["donation_id"], "D-1")
        self.assertEqual(greedy[1]["status"], "unassigned")
    def test_greedy_ready_time_priority(self):
        donations = [
            make_donation(donation_id="D-1", expiry_time=100, ready_time=30),
            make_donation(donation_id="D-2", expiry_time=100, ready_time=10)
        ]

        recipient = make_recipient(capacity=10)
        volunteer = make_volunteer(max_pickups=2)

        greedy = greedy_match(donations, [recipient], [volunteer])

        self.assertEqual(greedy[0]["donation_id"], "D-2")
        self.assertEqual(greedy[0]["status"], "assigned")
        self.assertEqual(greedy[1]["donation_id"], "D-1")
        self.assertEqual(greedy[1]["status"], "unassigned")