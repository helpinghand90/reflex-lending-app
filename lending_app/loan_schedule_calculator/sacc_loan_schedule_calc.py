
import datetime
import logging
from lending_app.config import logging  

from dateutil.relativedelta import relativedelta
from lending_app.utilities import generate_short_alphanumeric_uuid, complete_months_between


# TODO: add more tests for errors and edge cases


def generate_loan_schedule(
    payment_frequency, loan_amount, selected_loan_term_months: int, start_date
):
    logging.info(
        f""""Generating loan schedule: 
                 payment_frequency: {payment_frequency}, 
                 loan_amount: {loan_amount}, 
                 selected_loan_term_months: {selected_loan_term_months},  
                 start_date: {start_date} """
    )
    """
    Generates a loan schedule with a monthly fee and payment dates.

    Args:
      payment_frequency: The frequency of payments ('weekly', 'fortnightly', 'monthly').
      loan_amount: The original loan amount.
      loan_term: The loan term in years.
      start_date: The date the loan starts (e.g., '2024-03-15') in YYYY-MM-DD format.
    """

    loan_id = generate_short_alphanumeric_uuid("loan")

    # Validate inputs
    if payment_frequency.lower() not in ("weekly", "fortnightly", "monthly"):
        raise ValueError(
            "Invalid payment frequency. Must be 'weekly', 'fortnightly', or 'monthly'"
        )
    if (
        not isinstance(loan_amount, (int, float))
        or loan_amount < 500
        or loan_amount > 2000
    ):
        raise ValueError("Loan amount must be a positive number between 500 and 2000")
    if (
        not isinstance(selected_loan_term_months, int)
        or selected_loan_term_months < 1
        or selected_loan_term_months > 12
    ):
        raise ValueError("Loan term must be a positive number betwwen 1 and 12")
    try:
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Invalid start date format. Please use YYYY-MM-DD.")

    estimated_end_date = start_date + relativedelta(months=selected_loan_term_months)
    logging.info(f"Loan schedule starting on {start_date}")
    monthly_fee = 0.04 * loan_amount
    logging.info(f"Monthly fee: {monthly_fee}")
    establishment_fee = 0.2 * loan_amount
    logging.info(f"Establishment fee: {establishment_fee}")

    if payment_frequency.lower() == "weekly":
        # Calculate the difference in days between start and end date
        days_diff = (estimated_end_date - start_date).days
        # Calculate the total number of complete weeks
        total_payments = days_diff // 7
        repayment_step = datetime.timedelta(weeks=1)
        end_date = start_date + relativedelta(weeks=total_payments)
        loan_term_months = complete_months_between(start_date, end_date)

    elif payment_frequency.lower() == "fortnightly":

        # Calculate the difference in days between start and end date
        days_diff = (estimated_end_date - start_date).days
        # Calculate the total number of complete fortnights
        total_payments = days_diff // 14
        repayment_step = datetime.timedelta(weeks=2)
        end_date = start_date + relativedelta(weeks=total_payments * 2)
        loan_term_months = complete_months_between(start_date, end_date)

    elif payment_frequency.lower() == "monthly":
        total_payments = selected_loan_term_months
        repayment_step = relativedelta(months=1)
        loan_term_months = selected_loan_term_months
        end_date = estimated_end_date

    else:
        raise ValueError(
            "Invalid payment frequency. Must be 'weekly', 'fortnightly', or 'monthly'"
        )

    logging.info(f"Total payments: {total_payments}")
    logging.info(f"Repayment step: {repayment_step}")

    repayment_amount = round(
        (loan_amount + establishment_fee + monthly_fee * loan_term_months)
        / total_payments,
        ndigits=2,
    )
    logging.info(f"Repayment amount: {repayment_amount}")

    # Initialize variables
    loan_transactions = []

    # add disbursement transactions
    data = {
        "loan_id": loan_id,
        "transaction_date": start_date,
        "transaction_type": "disbursement",
        "amount": loan_amount,
    }
    loan_transactions.append(data)

    # add disbursement transactions
    data = {
        "loan_id": loan_id,
        "transaction_date": start_date,
        "transaction_type": "Establishment Fee",
        "amount": establishment_fee,
    }
    loan_transactions.append(data)

    current_date = start_date + repayment_step

    # add repayment transactions
    while current_date <= end_date:
        data = {
            "loan_id": loan_id,
            "transaction_date": current_date,
            "transaction_type": "repayment",
            "amount": repayment_amount * -1,
        }
        loan_transactions.append(data)
        current_date += repayment_step

    # add monthly fee transactions
    current_date = start_date

    for i in range(0, loan_term_months):
        current_date += relativedelta(months=1)
        data = {
            "loan_id": loan_id,
            "transaction_date": current_date,
            "transaction_type": "monthly fee",
            "amount": monthly_fee,
        }
        loan_transactions.append(data)

    sorted_loan_transactions = sorted(
        loan_transactions, key=lambda x: (x["transaction_date"], x["transaction_type"])
    )
    total_amount_check = 0
    revenue = 0
    for transaction in sorted_loan_transactions:
        total_amount_check += transaction["amount"]
        revenue += (
            transaction["amount"]
            if transaction["transaction_type"] not in ["disbursement", "repayment"]
            else 0
        )

    if abs(round(total_amount_check, ndigits=2)) > 0.2:
        raise ValueError(
            f"Total amount of transactions does not match the loan amount {total_amount_check}"
        )

    if revenue < 0:
       raise ValueError(f"Total revenue below $0 - {revenue}")

    # add to loan_schedule table
    return {
        "revenue": revenue,
        "loan_schedule": sorted_loan_transactions,
    }



