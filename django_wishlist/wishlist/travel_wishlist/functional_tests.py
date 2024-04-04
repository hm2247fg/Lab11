from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TitleTest(LiveServerTestCase):
    fixtures = ['test_users']

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

        self.browser.get(self.live_server_url + '/admin')
        self.browser.find_element_by_id('id_username').send_keys('alice')
        self.browser.find_element_by_id('id_password').send_keys('qwertyuiop')
        self.browser.find_element_by_css_selector('input[type="submit"]').click()

    def tearDown(self):
        self.browser.quit()

    def test_title_shown_on_home_page(self):
        self.browser.get(self.live_server_url)
        self.assertIn('Travel Wishlist', self.browser.title)


class AddEditPlacesTests(LiveServerTestCase):
    fixtures = ['test_users', 'test_places']

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

        self.browser.get(self.live_server_url + '/admin')
        self.browser.find_element_by_id('id_username').send_keys('alice')
        self.browser.find_element_by_id('id_password').send_keys('qwertyuiop')
        self.browser.find_element_by_css_selector('input[type="submit"]').click()

    def tearDown(self):
        self.browser.quit()

    def test_add_new_place(self):
        self.browser.get(self.live_server_url)
        input_name = self.browser.find_element_by_id('id_name')
        input_name.send_keys('Denver')
        add_button = self.browser.find_element_by_css_selector('input[type="submit"]')
        add_button.click()

        self.assertIn('Denver', self.browser.page_source)

    def test_mark_place_as_visited(self):
        self.browser.get(self.live_server_url)

        visited_button = self.browser.find_element_by_id('visited-button-2')
        visited_button.click()

        wait = WebDriverWait(self.browser, 3)
        wait.until(EC.invisibility_of_element_located((By.ID, 'place-name-2')))

        self.assertNotIn('New York', self.browser.page_source)

        self.browser.get(self.live_server_url + '/visited')

        self.assertIn('New York', self.browser.page_source)


class PageContentTests(LiveServerTestCase):
    fixtures = ['test_users', 'test_places']

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

        self.browser.get(self.live_server_url + '/admin')
        self.browser.find_element_by_id('id_username').send_keys('alice')
        self.browser.find_element_by_id('id_password').send_keys('qwertyuiop')
        self.browser.find_element_by_css_selector('input[type="submit"]').click()

    def tearDown(self):
        self.browser.quit()

    def test_get_home_page_list_of_places(self):
        self.browser.get(self.live_server_url)

        self.assertIn('San Francisco', self.browser.page_source)
        self.assertIn('New York', self.browser.page_source)

        self.assertNotIn('Tokyo', self.browser.page_source)
        self.assertNotIn('Moab', self.browser.page_source)

    def test_get_list_of_visited_places(self):
        self.browser.get(self.live_server_url + '/visited')

        self.assertIn('Tokyo', self.browser.page_source)
        self.assertIn('Moab', self.browser.page_source)

        self.assertNotIn('San Francisco', self.browser.page_source)
        self.assertNotIn('New York', self.browser.page_source)
