which virtualenv || { echo "virtualenv commmand not found, please install virtualenv"; exit 1; }
# Create virtualenv if not already created
find venv || python3 -m venv venv;
# Activate virtualenv and install requirements
source venv/bin/activate &&
pip3 install -U pip wheel setuptools &&
find requirements.txt &&
pip install -r requirements.txt &&
echo "Succes! To activate virtualenv : \`source venv/bin/activate\`, to exit virtual env: \`deactivate\`"
