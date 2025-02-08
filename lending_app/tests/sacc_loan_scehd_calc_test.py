import pytest
import sys
import os

# Add the root directory of the project to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from lending_app.loan_schedule_calculator.sacc_loan_schedule_calc import generate_loan_schedule



@pytest.mark.parametrize("payment_frequency, loan_amount, selected_loan_term_months, start_date, revenue", [
    ("weekly", 500, 1, '2024-03-15', 100.0),
    ("weekly", 1000, 3, '2024-03-15', 280.0),
    ("weekly", 1500, 6, '2024-03-15', 600.0),
    ("weekly", 2000, 12, '2024-03-15', 1280.0),
    ("fortnightly", 500, 1, '2024-03-15', 100.0),
    ("fortnightly", 1000, 3, '2024-03-15', 280.0),
    ("fortnightly", 1500, 6, '2024-03-15', 600.0),
    ("fortnightly", 2000, 12, '2024-03-15', 1280.0),
    ("monthly", 500, 1, '2024-03-15', 120.0),
    ("monthly", 1000, 3, '2024-03-15', 320.0),
    ("monthly", 1500, 6, '2024-03-15', 660.0),
    ("monthly", 2000, 12, '2024-03-15', 1360.0)
])
def test_loan_schedule(payment_frequency, loan_amount, selected_loan_term_months, start_date, revenue):
    try:
        result = generate_loan_schedule(payment_frequency, loan_amount, selected_loan_term_months, start_date)
        assert result["revenue"] == revenue
    except Exception as e:
        pytest.fail(f"generate_loan_schedule raised an exception: {e}")

