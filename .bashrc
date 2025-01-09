# if not running interactively, don't do anything
[[ $- != *i* ]] && return

shopt -s globstar histappend

alias vim='nvim'
alias ls='ls --color=auto'
alias ssh='TERM=xterm-256color ssh'

alias compose='docker compose'
alias goat='go-ascii-tool'
alias mc='mcli'

alias dotfiles='/usr/bin/git --git-dir=$HOME/.dotfiles --work-tree=$HOME'

httpd() {
  python -m http.server "${1:-8001}"
}

eval "$(starship init bash)"
eval "$(direnv hook bash)"
