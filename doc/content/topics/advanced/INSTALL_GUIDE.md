# Complete installation guide

This guide covers all installation options.

* [Shipan installation](#install_shipan)
  * [Install an official release](#official)
  * [Install the latest development version](#development)
* [Advanced tools](#advanced)
  * [Thesaurus](#thesaurus)
     * [gettext](#gettext)
     * [libstdc](#libstdc)
     * [Reboot](#reboot)
     * [That's it](#thatsit)

## Shipan installation
<a name='install_shipan'></a>

Select an installation method according to your needs:

* [Install an official release](#official) if you need a functional version
* [Install an development version](#development) if you want to test incoming features

### Install an official release
<a name='official'></a>

The default configuration of a **Shipan** Release is ready-to-use and made for Production environments,
 so the installation procedure is quite simple in order to obtain a functional website:

1. **Python 2.7**
   
   Download and install a `Python 2.7.x` release from [Python downloads](https://www.python.org/downloads/)

1. **Shipan**

   Download and install the last release version of **Shipan** from its official repository:
   ```
   git clone https://github.com/rlichiere/shipan.git
   python manage.py install
   ```

### Install the latest development version
<a name='development'></a>

The development version of **Shipan** should be ready-to-use, but some bugs might been encountered.

Proceed the same as the [official release](#official) installation method, except for the repository, for which you must obtain the development branch:
```
git clone https://github.com/rlichiere/shipan.git --branch develop
```

## Advanced tools
<a name='advanced'></a>

**Shipan** exposes some advanced tools mainly to facilitate the maintenance operations.

### Thesaurus
<a name='thesaurus'></a>

The **Thesaurus** tool allows you to **customize Shipan traduction messages**.

To use them on a _Windows_ operating system, you may have to install additional requirements.
Follow the following procedure to perform this installation.

#### 1. `gettext`
<a name='gettext'></a>

1. Download and unzip from [here](http://ftp.gnome.org/pub/gnome/binaries/win32/dependencies/):
   * `gettext-runtime_0.18.1.1-2_win32`
   * `gettext-tools-dev_0.18.1.1-2_win32`
1. Add their `bin` folder to the `PATH` of the operating system.

#### 2. `libstdc`
<a name='thesaurus'></a>

1. Download `libstdc++-6.dll` from [here](https://www.dll-files.com/libstdc++-6.dll.html)
1. Copy it to your system directory (`C:\Windows\SysWow64` or `C:\Windows\System32`)

### 3. Reboot
<a name='reboot'></a>

_Windows_ requires a reboot in order to considerate its `PATH` modifications.

#### That's it
<a name='thatsit'></a>

Once `gettext` and `libstdc` are installed, you can export, customize and reimport messages.

Report to the [Thesaurus](/doc/content/topics/advanced/THESAURUS.md) documentation for further information.
