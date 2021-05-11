set number

filetype plugin on


" https://github.com/neovim/neovim/wiki/FAQ#cursor-style-isnt-restored-after-exiting-or-suspending-and-resuming-nvim
autocmd VimLeave,VimSuspend * set guicursor=a:ver100-blinkon750
