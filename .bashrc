# shellcheck shell=bash

# if not running interactively, don't do anything
[[ $- != *i* ]] && return

alias vim='nvim'
alias ls='ls --color=auto'
alias ssh='TERM=xterm-256color ssh'

alias ranger='ranger --choosedir=$HOME/.ranger; cd "$(cat $HOME/.ranger)"; rm $HOME/.ranger'
alias dotfiles='/usr/bin/git --git-dir=$HOME/.dotfiles --work-tree=$HOME'
alias ytdl='youtube-dl -x --audio-format m4a --add-metadata'


httpd() {
  python -m http.server "${1:-8001}"
}


eval "$(starship init bash)"
eval "$(direnv hook bash)"
