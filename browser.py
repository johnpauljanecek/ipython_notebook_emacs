from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyvirtualdisplay import Display
from urllib2 import urlopen
from bs4 import BeautifulSoup
import os.path
import os
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import datetime

firefox_path = None

if os.environ["USER"] == "john" :
    firefox_path = "/usr/lib/firefox/firefox"
elif os.environ["USER"] == "ubuntu" :
    firefox_path = '/home/ubuntu/firefox/firefox/firefox-bin'
else :
    raise Exception("unknown user")

class Browser(object):
    def __init__(self):
        self.display = None
        self.driver = None
        self.start = datetime.datetime.now().strftime("%b-%d-%Y-%H:%M:%S")

    def get_id(self):
        return self.start
        
    def get_driver(self):
        return self.driver

        
    def get_ip(self,browser = False):
        u = urlopen("https://hide.me/en/check")
        soup = BeautifulSoup(u.read())
        div = soup.find("div",class_ = "col col3 check")
        ip = div.select("li strong")[0].text
        location = div.select("li strong")[1].text
        return (ip,location)
    
    def driver_chrome(self):
        self.driver = Chrome(executable_path='/usr/lib/chromium-browser/chromedriver')
        #ebdriver.Chrome(executable_path='/usr/lib/chromium-browser/chromedriver')
        self.driver.implicitly_wait(2)
        return "chrome"

    def driver_chrome_mobile(self):
        mobile_emulation = { "deviceName": "Google Nexus 5" }
        options = webdriver.ChromeOptions()
        options.add_experimental_option("mobileEmulation", mobile_emulation)
        self.driver = webdriver.Chrome(
            executable_path =
            #'/home/john/Development/chromedriver'
            os.path.join(os.path.abspath("."),'bin/chromedriver')
            ,
            chrome_options = options)
        self.driver.implicitly_wait(2)
        return "chrome_mobile"

    def driver_firefox(self):
        binary = FirefoxBinary(firefox_path)
        self.driver = Firefox(firefox_binary=binary)
        #self.driver = webdriver.Firefox(firefox_binary=binary)
        self.driver.implicitly_wait(10)
        return "firefox"

    def driver_firefox_firebug(self):
        profile = webdriver.FirefoxProfile()
        profile.set_preference("extensions.firebug.currentVersion","2.0.8")
        ext_dir = "./firefox_extensions/"
        extensions = [
            ("firebug","firebug@software.joehewitt.com.xpi"),
            ]
        for name,ext_path in extensions:
            profile.add_extension(os.path.join(ext_dir,ext_path))
        self.driver = Firefox(firefox_profile = profile)
        self.driver.implicitly_wait(10)
        return "firefox_firebug"

    def driver_firefox_mobile_dev(self):
        #about:config look here to see preferences
        profile = webdriver.FirefoxProfile()
        ext_dir = "./firefox_extensions/"
        extensions = [
            ("selenium","{a6fd85ed-e919-4a43-a5af-8da18bda539f}.xpi"),
            ("py-sel","pythonformatters@seleniumhq.org.xpi"),
            ("firebug","firebug@software.joehewitt.com.xpi"),
            ("firepath","FireXPath@pierre.tholence.com.xpi")]
        profile.set_preference("general.useragent.override", "Mozilla/5.0 (Android; Mobile; rv:26.0) Gecko/26.0 Firefox/26.0")
        for name,ext_path in extensions:
            profile.add_extension(os.path.join(ext_dir,ext_path))
        self.driver = webdriver.Firefox(firefox_profile = profile)
        self.driver.implicitly_wait(10)
        return "firefox_mobile_dev"

    def driver_firefox_mobile(self):
        """
        to do
        should modify all the adders as shown here
        http://automationttestingagiledevelopment.blogspot.com/2012/01/mobile-testing-automation-with-selenium.html
        """
        profile = webdriver.FirefoxProfile(firefox_path)
        profile.set_preference("general.useragent.override", "Mozilla/5.0 (Android; Mobile; rv:26.0) Gecko/26.0 Firefox/26.0")
        self.driver = webdriver.Firefox(firefox_profile = profile)
        self.driver.implicitly_wait(10)
        return "firefox_mobile"

    def driver_custom_firefox(self):
        from shutil import copytree,rmtree
        profile_path = "/home/john/Development/amazon/browser_profiles/firefox/selenium"
        dest_path = "/home/john/tmp/selenium"
        rmtree(dest_path)
        copytree(profile_path,dest_path,symlinks = True)
        profile_path = "/home/john/tmp/selenium"
        
        binary = FirefoxBinary(firefox_path)
        profile = webdriver.FirefoxProfile(profile_path)

        profile.set_preference("extensions.firebug.currentVersion","2.0.8")
        #load firebug
        ext_dir = "./firefox_extensions/"
        extensions = [
            ("firebug","firebug@software.joehewitt.com.xpi"),
            ]
        for name,ext_path in extensions:
            profile.add_extension(os.path.join(ext_dir,ext_path))
        
        self.driver = Firefox(firefox_profile=profile,
                              firefox_binary=binary)
        return "custom_firefox"
        
    def setup(self,visible = False,driver = "chrome",opt = None):
        if not visible :
            self.display = Display(backend="xvfb")
            self.display.start()
        
        try:
            return getattr(self,"driver_%s" % (driver,))()
        except AttributeError:
            self.teardown()
            return False

    def teardown(self):
        if self.driver :
            self.driver.quit()
            self.driver = None

        if self.display :
            self.display.stop()
            self.display = None
        return True

    def js_ex(self,script,*args):
        return self.driver.execute_script(script,*args)

    def js_ex_file(self,fileName):
        with file(fileName,"r") as f :
            script = f.read()
            return self.driver.execute_script(script)

    def get_attributes(self,element):
        """gets all of the attributes of a selenium web element"""
        return self.driver.execute_script("""
        var items = {}; 
        for (index = 0; index < arguments[0].attributes.length; ++index) 
        { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;""",
                                          element)

    def get_element_image(self,element):
        """takes screenshot of an element returns it as a PIL image
        on IPython notebook the PIL image will be automatically displayed"""
        from PIL import Image
        from StringIO import StringIO
        location = element.location
        size = element.size
        img = Image.open(StringIO(self.driver.get_screenshot_as_png()))
        left = int(location['x'])
        top = int(location['y'])
        right = int(location['x'] + size['width'])
        bottom = int(location['y'] + size['height'])
        img = img.crop((left, top, right, bottom))
        return img

            

