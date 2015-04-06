;;epc_browser.el

(require 'epc)
(defvar ipyn-browser nil)
(defvar ipyn-buffer "*ipyn--buffer*")
(defvar ipyn-result nil)
 
(defun ipyn-epc:connect (port)
  (interactive "nEnter ipyn-epc port : ")
  (setq ipyn-browser (epc:start-epc-debug port))
  )

(setq ipyn-browser (epc:start-epc "python" '("/home/john/Development/amazon/epc_browser.py")))

;;(plist-get (car ipyn-result) :output_type)
(defun ipyn:js-ex (code-str)
  (when ipyn-browser
    (setq ipyn-result nil)
    (deferred:$
    (epc:call-deferred 
     ipyn-browser 'js_ex
     (list
      code-str))
    (deferred:nextc it 
      (lambda (x) 
        (setq ipyn-result x)
        (message "js-ex successful")
        )))))

(defun ipyn:js-ex-region (start end)
  (interactive "r")
  (ipyn:js-ex (buffer-substring-no-properties start end))
  )

(defun ipyn:insert_cell_bottom ()
  (interactive)
  (let ((js-code 
         "return (function(nb) {
          var cell = nb.insert_cell_at_bottom('code');
          var cellIndex = nb.find_cell_index(cell);
          nb.scroll_to_cell(cellIndex,0.1);
          nb.select(cellIndex);
          nb.edit_mode()
          return true;
          })(IPython.notebook);"))
    (ipyn:js-ex js-code)
    ))

(defun ipyn:region_to_selected_cell (start end)
  (interactive "r")
  (when ipyn-browser
    (let ((sel-region (buffer-substring-no-properties start end)))
      (setq ipyn-result nil)
      (deferred:$
        (epc:call-deferred 
         ipyn-browser 'string_to_selected_cell
         (list sel-region))
        (deferred:nextc it 
          (lambda (x) 
            (setq ipyn-result x)
            (message "selection pasted to cell")
            ))))))

(defun ipyn:yank_region_from_selected_cell ()
  (interactive)
  (when ipyn-browser
    (setq ipyn-result nil)
    (let ((js-code "return (function(nb) {
          var selCell = nb.get_selected_cell();
          return selCell.get_text();
          })(IPython.notebook);
          "))
      (deferred:$
        (epc:call-deferred 
         ipyn-browser 'js_ex 
         (list 
          js-code))
         (deferred:nextc it 
          (lambda (x) 
            (setq ipyn-result x)
            (insert x)
            (message "cell yanked")
            ))))))

(defun ipyn:goto-url (url)
  ;;take ipython to the main page
  (interactive "sEnter url: ")
  (when ipyn-browser
    (setq ipyn-result nil)
    (deferred:$
      (epc:call-deferred 
       ipyn-browser 'goto_notebook 
       (list url))
      (deferred:nextc it 
        (lambda (x) 
          (message "main notebook loaded")
          )))))

(global-set-key (kbd "s-i x") 'ipyn:js-ex-region)
(global-set-key (kbd "s-i p") 'ipyn:region_to_selected_cell)
(global-set-key (kbd "s-i y") 'ipyn:yank_region_from_selected_cell)
(global-set-key (kbd "s-i i") 'ipyn:insert_cell_bottom)
       
