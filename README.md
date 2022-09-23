# ![](icon.svg) <font size="7">Scratch2Python</font>

<img src="https://img.shields.io/github/languages/top/Secret-chest/Scratch2Python?labelColor=546e7a&color=26c6da&logo=python&logoColor=26c6da&style=flat-square"> <img alt="GitHub" src="https://img.shields.io/github/license/Secret-chest/Scratch2Python?style=flat-square&labelColor=546e7a&color=ffa000&label=licence"> <img alt="GitHub issues" src="https://img.shields.io/github/issues/Secret-chest/Scratch2Python?labelColor=546e7a&color=64dd17&logo=github&logoColor=ffffff&style=flat-square"> <img alt="GitHub pull requests" src="https://img.shields.io/github/issues-pr/Secret-chest/Scratch2Python?labelColor=546e7a&color=64dd17&logo=github&logoColor=ffffff&style=flat-square"> <img alt="GitHub milestones" src="https://img.shields.io/github/milestones/open/Secret-chest/Scratch2Python?labelColor=546e7a&color=64dd17&style=flat-square"><a href="https://github.com/Secret-chest/scratch2python/network"> <img alt="GitHub forks" src="https://img.shields.io/github/forks/Secret-chest/scratch2python?labelColor=546e7a&color=ffc107&logo=github&logoColor=ffffff&style=flat-square"></a> <a href="https://github.com/Secret-chest/Scratch2Python/releases"><img alt="GitHub all releases" src="https://img.shields.io/github/downloads/Secret-chest/Scratch2Python/total?color=4caf50&logo=github&style=flat-square&labelColor=546e7a"></a>

<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-4-ff9800.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

Scratch2Python is a Scratch project interpreter that runs Scratch projects in Python, **using pygame to render your sprites**.
<sup>Go to #23 if you want to change the name.</sup>

Unlike others, Scratch2Python can actually _display_ your projects, not only process the variables, control flow, math and logic in the project,
and simply print speech bubble blocks.

It's not finished though. It only supports a few blocks, but it supports them well. The goal is to support almost everything
(save for online services like text-to-speech) when we'll declare it as done. (Of course we'll still update things like the GUI.)

Scratch2Python is not *yet* a transpiler.

## 📝 Requirements and installation
[📥 Visit the website to easily download Scratch2Python](https://secret-chest.github.io/s2p/download/)

Then install from requirements.txt using:

`pip install -r requirements.txt`

Scratch2Python also needs Python 3.8 or newer. [Click here to download Python for Windows and Mac](https://www.python.org/downloads/).
On recent GNU/Linux distros (Ubuntu 20.04+, Debian 11+, Linux Mint 20+, Fedora 32+, updated rolling-release distros),
Python 3 is preinstalled or downloadable from the repositories. Check your distro's documentation for more info.

<details>
<summary>Getting errors on Windows?</summary>

On Windows, Scratch2Python needs to be installed in a non-protected folder.
By default, the “Documents” folder is protected. Installing it anywhere else will work.

To unprotect the “Documents” folder, go to its Properties and uncheck the “Read-only” checkbox.

</details>

## ▶️ Setting the project
Now that you have downloaded Scratch2Python, let's run a project.

### Using test mode
For now Scratch2Python is in test mode by default. That means it will always run the project
defined in the `projectFileName` variable in `config.py`. The variable can be a path, which will load the project there,
or a Scratch ID / URL, which will download and cache the specified online project. No support for downloading unshared
projects is provided! (The Scratch Team will implement access control, and it won't be possible anyway soon too.)

### GUI (experimental)
Change the `testMode` variable to `False` so Scratch2Python will open a GUI when started. For now this is a basic filechooser,
but we'll implement a proper full GUI soon.

## 📖 Wiki
Our [GitHub Wiki](https://github.com/Secret-chest/scratch2python/wiki) may have some outdated information and it is short, but still useful.

## 🧑‍💻 Contributors

Thanks to the people listed here for contributing to Scratch2Python! ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://Secret-chest.github.io"><img src="https://avatars.githubusercontent.com/u/74449186?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Secret-chest</b></sub></a><br /><a href="https://github.com/Secret-chest/scratch2python/commits?author=Secret-chest" title="Code">💻</a> <a href="#projectManagement-Secret-chest" title="Project Management">📆</a> <a href="#design-Secret-chest" title="Design">🎨</a> <a href="https://github.com/Secret-chest/scratch2python/commits?author=Secret-chest" title="Documentation">📖</a> <a href="https://github.com/Secret-chest/scratch2python/issues?q=author%3ASecret-chest" title="Bug reports">🐛</a> <a href="#translation-Secret-chest" title="Translation">🌍</a> <a href="#content-Secret-chest" title="Content">🖋</a></td>
    <td align="center"><a href="https://github.com/tigercoding56"><img src="https://avatars.githubusercontent.com/u/90169211?v=4?s=100" width="100px;" alt=""/><br /><sub><b>tigercoding56</b></sub></a><br /><a href="https://github.com/Secret-chest/scratch2python/commits?author=tigercoding56" title="Documentation">📖</a> <a href="#ideas-tigercoding56" title="Ideas, Planning, & Feedback">🤔</a></td>
    <td align="center"><a href="https://github.com/superscratch444tre"><img src="https://avatars.githubusercontent.com/u/69812464?v=4?s=100" width="100px;" alt=""/><br /><sub><b>superscratch444tre</b></sub></a><br /><a href="https://github.com/Secret-chest/scratch2python/commits?author=superscratch444tre" title="Code">💻</a> <a href="https://github.com/Secret-chest/scratch2python/issues?q=author%3Asuperscratch444tre" title="Bug reports">🐛</a> <a href="https://github.com/Secret-chest/scratch2python/commits?author=superscratch444tre" title="Tests">⚠️</a></td>
    <td align="center"><a href="https://github.com/Melt2002"><img src="https://avatars.githubusercontent.com/u/62972395?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Melt</b></sub></a><br /><a href="https://github.com/Secret-chest/scratch2python/issues?q=author%3AMelt2002" title="Bug reports">🐛</a> <a href="https://github.com/Secret-chest/scratch2python/commits?author=Melt2002" title="Tests">⚠️</a></td>
  </tr>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!
Add your name here: [#29](https://github.com/Secret-chest/scratch2python/issues/29)
