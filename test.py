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
