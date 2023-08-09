
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import datetime

def print_with_timestamp(*args, sep=' ', end='\n'):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    content = sep.join(map(str, args))
    print(f"[{timestamp}] {content}", end=end)
    
def read_email_address():
    file_path = 'email_list.txt'
    try:
        with open(file_path, "r") as file:
            to_emails = file.readlines()
        # print_with_timestamp(f"subscribed people: \n{to_emails}")
        return to_emails;
    except Exception as e:
        print_with_timestamp("Error read recipient list:", str(e))
        return None

def rewrite_numbers_file(new_number):
    file_path = "mail_info.txt"

    try:
        with open(file_path, "w") as file:
            file.write(str(new_number))
        print_with_timestamp(f"File {file_path} rewritten with the number {new_number}")
    except Exception as e:
        print_with_timestamp("Error rewriting file:", str(e))


def send_email(subject, body, to_emails,new_mail_date):
    # Email configuration
    from_email = "notificationcenterunofficial@gmail.com"
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = "notificationcenterunofficial@gmail.com"
    smtp_password = "dfelnmtferfyomew"

    # Create a MIME message
    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = ", ".join(to_emails)
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    # Include HTML content with a link
    html_body = f"""
    <html>
        <body>
            <p>Check it out here - <a href="http://shahandanchor.com/placement/index.php">http://shahandanchor.com/placement/</a></p>
            <p>The mail was received at placement portal on {new_mail_date}</p>
            <p>This email has been generated automatically. Please refrain from replying to this email. </p>
        </body>
    </html>
    """

    msg.attach(MIMEText(html_body, "html"))

    # Connect to the SMTP server and send the email
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(from_email, to_emails, msg.as_string())
        server.quit()
        print_with_timestamp("Emails sent successfully.")
    except Exception as e:
        print_with_timestamp("Error sending email:", str(e))


def read_number_from_file():
    file_path = "mail_info.txt"
    with open(file_path, "r") as file:
        content = file.read()
        try:
            number = int(content.strip())
            return number
        except ValueError:
            print_with_timestamp("Error: The file does not contain a valid number.")
            return None


def main():
    # Create ChromeOptions with headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--single-process")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Create a WebDriver instance with headless mode
    driver = webdriver.Chrome(options=chrome_options)

    url = "http://shahandanchor.com/placement/index.php"
    driver.get(url)
    print_with_timestamp('Logging in...')
    
    # Fill in form fields
    reg_id_field = driver.find_element(By.NAME, "reg_id")
    reg_id_field.send_keys("15675")

    password_field = driver.find_element(By.NAME, "password")
    password_field.send_keys("akhilp")

    # Submit the form
    submit_button = driver.find_element(By.NAME, "login")
    submit_button.click()

    # Wait for AJAX request to complete (i.e a element is updated using AJAX)
    wait = WebDriverWait(driver, 10)
    updated_element = wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    
    print_with_timestamp("Login successfull...")
    print_with_timestamp("Checking for new mail...")

    # Find all element containing all mails
    all_mails = updated_element.find_element(By.TAG_NAME, "tbody")

    # list of all mails
    mail = all_mails.find_elements(By.XPATH, "./*")

    # Latest mail 
    newest_mail = mail[0].find_elements(By.TAG_NAME, "td")
    # Latest mail body
    new_mail_body = newest_mail[0]
    
    # Extracting subject from latest mail
    new_mail_subject = (
        new_mail_body.find_element(By.TAG_NAME, "a").find_element(By.TAG_NAME, "b").text
    )
    # Date latest mail is receeived
    new_mail_date = newest_mail[1].text
    
    # Total number of mails in inbox
    number_of_mails = len(mail)

    body = new_mail_subject + "\n A new mail has arrived in the sakec placement portal."

    #  email receipients list
    to_emails = read_email_address()
    
    number_of_previous_mails = read_number_from_file() 
    number_of_new_mails = number_of_mails- number_of_previous_mails

    if number_of_previous_mails < number_of_mails:
        print_with_timestamp("NEW MAIL DETECTED")
        print_with_timestamp('There are',number_of_new_mails,' new mails')
        rewrite_numbers_file(number_of_mails)
        send_email(new_mail_subject, body, to_emails,new_mail_date)
    else:
        # send_email('testing', 'No new mail from sakec placement portal', to_emails,'NIL')
        print_with_timestamp("NO NEW MAIL")

    # Close the browser
    print_with_timestamp('Closing browser...')
    driver.close()
    driver.quit()
    print_with_timestamp('Browser closed successfully\n\n')

if __name__ == "__main__":
    main()