export BROWSER=firefox
export EDITOR=vim
export TERM=alacritty

# clean up (cache)
export npm_config_cache=$HOME/.cache/node
export CARGO_HOME=$HOME/.cache/cargo
export LESSHISTFILE=/dev/null
export PYLINTHOME=$HOME/.cache/pylint.d
export SQLITE_HISTORY=$HOME/.cache/sqlite/history

# clean up (config)
export COOKIECUTTER_CONFIG=$HOME/.config/cookiecutter/config.yaml
export DOCKER_CONFIG=$HOME/.config/docker
export IPYTHONDIR=$HOME/.config/ipython
export JUPYTER_CONFIG_DIR=$HOME/.config/jupyter
export PYTHONSTARTUP=$HOME/.config/python/pythonrc
export STARSHIP_CONFIG=$HOME/.config/starship/config.toml

# clean up (local)
export GNUPGHOME=$HOME/.local/share/gnupg
export GOPATH=$HOME/.local/share/go
export VAGRANT_HOME=$HOME/.local/share/vagrant

# configuration
export GOPROXY=direct
export GOSUMDB=off

# expand PATH
PATH=$PATH:$HOME/bin
PATH=$PATH:$GOPATH/bin

# source bashrc
[[ -f ~/.bashrc ]] && . ~/.bashrc
