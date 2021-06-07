gnome = import('gnome')
python = import('python')

pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'tasko')

gnome.compile_resources(
    'tasko',
    'tasko.gresource.xml',
    gresource_bundle: true,
    install: true,
    install_dir: pkgdatadir,
)

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
    input: 'tasko.in',
    output: 'tasko',
    configuration: conf,
    install: true,
    install_dir: get_option('bindir')
)

sources = [
    '__init__.py',
    'define.py',
    'application.py',
    'window.py',
    'database.py'
]

install_data(sources, install_dir: moduledir)
