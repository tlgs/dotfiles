# shellcheck shell=bash

# if not running interactively, don't do anything
[[ $- != *i* ]] && return

alias vim='nvim'
alias ls='ls --color=auto'
alias ssh='TERM=xterm-256color ssh'

alias goat='go-ascii-tool'

alias dotfiles='/usr/bin/git --git-dir=$HOME/.dotfiles --work-tree=$HOME'

httpd() {
  python -m http.server "${1:-8001}"
}

ytdl-playlist() {
  options=(--no-progress -x --audio-format flac --add-metadata --)
  youtube-dl --get-id "$1" | xargs -n 1 -P "${2:-5}" youtube-dl "${options[@]}"
}

clippy-tts() {
  xclip -o -selection clipboard | festival --tts
}

eval "$(starship init bash)"
eval "$(direnv hook bash)"
