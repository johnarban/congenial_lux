# .bash_profile
echo "Run John's .bash_profile"
# Get the aliases and functions
if [ -f ~/.bashrc ]; then
	. ~/.bashrc
fi

# load modules
# module load slurm # pre-loaded in default .bashrc
# module load python/3.8.6 # this is currently needed for jupyter notebooks
module load openmpi  # for mpi


source ~/.bash_aliases
source ~/.bash_functions

# User specific environment and startup programs
PATH=$HOME/.local/bin:$PATH
PATH=$PATH:$HOME/casa/bin
PATH=$PATH:$HOME/scripts
export PATH

CASAPATH=$HOME/casa/bin
export CASAPATH

LD_LIBRARY_PATH=$LD_LIBRARY_PATH_modshare:$LD_LIBRARY_PATH:$HOME/.local/lib
export LD_LIBRARY_PATH

MANPATH=$MANPATH:$HOME/.local/share/man
export MANPATH

APPIMAGE_EXTRACT_AND_RUN=1
export APPIMAGE_EXTRACT_AND_RUN



# starlink eao installation
echo "To run starlink programs run <<starlink>> in the terminal"
echo "this may break programs like CASA. So be sure to run in it's own terminal"
starlink () { #function to add starlink to path
    if [ -z "$STARLINK_DIR" ]; then
        export STARLINK_DIR=/home/joarlewi/star-2021A
        source $STARLINK_DIR/etc/profile
    fi
}

source ~/scripts/casaver