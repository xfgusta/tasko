<img height="128" src="data/icons/hicolor/scalable/apps/com.github.xfgusta.tasko.svg" align="left"/>

# Tasko

A simple to-do list app for GNOME

<br>

<p float="middle">
  <img src="data/img/tasks.png?raw=true"/>
  <img src="data/img/menu.png?raw=true"/> 
</p>

Tasko /'tasko/ (task in Esperanto)  is a simple to-do list for GNOME. It is designed to be simple and reliable. You just open the app, write down your tasks and close it. You can also mark the tasks as done and remove them later. Everything is fast and easy to use.

## Installation 

### Requirements

- Python 3 `python`
- PyGObject `python-gobject`
- GTK3 `gtk3`
- Meson `meson`
- Ninja `ninja`

Build and install with:

```
git clone https://github.com/xfgusta/tasko.git
cd tasko
meson build
```

And then `ninja -C build install` as root.

To uninstall, run `ninja -C build uninstall` as root as well.

## License

The MIT License (MIT)

Copyright (C) 2021 Gustavo Costa
