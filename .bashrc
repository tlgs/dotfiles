# if not running interactively, don't do anything
[[ $- != *i* ]] && return

alias vim='nvim'
alias ls='ls --color=auto'
alias tree='tree --gitignore -I .git'
alias ssh='TERM=xterm-256color ssh'

alias goat='go-ascii-tool'
alias compose='docker compose'

alias dotfiles='/usr/bin/git --git-dir=$HOME/.dotfiles --work-tree=$HOME'

httpd() {
  python -m http.server "${1:-8001}"
}

clippy-tts() {
  xclip -o -selection clipboard | festival --tts
}

eval "$(starship init bash)"
eval "$(direnv hook bash)"
