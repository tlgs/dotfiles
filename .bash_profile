# shellcheck shell=bash

export EDITOR=vim
export TERM=alacritty
export BROWSER=firefox

# clean up
export LESSHISTFILE=/dev/null
export PYLINTHOME=~/.cache/pylint.d

# expand PATH
PATH=$PATH:$HOME/bin
PATH=$PATH:$HOME/.local/bin
PATH=$PATH:$HOME/Applications

# source bashrc
[[ -f ~/.bashrc ]] && . ~/.bashrc

if [ -z "${DISPLAY}" ] && [ "${XDG_VTNR}" -eq 1 ]; then
  exec startx
fi
