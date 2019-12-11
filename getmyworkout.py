import bs4
import requests
import smtplib
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from contextlib import redirect_stdout

# CHANGE if needed
from_address = "from_test@test.com"
to_address = "to_test@test.com"
local_path = "file:///Users/your/local/path/here"
actual_path = "/Users/local/path/here"

# Should not need to change
url = "https://www.thequadguy.com/dailypump"
filename = "workout"
delimiter = "_"
now = str(datetime.today().strftime("%m-%d-%Y"))
extension = ".html"

log_file = now + ".txt"

with open(log_file, 'w') as f:
    try:
        s = requests.Session()

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            'Referer': 'https://www.sentrylogin.com/sentry/scripts/CSS_flat_Kady.css',
            'Origin': 'https://www.thequadguy.com',
        }

        params = (
            ('Sentry_ID', '1234'),
            ('e', 'test@test.com'),
            ('p', 'test'),
            ('psist', '0'),
            ('ip', '127.0.0.1'),
            ('ms', '1234'),
        )

        url = "https://www.thequadguy.com/dailypump"

        s.post('https://www.sentrylogin.com/sentry/NoSockets/loginActionAJAX.asp',
               headers=headers, params=params)

        get_page = s.get(url)
        get_page.raise_for_status()  # if error it will stop the program
        print("Checked: {0}".format(url), file=f)

        # Parse text
        get_html = bs4.BeautifulSoup(get_page.text, 'html.parser')
        get_class = bs4.BeautifulSoup.find(get_html, id="block-yui_3_17_2_1_1554898039337_10815")
        get_header = bs4.BeautifulSoup.find(get_class, "h1").text.strip()

        print("Workout: {0}".format(get_header), file=f)
        get_header = get_header.replace("/", "-")

        # Initialize file names
        file_extension = filename + delimiter + now + delimiter + get_header + extension
        file_noextension = filename + delimiter + now + delimiter + get_header
        workout_extension = file_noextension + ".png"
        attach = [actual_path + workout_extension, actual_path + log_file]

        # Create html file if it doesn't exist for the day
        try:
            init_file = open(file_extension, "r")
            init_file.close()
        except IOError:
            init_file = open(file_extension, "a+")
            init_file.close()

        # Write data obtained from html id
        file = open(file_extension, "w")
        file.write(str(get_class))
        file.close()

        # Initialize first Chrome browser to get window size info
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get(local_path + file_extension)
        height = driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, "
                                       "document.documentElement.clientHeight, "
                                       "document.documentElement.scrollHeight, "
                                       "document.documentElement.offsetHeight )")
        driver.quit()
        print("\nGot window height: {0}".format(height), file=f)

        # Initialize second Chrome browser to take screenshot
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument(f"--window-size=900,{height}")
        chrome_options.add_argument("--hide-scrollbars")
        driver = webdriver.Chrome(options=chrome_options)

        driver.get(local_path + file_extension)
        driver.save_screenshot(file_noextension + ".png")
        driver.quit()
        print("Got screenshot: {0}".format(file_noextension + ".png"), file=f)
        print("Sent email to: {0}".format(to_address), file=f)
    except Exception as e:
        print("Error:", e, file=f)

 def send_email():
     s = smtplib.SMTP('smtp.gmail.com', 587)
     s.starttls()
     s.login(from_address, "gmail_password_here")
     # s.set_debuglevel(1)
     msg = MIMEMultipart()
     sender = from_address
     msg['Subject'] = "Workout - {0} - {1}".format(now, get_header)
     msg['To'] = to_address
     for each_file_path in attach:
         try:
             file_name = each_file_path.split("/")[-1]
             part = MIMEBase('application', "octet-stream")
             part.set_payload(open(each_file_path, "rb").read())

             encoders.encode_base64(part)
             part.add_header('Content-Disposition', 'attachment', filename=file_name)
             msg.attach(part)
         except Exception as file_exception:
             print("Could not attach file:", file_exception)
     msg.attach(MIMEText("", 'html'))
     s.sendmail(sender, to_address, msg.as_string())
     s.quit()


 send_email()
