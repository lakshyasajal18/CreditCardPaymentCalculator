"""Perform credit card calculations."""
from argparse import ArgumentParser
import sys

def get_min_payment(balance,fees=0):
    """Getting the minimum payment
    Args:
    balance(int)= The total amount of the balance in an account that is left to pay 
    fees(int)=The fees associated with the credit card account
    Output:
    min_payment(int): The minimum credit card payment
    """
    #Setting the value for m
    m=0.02
    #Using the formula to define the minimum payment
    min_payment=((balance * m)+ fees)
    #Condition when the minimum paymment is less than 25
    if min_payment<25:
        min_payment=25
    return min_payment

def interest_charged(balance,apr):
    """Calculating the interest charged
    Args:
    balance(int)=The total amount of the balance in an account that is left to pay
    apr(float)=The annual APR
    Output:
    i(int):the interest on the balance
    """
    #Setting the constants and formatting apr
    a=apr/100.0
    y=365
    d=30
    #using the formula to define the interest
    i=(a/y)*balance*d
    return i

def remaining_payments(balance, apr, targetamount, credit_line=5000, fees=0):
    """Calculating the number of payments required to pay off the credit card balance
    Args:
    balance(int)=The total amount of the balance in an account that is left to pay
    apr(float)=The annual APR
    targetamount(int)=The target payment 
    credit_line(int)=default credit line
    fees(int)=The fees associated with the credit card account
    Output:
    (int):The number of payments required to pay off the credit card balance along with the number of months required to pay off the balance depending on the the balance spends over 75%,50% and 25% of the maximum allowed credit line.
    """
    # Initializing the counters
    num_payments = 0
    over_75_counter = 0
    over_50_counter = 0
    over_25_counter = 0
    while balance > 0:
        # Determining the payment amount
        if targetamount is None:
            payment = get_min_payment(balance, fees)
        else:
            payment = targetamount   
        # Setting the interest charged
        interest = interest_charged(balance, apr)  
        # Calculating the amount going towards balance
        balance_payment = payment - interest 
        # Condition when balance_payment is negative
        if balance_payment < 0:
            print("The card balance cannot be paid off.")
            #quitting the function
            quit()
        # Reducing the balance by payment amount
        balance -= balance_payment 
        # Checking if the balance exceeds certain thresholds and increasing the counters accordingly
        if balance >= 0.75 * credit_line:
            over_75_counter += 1
        if balance >= 0.50 * credit_line:
            over_50_counter += 1
        if balance >= 0.25 * credit_line:
            over_25_counter += 1   
        # Incrementing the total payment counter
        num_payments += 1   
    # Returning the counters as a tuple
    return (num_payments, over_25_counter, over_50_counter, over_75_counter)

def main(balance, apr, targetamount=None, credit_line=5000, fees=0):
    """Displaying all of the information
    Args:
    balance(int)=The total amount of the balance in an account that is left to pay
    apr(float)=The annual APR
    targetamount(int)=The target payment 
    credit_line(int)=default credit line
    fees(int)=The fees associated with the credit card account
    Output:
    string:statements including the information on how many months they would need to pay off the balance and the total number of payments they would have to make"""
    # Setting the recommended minimum payment
    min_payment = get_min_payment(balance, fees)
    # tracking if the user pays the minimum amount
    pays_minimum = False
    payments_info = remaining_payments(balance, apr, targetamount, credit_line, fees)
    if targetamount is None:
        pays_minimum = True
    elif targetamount < min_payment:
        return "Your target payment is less than the minimum payment for this credit card"
    print("Your recommended starting minimum payment is $", min_payment,".")
    if pays_minimum:
        print("If you pay the minimum payments each month, you will pay off the balance in", payments_info[0], "payments.")      
    else:
        print("If you make payments of $", targetamount, ", you will pay off the credit card in", payments_info[0], "payments")
    # Creating the result string
    result_string = f"You will spend a total of {payments_info[1]} months over 25% of the credit line\n"
    result_string += f"You will spend a total of {payments_info[2]} months over 50% of the credit line\n"
    result_string += f"You will spend a total of {payments_info[3]} months over 75% of the credit line"
    return result_string

def parse_args(args_list):
    """Takes a list of strings from the command prompt and passes them through as
    arguments
    Args:
        args_list (list) : the list of strings from the command prompt
    Returns:
        args (ArgumentParser)
    """
    parser = ArgumentParser()
    parser.add_argument('balance_amount', type = float, help = 'The total amount of balance left on the credit account')
    parser.add_argument('apr', type = int, help = 'The annual APR, should be an int between 1 and 100')
    parser.add_argument('credit_line', type = int, help = 'The maximum amount of balance allowed on the credit line.')
    parser.add_argument('--payment', type = int, default = None, help = 'The amount the user wants to pay per payment, should be a positive number')
    parser.add_argument('--fees', type = float, default = 0, help = 'The fees that are applied monthly.')
    # parse and validate arguments
    args = parser.parse_args(args_list)
    if args.balance_amount < 0:
        raise ValueError("balance amount must be positive")
    if not 0 <= args.apr <= 100:
        raise ValueError("APR must be between 0 and 100")
    if args.credit_line < 1:
        raise ValueError("credit line must be positive")
    if args.payment is not None and args.payment < 0:
        raise ValueError("number of payments per year must be positive")
    if args.fees < 0:
        raise ValueError("fees must be positive")
    return args

if __name__ == "__main__":
    try:
        arguments = parse_args(sys.argv[1:])
    except ValueError as e:
        sys.exit(str(e))
    print(main(arguments.balance_amount, arguments.apr, credit_line = arguments.credit_line, targetamount = arguments.payment, fees = arguments.fees))