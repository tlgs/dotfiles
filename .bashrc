# shellcheck shell=bash

# if not running interactively, don't do anything
[[ $- != *i* ]] && return

alias ls='ls --color=auto'
alias config='/usr/bin/git --git-dir=$HOME/.dotfiles --work-tree=$HOME'

eval "$(starship init bash)"
