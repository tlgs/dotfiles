export BROWSER=firefox
export EDITOR=nvim
export TERM=alacritty

XDG_CONFIG_HOME="$HOME/.config"
XDG_CACHE_HOME="$HOME/.cache"
XDG_DATA_HOME="$HOME/.local/share"
XDG_STATE_HOME="$HOME/.local/state"

export ANSIBLE_HOME="${XDG_CONFIG_HOME}"/ansible
export COOKIECUTTER_CONFIG="${XDG_CONFIG_HOME}"/cookiecutter/config.yaml
export DOCKER_CONFIG="${XDG_CONFIG_HOME}"/docker
export IPYTHONDIR="${XDG_CONFIG_HOME}"/ipython
export JUPYTER_CONFIG_DIR="${XDG_CONFIG_HOME}"/jupyter
export MC_CONFIG_DIR="${XDG_CONFIG_HOME}"/mc
export PYTHONSTARTUP="${XDG_CONFIG_HOME}"/python/pythonrc
export STARSHIP_CONFIG="${XDG_CONFIG_HOME}"/starship/config.toml

export npm_config_cache="${XDG_CACHE_HOME}"/node

export CARGO_HOME="${XDG_DATA_HOME}"/cargo
export GNUPGHOME="${XDG_DATA_HOME}"/gnupg
export GOPATH="${XDG_DATA_HOME}"/go

export HISTFILE="${XDG_STATE_HOME}"/bash_history
export SQLITE_HISTORY="${XDG_STATE_HOME}"/sqlite_history

# configuration
export GOPROXY=direct
export GOSUMDB=off

PATH=$PATH:$HOME/bin
PATH=$PATH:$GOPATH/bin

[[ -f ~/.bashrc ]] && . ~/.bashrc
