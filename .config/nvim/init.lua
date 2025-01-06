-- kickstart.nvim set options:
vim.o.hlsearch = false                  -- set highlight on search
vim.wo.number = true                    -- make line numbers default
vim.o.mouse = 'a'                       -- enable mouse mode
vim.o.clipboard = 'unnamedplus'         -- sync clipboard between OS and Neovim
vim.o.breakindent = true                -- wrapped lines continue visually indented
vim.o.undofile = true                   -- save undo history
vim.o.ignorecase = true                 -- case-insensitive searching
vim.o.smartcase = true
vim.o.updatetime = 250                  -- decrease update time
vim.o.timeoutlen = 300
vim.o.completeopt = 'menuone,noselect'  -- better completion experience
vim.o.termguicolors = true              -- enable 24-bit RG

vim.cmd 'colorscheme vim'
