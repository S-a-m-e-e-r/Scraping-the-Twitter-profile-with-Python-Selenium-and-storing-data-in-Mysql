# Import necessary packages
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from lxml import html
import csv
import mysql.connector

# Create a connection to MySQL
conn=mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="twitterprofiles"
)

# Create a cursor
cursor = conn.cursor()



# Create a Firefox WebDriver
driver = webdriver.Firefox()

def login():
    # Replace these with your Twitter credentials
    username = "mohammed_5ameer"
    password = "MDsami786"

    # Open Twitter login page
    driver.get("https://twitter.com/login")

    # Wait for the page to load
    driver.implicitly_wait(5)

    # Find the username input field using XPath
    username_field = driver.find_element(By.XPATH, '//input[@class="r-30o5oe r-1dz5y72 r-13qz1uu r-1niwhzg r-17gur6a r-1yadl64 r-deolkf r-homxoj r-poiln3 r-7cikom r-1ny4l3l r-t60dpp r-fdjqy7"]')

    # Enter your Twitter username
    username_field.send_keys(username)

    # Find the "Next" button and click it
    next_button = driver.find_element(By.XPATH, '//div[@class="css-175oi2r r-sdzlij r-1phboty r-rs99b7 r-lrvibr r-ywje51 r-usiww2 r-13qz1uu r-2yi16 r-1qi8awa r-ymttw5 r-1loqt21 r-o7ynqc r-6416eg r-1ny4l3l"][1]')
    next_button.click()

    # Find the password input field using XPath
    password_field = driver.find_element(By.XPATH, '//input[@class="r-30o5oe r-1dz5y72 r-13qz1uu r-1niwhzg r-17gur6a r-1yadl64 r-deolkf r-homxoj r-poiln3 r-7cikom r-1ny4l3l r-t60dpp r-fdjqy7"]')

    # Enter your Twitter password
    password_field.send_keys(password)

    # Wait for the login button using XPath
    driver.implicitly_wait(10)
    login_button = driver.find_element(By.XPATH, '//div[@data-testid="LoginForm_Login_Button"]')

    # Click the login button
    login_button.click()

    # Wait for the login to complete
    sleep(5)  # Adjust waiting time as needed

# Call the login function to log in
login()

# Wait for 5 seconds after login
sleep(5)

# List to store links that failed to extract data
links = []

def extract(driver, val):
    # Open the Twitter profile in the browser
    driver.get(val)

    # Wait for 6 seconds
    sleep(6)

    # Parse the HTML tree of the page
    tree = html.fromstring(driver.page_source)

    try:
        # Extract information from the page using XPath
        bio = tree.xpath('//div[@data-testid="UserDescription"]//span[@class="css-1qaijid r-bcqeeo r-qvutc0 r-poiln3"]/text()')
        if bio:
            bio = bio[0]
        else:
            bio="N/A"
        print(bio)

        loc = tree.xpath('//span[@data-testid="UserLocation"]//span//span[@class="css-1qaijid r-bcqeeo r-qvutc0 r-poiln3"]/text()')
        if loc:
            loc = loc[0]
        else:
            loc="N/A"
        print(loc)

        web = tree.xpath('//a[@data-testid="UserUrl"]//span[@class="css-1qaijid r-bcqeeo r-qvutc0 r-poiln3"]/text()')
        if web:
            web = web[0]
        else:
            web="N/A"
        print(web)

        following = tree.xpath('//div[@class="css-175oi2r r-1mf7evn"]//a//span[@class="css-1qaijid r-bcqeeo r-qvutc0 r-poiln3 r-1b43r93 r-1cwl3u0 r-b88u0q"]//span/text()')
        if following:
            following = following[0]
        else:
            following='0'
        print(following)

        follower = tree.xpath('//div[@class="css-175oi2r r-13awgt0 r-18u37iz r-1w6e6rj"]//div[@class="css-175oi2r"]//a//span[@class="css-1qaijid r-bcqeeo r-qvutc0 r-poiln3 r-1b43r93 r-1cwl3u0 r-b88u0q"]//span/text()')
        if follower:
            follower = follower[0]
        else:
            follower='0'
        print(follower)

        return bio, following, follower, loc, web

    except Exception as e:
        if val not in links:
            links.append(val)
        print(f"Failed to extract data for {val}: {e}")
        return 'N/A', '0', '0', 'N/A', 'N/A'


def convert_to_int(value):
    value = value.replace(',', '')  # Remove commas if present
    if 'm' in value.lower():
        return int(float(value[:-1]) * 1e6)  # Convert million to integer
    elif 'k' in value.lower():
        return int(float(value[:-1]) * 1e3)  # Convert thousand to integer
    else:
        return int(value)  # Convert regular integer to integer


def output_to_mysql():
    # Open input CSV file
    with open('twitter_links.csv', newline='') as inputfile:
        # Create a CSV reader
        spamreader = csv.reader(inputfile, delimiter=' ', quotechar='|')

        # Iterate through each row in the input CSV
        for row in spamreader:
            # Convert row to a single string and remove quotes
            val = ', '.join(row).replace('"', "")

            # Wait for 2 seconds
            sleep(2)

            # Extract information with the driver instance returned by login
            bio, following, follower, loc, web = extract(driver, val)

            # Convert lists to strings'
            following_int = convert_to_int(following)
            followers_int = convert_to_int(follower)
           

            # Insert data into MySQL database
            insert_query = """
                INSERT INTO twitter_profiles (Bio, Following_Count, Followers_Count, Location, Website)
                VALUES (%s, %s, %s, %s, %s)
            """
            data = (bio, following_int, followers_int, loc, web)
            cursor.execute(insert_query, data)

            # Commit the changes to the database
            conn.commit()

        #print(links)

    # Print a message when the data is inserted into the MySQL database
    print("Data inserted into MySQL database")

# Call the output_to_mysql function
output_to_mysql()

# Close the cursor and connection to MySQL
cursor.close()
conn.close()

# Close the webdriver
driver.close()
