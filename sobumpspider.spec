# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['sobumpspider.py'],
             pathex=['/home/a/Desktop/github/getgot'],
             binaries=[('/home/a/Downloads/CurrencyConverter-0.14.2/currency_converter/eurofxref-hist.zip', 'currency_converter')],
             datas=[],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='sobumpspider',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
