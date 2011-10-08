# -*- mode: python -*-
import sys
import os

CTYPES_DIR = "ctypes"
TEST_LIB = os.path.join(CTYPES_DIR, "testctypes")
if sys.platform == "linux2" or sys.platform.startswith('sun') or \
    sys.platform.startswith('aix'):
    TEST_LIB += ".so"
elif sys.platform[:6] == "darwin":
    TEST_LIB += ".dylib"
elif sys.platform == "win32":
    TEST_LIB += ".dll"
else:
    raise NotImplementedError

# If the required dylib does not reside in the current directory, the Analysis
# class machinery, based on ctypes.util.find_library, will not find it. This was
# done on purpose for this test, to show how to give Analysis class a clue.
if sys.platform == "win32":
    os.environ["PATH"] = os.path.abspath(CTYPES_DIR) + ";" + os.environ["PATH"]
else:
    os.environ["DYLD_LIBRARY_PATH"] = CTYPES_DIR
    os.environ["LD_LIBRARY_PATH"] = CTYPES_DIR

os.chdir(CTYPES_DIR)
if sys.platform[:6] == "darwin":
    os.system("gcc -Wall -dynamiclib testctypes.c -o testctypes.dylib -headerpad_max_install_names")
    id_dylib = os.path.abspath("testctypes.dylib")
    os.system("install_name_tool -id %s testctypes.dylib" % (id_dylib,))
elif sys.platform == "linux2" or sys.platform.startswith('sun') or \
    sys.platform.startswith('aix'):
    os.system("gcc -fPIC -shared testctypes.c -o testctypes.so")
else:
    ret = os.system("cl /LD testctypes-win.c")
    if ret != 0:
        ret = os.system("gcc -shared testctypes-win.c -o testctypes.dll")
        if ret != 0:
            raise NotImplementedError("Cannot find either MinGW or Visual Studio in PATH")
os.chdir("..")

__testname__ = 'test_ctypes'

a = Analysis([os.path.join(HOMEPATH, 'support/_mountzlib.py'),
              os.path.join(CONFIGDIR, 'support/useUnicode.py'),
              __testname__ + '.py'],
             pathex=[])
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          name=os.path.join('dist', __testname__, __testname__ + '.exe'),
          debug=False,
          strip=False,
          upx=False,
          console=1 )
