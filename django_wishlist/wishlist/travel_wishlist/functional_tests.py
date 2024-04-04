from django.test import LiveServerTestCase   # Importing necessary modules from Django for testing
from selenium import webdriver   # Importing Selenium for browser automation
from selenium.webdriver.common.by import By  # Importing necessary Selenium modules
from selenium.webdriver.support.ui import WebDriverWait  # Importing necessary Selenium modules
from selenium.webdriver.support import expected_conditions as EC  # Importing necessary Selenium modules


class TitleTest(LiveServerTestCase):
    fixtures = ['test_users']  # Defining fixtures to load test data

    def setUp(self):
        self.browser = webdriver.Firefox()  # Setting up Firefox browser for testing
        self.browser.implicitly_wait(3)  # Setting implicit wait for 3 seconds

        self.browser.get(self.live_server_url + '/admin')  # Opening the admin page of the live server
        self.browser.find_element_by_id('id_username').send_keys('alice')  # Entering username 'alice'
        self.browser.find_element_by_id('id_password').send_keys('qwertyuiop')  # Entering password 'qwertyuiop'
        self.browser.find_element_by_css_selector('input[type="submit"]').click()  # Clicking the submit button

    def tearDown(self):
        self.browser.quit()  # Closing the browser after each test

    def test_title_shown_on_home_page(self):
        self.browser.get(self.live_server_url)  # Opening the home page of the live server
        self.assertIn('Travel Wishlist', self.browser.title)  # Checking if 'Travel Wishlist' is present in the title


class AddEditPlacesTests(LiveServerTestCase):
    fixtures = ['test_users', 'test_places']  # Defining fixtures to load test data

    def setUp(self):
        self.browser = webdriver.Firefox()                        # Setting up Firefox browser for testing
        self.browser.implicitly_wait(3)                           # Setting implicit wait for 3 seconds

        self.browser.get(self.live_server_url + '/admin')         # Opening the admin page of the live server
        self.browser.find_element_by_id('id_username').send_keys('alice')  # Entering username 'alice'
        self.browser.find_element_by_id('id_password').send_keys('qwertyuiop')  # Entering password 'qwertyuiop'
        self.browser.find_element_by_css_selector('input[type="submit"]').click()  # Clicking the submit button

    def tearDown(self):
        self.browser.quit()                                      # Closing the browser after each test

    def test_add_new_place(self):
        self.browser.get(self.live_server_url)                   # Opening the home page of the live server
        input_name = self.browser.find_element_by_id('id_name')  # Finding the input field for place name
        input_name.send_keys('Denver')                           # Entering 'Denver' in the place name input field
        add_button = self.browser.find_element_by_css_selector('input[type="submit"]')  # Finding the add button
        add_button.click()                                       # Clicking the add button

        self.assertIn('Denver', self.browser.page_source)  # Checking if 'Denver' is present in the page source

    def test_mark_place_as_visited(self):
        self.browser.get(self.live_server_url)  # Opening the home page of the live server

        visited_button = self.browser.find_element_by_id('visited-button-2')  # Finding the visited button for New York
        visited_button.click()  # Clicking the visited button for New York

        wait = WebDriverWait(self.browser, 3)  # Setting up explicit wait for 3 seconds
        wait.until(EC.invisibility_of_element_located((By.ID, 'place-name-2')))  # Waiting for New York to disappear
        # Checking if 'New York' is not present in the page source
        self.assertNotIn('New York', self.browser.page_source)

        self.browser.get(self.live_server_url + '/visited')  # Opening the visited page
        self.assertIn('New York', self.browser.page_source)  # Checking if 'New York' is present in the visited page


class PageContentTests(LiveServerTestCase):
    fixtures = ['test_users', 'test_places']  # Defining fixtures to load test data

    def setUp(self):
        self.browser = webdriver.Firefox()  # Setting up Firefox browser for testing
        self.browser.implicitly_wait(3)  # Setting implicit wait for 3 seconds

        self.browser.get(self.live_server_url + '/admin')  # Opening the admin page of the live server
        self.browser.find_element_by_id('id_username').send_keys('alice')  # Entering username 'alice'
        self.browser.find_element_by_id('id_password').send_keys('qwertyuiop')  # Entering password 'qwertyuiop'
        self.browser.find_element_by_css_selector('input[type="submit"]').click()  # Clicking the submit button

    def tearDown(self):
        self.browser.quit() # Closing the browser after each test

    def test_get_home_page_list_of_places(self):
        self.browser.get(self.live_server_url)  # Opening the home page of the live server
        # Checking if 'San Francisco' is present in the page source
        self.assertIn('San Francisco', self.browser.page_source)
        self.assertIn('New York', self.browser.page_source)  # Checking if 'New York' is present in the page source
        self.assertNotIn('Tokyo', self.browser.page_source)  # Checking if 'Tokyo' is not present in the page source
        self.assertNotIn('Moab', self.browser.page_source)  # Checking if 'Moab' is not present in the page source

    def test_get_list_of_visited_places(self):
        # Opening the visited page of the live server
        self.browser.get(self.live_server_url + '/visited')

        self.assertIn('Tokyo', self.browser.page_source)  # Checking if 'Tokyo' is present in the visited page
        self.assertIn('Moab', self.browser.page_source)  # Checking if 'Moab' is present in the visited page
        # Checking if 'San Francisco' is not present in the visited page
        self.assertNotIn('San Francisco', self.browser.page_source)
        # Checking if 'New York' is not present in the visited page
        self.assertNotIn('New York', self.browser.page_source)
