# Python **virtualenv** Setup

```shell
pip install --upgrade virtualenv
python -m venv .venv --clear --upgrade-deps
.venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install --upgrade -r requirements.txt
# ......
deactivate.bat
```
