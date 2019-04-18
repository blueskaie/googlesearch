from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.proxy import Proxy, ProxyType
import time

class GoogleKeywordSearch:
    def __init__(self):
        self.sites = []
        self.searchitems = []
        self.result = []
        self.baseurl = "https://www.google.com"
        # self.browser = self.installProxy("5.202.74.124", "80")
        self.browser = webdriver.Chrome()
    def installProxy(self, PROXY_HOST, PROXY_PORT):
        prox = Proxy()
        prox.proxy_type = ProxyType.MANUAL
        proxstr = PROXY_HOST + ":" + PROXY_PORT
        prox.http_proxy = proxstr
        prox.socks_proxy = proxstr
        prox.ssl_proxy = proxstr

        capabilities = webdriver.DesiredCapabilities.CHROME
        prox.add_to_capabilities(capabilities)
        return webdriver.Chrome()

    def getSearchOccurance(self, url, keyword):
        occurance = 0
        try:
            searchPattern = "site:${url} ${keyword}"
            searchText = searchPattern.replace("${url}", url).replace("${keyword}", keyword)
            self.browser.get(self.baseurl)
            self.browser.find_element_by_xpath("//input[@name='q']").send_keys(searchText)
            self.browser.find_element_by_xpath("//input[@name='q']").send_keys(Keys.ENTER)
            time.sleep(3)
            resultstats = self.browser.find_element_by_xpath("//div[@id='resultStats']").text
            occurance = self.getExtractOccurance(resultstats)    
        except NoSuchElementException as ne:
            occurance = 0
            print("0")
        except Exception as e:
            print("ERROR: "+e)
        print(url+" : "+keyword+":"+str(occurance))
        return occurance
    
    def getExtractOccurance(self, resultstats):
        result = 0
        startindex = resultstats.find("About")
        lastindex = resultstats.find("result")
        if (lastindex > 0 and startindex >= 0):
            numstr = resultstats[startindex+5:lastindex]
            numstr = numstr.replace(",", "")
            result = int(numstr)
        elif (lastindex > 0 and startindex < 0):
            numstr = resultstats[0:lastindex]
            numstr = numstr.replace(",", "")
            result = int(numstr)
        else:
            result = 0
        return result

    def close(self):
        self.browser.quit()

def main():
    try:
        s = GoogleKeywordSearch()
        a = s.getExtractOccurance("About 10 result (0.21 seconds) ")
        print(a)
    except Exception as e:
        print(e)
    else:
        print("Success!")

if __name__ == "__main__":
    main()