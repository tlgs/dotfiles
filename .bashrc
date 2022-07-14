# shellcheck shell=bash

# if not running interactively, don't do anything
[[ $- != *i* ]] && return

alias vim='nvim'
alias ls='ls --color=auto'
alias ssh='TERM=xterm-256color ssh'

alias ranger='ranger --choosedir=$HOME/.ranger; cd "$(cat $HOME/.ranger)"; rm $HOME/.ranger'
alias dotfiles='/usr/bin/git --git-dir=$HOME/.dotfiles --work-tree=$HOME'


httpd() {
  python -m http.server "${1:-8001}"
}

ytdl-playlist() {
  youtube-dl --get-id "$1" \
    | xargs -I '{}' -P ${2:-5} youtube-dl -x --audio-format m4a --add-metadata 'https://youtube.com/watch?v={}'
}

clippy-tts() {
  xclip -o -selection clipboard | festival --tts
}

eval "$(starship init bash)"
eval "$(direnv hook bash)"
