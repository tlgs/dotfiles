# shellcheck shell=bash

# if not running interactively, don't do anything
[[ $- != *i* ]] && return

alias ls='ls --color=auto'
alias config='/usr/bin/git --git-dir=$HOME/.dotfiles --work-tree=$HOME'
alias vim='nvim'

# media
alias ytdl='youtube-dl -x --audio-format m4a --add-metadata'


httpd() {
  python -m http.server "${1:-8001}"
}


eval "$(starship init bash)"
eval "$(direnv hook bash)"
