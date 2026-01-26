#!/bin/bash
set -e

echo "🚀 Setting up development environment..."
mkdir -p "$HOME/.cache/uv"

echo "🚀 Git credentials"
sudo chown -R $(whoami) /workspaces/dev
git config user.name
git config user.email

# Setup uv
uv venv --python 3.12
uv sync

# Note cocotb supports Verilator 5.036+
# sudo apt update
# sudo apt-get install verilator
# verilator --version

# Build from repo
sudo apt update
sudo apt-get install git help2man perl python3 make autoconf g++ flex bison ccache
sudo apt-get install libgoogle-perftools-dev numactl perl-doc
git clone https://github.com/verilator/verilator
unset VERILATOR_ROOT
cd verilator
git checkout stable
autoconf
./configure
make -j `nproc`
sudo make install
verilator --version
