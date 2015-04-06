# ipython_notebook_emacs

Control an ipython notebook started in a web browser using emacs
================================================================

The ipython notebook emacs module is hard to install, also it does not containt the features which make ipython notebook nice to work with. I found myself working in the ipython notebook to try out concepts and then cutting and pasting back and forth between emacs and a webbrowser.

I decided to create a emacs module which will cut and paste an ipython notebook cell between ipython and emacs or vice versa. I can also add a cell at the end, and insert contents from emacs to ipython notebook in the webbrowser.

It does this by using the epc module to communicate with a webbrowser which has been started using ipython.

Right now the module is unpolished and is something which I personally use. I am posting it so others can learn how to control python programs from emacs.

Requirements
------------

* The epc <https://python-epc.readthedocs.org/en/latest/> module allows python programs to be 
* selenium for python https://selenium-python.readthedocs.org/
* a web browser which works with selenium.

Usage
-----

the epc_broswer.el is the emacs module. The path to file the file should be set by ipyn-path.

* ipyn:start will start a web browser, and will automatically connect to it.
* ipyn-epc:connect is for debugging, if the file is run under ipython console, extra server functions can be added or modified. connect to it with this function
* ipyn:js-ex will execute javascript string in the browser
* ipyn:js-ex-region will execute a selected region in emacs in run in the browser.
* ipyn:insert_cell_bottom will insert a cell at the bottom of the ipython notebook and select it
* ipyn:region_to_selected_cell will insert a selected emacs region into a selected ipython notebook cell
* ipyn:yank_region_from_selected_cell will yank the contents of a selected ipython notebook cell into emacs.
* ipyn:goto-url will switch the browser to a selected url. used to switch the browser to an ipython notebook url


I have mapped some of the functions to keys. On my linux system "s" is the windows key.

