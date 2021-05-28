# shellcheck shell=bash

export EDITOR=vim
export TERM=alacritty
export BROWSER=firefox

# clean up (cache)
export LESSHISTFILE=/dev/null
export PYLINTHOME=~/.cache/pylint.d
export npm_config_cache=~/.cache/node

# clean up (config)
export PYTHONSTARTUP=~/.config/python/pythonrc
export COOKIECUTTER_CONFIG=~/.config/cookiecutter/config.yaml
export STARSHIP_CONFIG=~/.config/starship/config.toml

# expand PATH
PATH=$PATH:$HOME/bin
PATH=$PATH:$HOME/.local/bin
PATH=$PATH:$HOME/applications

# source secrets
[[ -f ~/.bash_secrets ]] && . ~/.bash_secrets

# source bashrc
[[ -f ~/.bashrc ]] && . ~/.bashrc

if [ -z "${DISPLAY}" ] && [ "${XDG_VTNR}" -eq 1 ]; then
  exec startx
fi
