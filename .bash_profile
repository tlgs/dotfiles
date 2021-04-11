# shellcheck shell=bash

export EDITOR=vim
export TERM=alacritty
export BROWSER=firefox

# clean up (cache)
export LESSHISTFILE=/dev/null
export PYLINTHOME=~/.cache/pylint.d
export npm_config_cache=~/.cache/node

# clean up (config)
export COOKIECUTTER_CONFIG=~/.config/cookiecutter/config.yaml

# expand PATH
PATH=$PATH:$HOME/bin
PATH=$PATH:$HOME/.local/bin
PATH=$PATH:$HOME/Applications

# source bashrc
[[ -f ~/.bashrc ]] && . ~/.bashrc

if [ -z "${DISPLAY}" ] && [ "${XDG_VTNR}" -eq 1 ]; then
  exec startx
fi
