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

if __name__ == "__main__":
    amount = float(input("Enter the payment amount in rupees: "))
    # upi_id = input("Enter the UPI ID: ")
    upi_id = "8250129352@apl"

    qr_code_path = generate_upi_qr_code(amount, upi_id)
    print("QR code generated successfully. You can find it at:", qr_code_path)

    # Open the generated QR code image
    os.startfile(qr_code_path)

    # # Open the generated QR code image
    # webbrowser.open(qr_code_path)