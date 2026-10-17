CPSC 335: Algorithms and Data Structures
- RescueRoute -
- GITHUB URL: [https://github.com/ptran2005/rescue_route](url)

This is a python commandline project that matches time-sensitive surplus food donations to compatible recipients and volunteer drivers. It uses a fifo algorithm as well as a greedy algorithm to compare and make decision for all donations. 
**This project is NOT approved for real food-handling, medical, emergency, or operational use.**



## Setup

Requires **Python 3.10+** and no needs for any other dependencies beside standard library

**macOS / Linux:**
```bash
# Run the application
python3 rescue_route.py

# Run the automated test 
python3 -m unittest test -v

# Windows:
# Run the application
python rescue_route.py

# Run the automated test
python -m unittest test -v
```
# This project is organized in the following procedures:
1. Load & validate - load_data reads the samples provided in the given JSON file, and calls validate_data which would eventually call validate_records to check each record and skip over the invalid ones
2. Feasibility check - check_feasible_match validates donation recipient-vollunteer and returns a reason corresponding to the situation
3. Scheduling - greedy_match and fifo_match are used for prioritizing feasible matches, tracking capacity and record every donations

# Algorithm:
- FIFO: process donations based on arrival order
- GREEDY: process donations based on priorities which is calculate using expiry_time, quantity, and ready_time

Greedy follows the rule of soonest food to expire. Although it is not fully optimized yet as there are still challenges that we encountered.

# Complexity:
- We have D for donations, R for recipients, and V for volunteers
- We used nested loop in our algorithm which would make our O complexity D x R x V. 
- For example, if we have 5 donations, 5 recipients and 5 volunteers, it would be 5 x 5 x 5 = 125 times and this is for **FIFO**

- Greedy also follows the same algorithm except with one additional part of the code which is the sorting (expiry_time, -quantity, and ready_time) 
- So technically they both run the same nested loop which would make complexity D x R x V BUT greedy also has its sorting system which would equates to Dlog(D) making the final time complexity for greedy sort: D x R x V + Dlog(D)

# Testing
15 Test in total in test.py file which includes:
- Normal match
- Duplicated id
- Expired donations
- Food-type mismatch
- Not enough capacity
- Vehicle too small
- No pickups left
- Competing donations
- Empty list
- FIFO vs Greedy
- Fairness and starvation test
- Greedy to test time
- Quantity priority

# Metrics & FIFO vs Greedy comparison
- FIFO processes donations in their original JSON list order, which represents arrival order. For each donation, it selects the first recipient-volunteer combination that passes the feasibility checks. Earlier donations receive access to capacity first.
- Greedy sorts donations by earliest expiration, then larger quantity, then earlier ready time. Donations tied on all three criteria retain their input order. After sorting, it uses the same first-feasible matching procedure as FIFO. Its local goal is to prioritize food with less time before expiration; it does not guarantee the greatest total rescued quantity.

```text
--- FIFO vs Greedy Comparison ---
donations_received : 0
donations_assigned : 0
donations_unassigned : 0
food_quantity_rescued : 0
food_quantity_at_risk : 0
recipient_capacity_utilization : 0.0
volunteer_capacity_utilization : 0.0
urgent_rescue_rate : 75.0
```

- Each difference is calculated as Greedy − FIFO. A negative value means FIFO’s value was higher; a positive value means Greedy’s value was higher. Higher values are not always better—for example, less food at risk is preferable.
- Both algorithms assigned 8 donations and rescued 90 units, producing zero differences for those metrics. However, they selected different donations, with greedy prioritizing earlier expiration.
- In this urgent rescue rate, the score is 75, which means Greedy was 75 percentage points higher than FIFO.

# Team contribution
- **Phat Tran** - Product & Quality Lead: Worked on validations, data, and output.
- **Kevin Lam** - Data matching & Test lead: Started the data checks as well as implementing the automated tests for the program
- **Eduardo Perez** -  Algorithm & Optimization Lead: Worked on the FIFO and Greedy schedulers as well as the metric calculations and algorithm comparisons

# AI usage
- chatGPT (openAI) was used during the preparation of this project to generate sample input data, including donations, recipients, and volunteers, to be tested by the algorithms. All AI-generated data was reviewed by the group. The algorithms and implementation are the original work of the group.
