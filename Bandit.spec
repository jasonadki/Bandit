# -*- mode: python -*-
import sys
sys.setrecursionlimit(5000)

block_cipher = None


a = Analysis(['Bandit.py'],
             pathex=['C:\\Users\\adkija\\Desktop\\pythonCode\\RateBookBandit\\RateBookBandit',
       'C:\\Users\\adkija\\Downloads\\C:\\Users\\adkija\\Downloads\\poppler-0.68.0_x86'],
             binaries=[],
             datas=[('C:\\Users\\adkija\\Desktop\\pythonCode\\RateBookBandit\\RateBookBandit\\tabula-1.0.2-jar-with-dependencies.jar', 'tabula'),
             ('C:\\Users\\adkija\\Desktop\\pythonCode\\RateBookBandit\\RateBookBandit\\*.dll', 'pdf2image'),
             ('C:\\Users\\adkija\\Desktop\\pythonCode\\RateBookBandit\\RateBookBandit\\*.exe', 'pdf2image')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Bandit',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True
          )
