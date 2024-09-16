import qrcode
import pyqrcode
import os
import csv
from datetime import datetime

def generate_upi_qr_code(amount, upi_id):
    """
    Generates a UPI QR code with the specified amount and UPI ID.

    Args:
        amount (float): The payment amount in rupees.
        upi_id (str): The UPI ID of the recipient.

    Returns:
        str: The QR code image file path.
    """

    # Construct the UPI payment URL
    upi_payment_url = f"upi://pay?pa={upi_id}&pn=Payment&am={amount}&cu=INR"

    # Create a QR code object
    # qr_code = pyqrcode.QRCode(upi_payment_url, error_correctors=pyqrcode.constants.ERROR_CORRECT_L)
    qr_code = pyqrcode.QRCode(upi_payment_url, error='L')

    # Generate the QR code image
    qr_code.png("upi_payment_qr.png", scale=6)

    return "upi_payment_qr.png"


def store_transaction(amount, upi_id):
    """
    Stores the transaction details in a CSV file.

    Args:
        amount (float): The payment amount in rupees.
        upi_id (str): The UPI ID of the recipient.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = "transaction_history.csv"
    file_exists = os.path.isfile(filename)
    
    with open(filename, 'a', newline='') as csvfile:
        fieldnames = ['Timestamp', 'Amount', 'UPI ID']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()
        
        writer.writerow({'Timestamp': timestamp, 'Amount': amount, 'UPI ID': upi_id})


if __name__ == "__main__":
    amount = float(input("Enter the payment amount in rupees: "))
    upi_id = input("Enter the UPI ID: ")

    qr_code_path = generate_upi_qr_code(amount, upi_id)
    print("QR code generated successfully. You can find it at:", qr_code_path)

    # Open the generated QR code image
    os.startfile(qr_code_path)

    # # Open the generated QR code image
    # webbrowser.open(qr_code_path)

    # Simulate successful payment (in a real scenario, you'd verify the payment first)
    input("Press Enter after successful payment...")
    
    # Store transaction details
    store_transaction(amount, upi_id)
    print("Transaction details stored successfully.")
