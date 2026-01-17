import smtplib
from email.message import EmailMessage
from config import SENDER_EMAIL, RECEIVER_EMAIL, EMAIL_PASSWORD


def send_email_alert(stock_symbol, price, target_price):
    msg = EmailMessage()
    msg.set_content(
        f"Stock Price Alert!\n\n"
        f"Stock: {stock_symbol}\n"
        f"Current Price: ${price}\n"
        f"Target Price: ${target_price}\n\n"
        f"Action: Target Reached!"
    )
    msg['Subject'] = f"Stock Alert: {stock_symbol}"
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(SENDER_EMAIL, EMAIL_PASSWORD)
    server.send_message(msg)
    server.quit()

    print("Email alert sent successfully!")