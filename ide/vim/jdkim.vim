
" 1) Add next line to _vimrc in vim installation directory in windows.
"     source $VIMRUNTIME/../jdkim.vim
" 2) Install vundle (https://github.com/gmarik/Vundle.vim/wiki/Vundle-for-Windows)
"     cd %USERPROFILE%
"     git clone https://github.com/gmarik/vundle.git vimfiles/bundle/vundle
" 3) Run vim and type :BundleInstall (automatically all bundle will be installed.)


set rtp+=~/vimfiles/bundle/vundle/
call vundle#rc()

" let Vundle manage Vundle
" required!
Bundle 'gmarik/vundle'

" The bundles you install will be listed here
Bundle 'Lokaltog/powerline', {'rtp': 'powerline/bindings/vim/'}
Bundle 'tpope/vim-fugitive'
Bundle 'scrooloose/nerdtree'
Bundle 'klen/python-mode'
Bundle 'davidhalter/jedi-vim'
Bundle 'rainux/vim-desert-warm-256'

set paste
set nobackup
set hlsearch incsearch
set ruler nowrap nu showcmd sm wmnu
set report=0 ls=2 bs=2 sel=inclusive
set magic sol
set ignorecase smartcase
set ts=4 tw=200 sw=4 sts=4 nuw=5 wrap
set ai ci nosi
set laststatus=2

syntax on

colorschem desert-warm-256

nmap <F5> :!python %<CR>
nmap <F6> :!python % > dump.txt<CR>
map <F2> :NERDTreeToggle<CR>

let g:NERDTreeWinPos = "left"

set guifont=³ª´®°íµñÄÚµù:h10
