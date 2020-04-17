with import <nixpkgs> {};
let
  deps = (import ./deps.nix);
  myEmacs = (import ./emacs.nix { inherit pkgs; });
  
in
agda.mkDerivation(self:  {
  name = "agdaShellEnv";
  dontUnpack = true;
  buildDepends = deps.buildDepends;
  buildInputs = deps.buildInputs ++ [
    myEmacs

    # these packages are required for virtualenv and pip to work:
    #
    mypy
    python38Full
    python38Packages.virtualenv
  ];
  # libPath = deps.libPath;
  src = null;
  shellHook = ''

    # set SOURCE_DATE_EPOCH so that we can use python wheels
    SOURCE_DATE_EPOCH=$(date +%s)
    export LANG=en_US.UTF-8

    activate_python_env () {
      source venv/bin/activate
      export PATH=$PWD/venv/bin:$PATH
      export PYTHONPATH=$PWD:$PYTHONPATH
    }
    
    if [ ! -d "venv" ]; then
      # initialize python environment
      virtualenv venv
      activate_python_env
      pip install agda-pkg
    else
      activate_python_env
    fi

    export AGDA_PROJ_DIR=$PWD
    export AGDA_DIR=$AGDA_PROJ_DIR/.agda
    if [ ! -d "$AGDA_DIR" ]; then
      mkdir -p "$AGDA_DIR"
      apkg init
      apkg upgrade
      apkg install -r agda_requirements.txt
    fi


    if [ ! -f "$AGDA_PROJ_DIR/.emacs" ]; then
      export ORIG_HOME=$HOME
      export HOME=$AGDA_PROJ_DIR

      echo '(load (expand-file-name "~/.emacs") "" nil t)' > $AGDA_PROJ_DIR/.emacs
      agda-mode setup
      export EMACS_USER_FILE="$AGDA_PROJ_DIR/.emacs_user_config"
      if [ -f "$EMACS_USER_FILE" ]; then
        cat "$EMACS_USER_FILE" >> $AGDA_PROJ_DIR/.emacs
      fi
      export HOME=$ORIG_HOME
      unset ORIG_HOME
      rmdir .emacs.d
      unset EMACS_USER_FILE
    fi
    
    mymacs () {
      emacs -Q --load $AGDA_PROJ_DIR/.emacs $@
    }
  '';
})
