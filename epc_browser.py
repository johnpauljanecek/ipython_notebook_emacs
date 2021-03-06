#epc_browser.py
from browser import Browser
from epc.server import EPCServer
from epc.server import ThreadingEPCServer
import threading 

global server
server = None
try:
    __IPYTHON__
    server = ThreadingEPCServer(('localhost',0))
except :
    server = EPCServer(('localhost', 0))

class EpcBrowser(Browser):
    def setup(self):
        result = Browser.setup(self,visible=True,driver = "firefox_firebug")
        return result

global browser
browser = EpcBrowser()
browser.setup()

def js_ex(string):
    print "js_ex "
    result = browser.js_ex(string)
    print result
    return result

server.register_function(js_ex)

def string_to_selected_cell(codeStr):
    jsCode = """
    return (function(codeStr) {
    var nb = IPython.notebook;
    var selCell = nb.get_selected_cell();
    selCell.set_text(codeStr);
    })(arguments[0]);
    """
    browser.js_ex(jsCode,codeStr)
server.register_function(string_to_selected_cell)

def goto_notebook(url):
    browser.driver.get(url)
    return True

server.register_function(goto_notebook)

try:
    __IPYTHON__
    server_thread = threading.Thread(target = server.serve_forever)
    server_thread.allow_reuse_address = True 
    server_thread.start()
    server.print_port()
except :
    server.print_port()
    server.serve_forever()



