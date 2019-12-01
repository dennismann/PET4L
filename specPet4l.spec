# -*- mode: python -*-
import sys
import os.path as os_path
import simplejson as json

os_type = sys.platform
block_cipher = None
base_dir = os_path.dirname(os_path.realpath('__file__'))

def libModule(module, source, dest):
	m = __import__(module)
	module_path = os_path.dirname(m.__file__)
	del m
	print("libModule %s" % str(( os_path.join(module_path, source), dest )))
	return ( os_path.join(module_path, source), dest )

# look for version string
version_str = ''
with open(os_path.join(base_dir, 'src', 'version.txt')) as version_file:
	version_data = json.load(version_file)
version_file.close()
version_str = version_data["number"] + version_data["tag"]

add_files = [('src/version.txt', '.'), ('img', 'img')]
add_files.append( libModule('bitcoin', 'english.txt','bitcoin') )
add_files.append( (os.path.join(lib_path, 'trezorlib/coins.json'), 'trezorlib') )
add_files.append( (os.path.join(lib_path, 'trezorlib/transport'), 'trezorlib/transport') )

elif os_type == 'win32':
    import ctypes.util
    l = ctypes.util.find_library('libusb-1.0.dll')
    if l:
       add_files.append( (l, '.') )


a = Analysis(['pet4l.py'],
             pathex=[base_dir, 'src', 'src/qt'],
             binaries=[],
             datas=add_files,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[ 'numpy',
                        'cryptography',
                        'lib2to3',
                        'pkg_resources',
                        'distutils',
                        'Crypto',
                        'pyi_rth_qt5',
                        'pytest',
                        'scipy',
                        'pycparser',
                        'pydoc',
                        'PyQt5.QtHelp',
                        'PyQt5.QtMultimedia',
                        'PyQt5.QtNetwork',
                        'PyQt5.QtOpenGL',
                        'PyQt5.QtPrintSupport',
                        'PyQt5.QtQml',
                        'PyQt5.QtQuick',
                        'PyQt5.QtQuickWidgets',
                        'PyQt5.QtSensors',
                        'PyQt5.QtSerialPort',
                        'PyQt5.QtSql',
                        'PyQt5.QtSvg',
                        'PyQt5.QtTest',
                        'PyQt5.QtWebEngine',
                        'PyQt5.QtWebEngineCore',
                        'PyQt5.QtWebEngineWidgets',
                        'PyQt5.QtXml',
                        'win32com',
                        'xml.dom.domreg',
                        ],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.binaries,
          a.zipfiles,
          a.datas,
          a.scripts,
          name='pet4l',
          debug=False,
          strip=False,
          upx=False,
          console=False,
          icon=os_path.join(base_dir, 'img', 'spmt.%s' % ('icns' if os_type=='darwin' else 'ico')) )

if os_type == 'darwin':
	app = BUNDLE(exe,
             name='pet4l.app',
             icon=os_path.join(base_dir, 'img', 'spmt.icns'),
             bundle_identifier=None,
             info_plist={'NSHighResolutionCapable': 'True'})


# Prepare bundles
dist_path = os_path.join(base_dir, 'dist')
app_path = os_path.join(dist_path, 'app')
os.chdir(dist_path)

if os_type == 'win32':
	os.chdir(base_dir)
	# Rename dist Dir
	dist_path_win = os_path.join(base_dir, 'PET4L-v' + version_str + '-Win64')
	os.rename(dist_path, dist_path_win)
	# Create NSIS compressed installer
	print('Creating Windows installer (requires NSIS)')
	os.system('\"c:\\program files (x86)\\NSIS\\makensis.exe\" %s' % os.path.join(base_dir, 'setup.nsi'))

if os_type == 'linux':
	os.chdir(base_dir)
	# Rename dist Dir
	dist_path_linux = os_path.join(base_dir, 'PET4L-v' + version_str + '-gnu_linux')
	os.rename(dist_path, dist_path_linux)
	# Compress dist Dir
	print('Compressing Linux App Folder')
	os.system('tar -zcvf %s -C %s %s' % ('PET4L-v' + version_str + '-x86_64-gnu_linux.tar.gz',
                base_dir, 'PET4L-v' + version_str + '-gnu_linux'))

if os_type == 'darwin':
    os.chdir(base_dir)
    # Rename dist Dir
    dist_path_mac = os_path.join(base_dir, 'PET4L-v' + version_str + '-MacOSX')
    os.rename(dist_path, dist_path_mac)
    # Remove 'app' folder
    print("Removin 'app' folder")
    os.chdir(dist_path_mac)
    os.system('rm -rf app')
    os.chdir(base_dir)
    # Compress dist Dir
    print('Compressing Mac App Folder')
    os.system('tar -zcvf %s -C %s %s' % ('PET4L-v' + version_str + '-MacOSX.tar.gz',
                base_dir, 'PET4L-v' + version_str + '-MacOSX'))


