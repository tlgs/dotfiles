# shellcheck shell=bash

export EDITOR=vim
export TERM=alacritty
export BROWSER=firefox

# clean up (cache)
export npm_config_cache=$HOME/.cache/node
export CARGO_HOME=$HOME/.cache/cargo
export LESSHISTFILE=/dev/null
export PYLINTHOME=$HOME/.cache/pylint.d
export SQLITE_HISTORY="$HOME/.cache/sqlite/history"

# clean up (config)
export COOKIECUTTER_CONFIG=$HOME/.config/cookiecutter/config.yaml
export PYTHONSTARTUP=$HOME/.config/python/pythonrc
export STARSHIP_CONFIG=$HOME/.config/starship/config.toml

# clean up (local)
export GOPATH=$HOME/.local/go

# configuration
export GOPROXY=direct

# expand PATH
PATH=$PATH:$HOME/bin
PATH=$PATH:$HOME/.local/bin
PATH=$PATH:$HOME/.local/go/bin

# source bashrc
[[ -f ~/.bashrc ]] && . ~/.bashrc
