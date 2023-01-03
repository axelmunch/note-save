# Note Save

## Description

Note Save is a simple tool that helps you quickly manage short notes and images in collections.

The application is portable and requires no installation.

Note Save is only available on Windows for the moment.

## Features

- Supports UTF-8 text
- Paste an image or a group of images
- Create collections
- Get the images in the file explorer
- Open collection in the app viewer
- Copy saved text

In future versions :
  - *Edit or delete what's inside a collection*

## Usage / Shortcuts

- `Ctrl + V` : Paste text or images
- `Enter` : Save or validate
- `Shift + Enter` : New line in text
- `Escape` : Delete images, text or close the application

## Run the project

Clone the project :

[SSH]
```sh
git clone git@github.com:axelmunch/note-save.git
```
[HTTPS]
```sh
git clone https://github.com/axelmunch/note-save.git
```

Requirements :

- [Python](https://www.python.org/) >= 3.10
- [Pip](https://pypi.org/project/pip/)

Installing requirememnts :

```sh
pip install -r requirements.txt
```

Running :

```sh
python -m note_save
```

Building :

```sh
build.bat
```
