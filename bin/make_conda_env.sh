%%writefile make_conda_env.sh
#!/usr/bin/env bash

read -p "Create new conda env (y/n)?" CONT

if [ "$CONT" == "n" ]; then
  echo "exit";
else

  echo "Creating new conda environment, choose name"
  read input_variable
  echo "Name $input_variable was chosen";

  echo "installing base packages"
  conda create --name $input_variable\
  python=3.10
    fi
  echo "to exit: source deactivate"
fi
