
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-1-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->
![Logo](s2p.svg)

<img src="https://img.shields.io/github/languages/top/Secret-chest/Scratch2Python?labelColor=546e7a&color=26c6da&logo=python&logoColor=26c6da&style=flat-square"> <img alt="GitHub" src="https://img.shields.io/github/license/Secret-chest/Scratch2Python?style=flat-square&labelColor=546e7a&color=ffa000"> <img alt="GitHub issues" src="https://img.shields.io/github/issues/Secret-chest/Scratch2Python?labelColor=546e7a&color=64dd17&logo=github&logoColor=ffffff&style=flat-square"> <img alt="GitHub pull requests" src="https://img.shields.io/github/issues-pr/Secret-chest/Scratch2Python?labelColor=546e7a&color=64dd17&logo=github&logoColor=ffffff&style=flat-square"> <img alt="GitHub milestones" src="https://img.shields.io/github/milestones/open/Secret-chest/Scratch2Python?labelColor=546e7a&color=64dd17&style=flat-square"><a href="https://github.com/Secret-chest/scratch2python/network"> <img alt="GitHub forks" src="https://img.shields.io/github/forks/Secret-chest/scratch2python?labelColor=546e7a&color=ffc107&logo=github&logoColor=ffffff&style=flat-square"></a>

# Scratch2Python
Scratch2Python is a Scratch project interpreter that runs Scratch projects in Python, using pygame to render your sprites.

A GUI for accessing the Scratch website is planned. It will most probably use... Qt. I would love using GTK, but **WINDOWS...** [Or maybe not](https://www.gtk.org/docs/installations/windows).

Scratch2Python may only be the temporary name, as this may get confused with [Scratch2Py](https://github.com/The-Cloud-Dev/scratch2py). See #23 for more information.
## 📝 Requirements
Install from requirements.txt (Scratch2Python also needs Python 3.8 or newer).

On Windows, Scratch2Python needs to be installed in a non-protected folder.
By default, the "Documents" folder is protected. Installing it anywhere else will work.

## 📘 Docs
[Read the wiki here](https://github.com/Secret-chest/scratch2python/wiki). Also read `CONTRIBUTING.md`.

## 🔨 How to use 
Assuming that you installed all necessary requirements, place your sb3 files somewhere accessible, or in the Scratch2Python folder. You can use an absolute or relative path.
Then, go to `config.py` and change the projectFileName variable to your project file.
There you can also choose to use a command-line argument, or an interactive prompt. The variable option is the default as it's more useful for testing.

Now, just run `python3 main.py` and the project will start!

### ✅ Config
The `config.py` file contains some more configuration options.

Each of them is nicely explained, so why not just check it out?

## 🌐 Localization
To translate Scratch2Python, add a new file in the `lang` directory. Copy the English file for reference, and replace the string.

Then add it on the supported languages list both here and in `config.py`.
Though I would not recommend translating it right now. It is still very WIP and you would have to update your language
file very frequently.

Currently supported languages:

| Language code | Language name (English) | Language name (translated) | Flag |
|---------------|-------------------------|----------------------------|------|
| en            | English                 | English                    | 🇬🇧 |
| ro            | Romanian                | limba română               | 🇷🇴 |

## ✨ Contributors

These people have contributed to this project and helped shape it ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://Secret-chest.github.io"><img src="https://avatars.githubusercontent.com/u/74449186?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Secret-chest</b></sub></a><br /><a href="https://github.com/Secret-chest/scratch2python/commits?author=Secret-chest" title="Code">💻</a> <a href="#projectManagement-Secret-chest" title="Project Management">📆</a> <a href="#design-Secret-chest" title="Design">🎨</a> <a href="https://github.com/Secret-chest/scratch2python/commits?author=Secret-chest" title="Documentation">📖</a> <a href="https://github.com/Secret-chest/scratch2python/issues?q=author%3ASecret-chest" title="Bug reports">🐛</a> <a href="#translation-Secret-chest" title="Translation">🌍</a></td>
  </tr>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!
Add your name here: [https://github.com/Secret-chest/scratch2python/issues/29](issue #29)
