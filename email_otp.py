from email.message import EmailMessage
import ssl
import smtplib

def send_otp(to, otp):
    try:
        # Initialising Email Object
        emailObj = EmailMessage()
        emailObj["From"] = "aadityajain010203@gmail.com"
        emailObj["To"] = to
        emailObj["Subject"] = "OTP Verification for HackerCode"
        emailObj.set_content(f"Here is your OTP for HackerCode\n\t{otp}")

        # SSL Certificate
        context = ssl.create_default_context()

        # Sending Email using smtplib
        # Port 465: This port was previously used for Secure SMTP (SMTPS). It has now been deprecated by the Internet Engineering Task Force (IETF)
        with smtplib.SMTP_SSL("smtp.gmail.com", port=465, context=context) as smtp:
            smtp.login("aadityajain010203@gmail.com", "ustnrjbkusdszvds")
            smtp.sendmail("aadityajain010203@gmail.com", to, emailObj.as_string())

        return True
    
    except:
        return False
    

if __name__ == "__main__":
    print(send_otp("aadityajain0128@gmail.com", 3412))