# -*- mode: python ; coding: utf-8 -*-
import sys
sys.setrecursionlimit(10000)
block_cipher = None

pf_foldr='C:\\Users\\DELL\\PLAYGROUND\\Anaconda3\\envs\\py37_32\\Library\\plugins\\platforms\\'

a = Analysis(['Program_main.py'],
             pathex=['C:\\Users\\DELL\\PLAYGROUND\\hkdevstudio\\Tiautory'],
             binaries=[],
             datas=[('./img','.'),
                    ('./lib/*.exe','./lib'),
                    ('./nohand','./blogInfo.properties')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='Tiautory',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='Tiautory')
