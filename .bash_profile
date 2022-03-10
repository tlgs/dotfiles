# shellcheck shell=bash

export EDITOR=vim
export TERM=alacritty
export BROWSER=firefox

export BAT_THEME='ansi'

# clean up (cache)
export LESSHISTFILE=/dev/null
export PYLINTHOME=$HOME/.cache/pylint.d
export npm_config_cache=$HOME/.cache/node

# clean up (config)
export PYTHONSTARTUP=$HOME/.config/python/pythonrc
export COOKIECUTTER_CONFIG=$HOME/.config/cookiecutter/config.yaml
export STARSHIP_CONFIG=$HOME/.config/starship/config.toml

# clean up (local)
export GOPATH=$HOME/.local/go

# expand PATH
PATH=$PATH:$HOME/bin
PATH=$PATH:$HOME/.local/bin
PATH=$PATH:$HOME/.local/go/bin

# source bashrc
[[ -f ~/.bashrc ]] && . ~/.bashrc
