# -*- mode: python ; coding: utf-8 -*-
from pathlib import Path
from PyInstaller.utils.hooks import collect_submodules

ROOT = Path(SPECPATH).parent
hiddenimports = collect_submodules('src')

analysis = Analysis(
    ['src/main.py'],
    pathex=[str(ROOT)],
    binaries=[],
    datas=[
        (str(ROOT / 'assets'), 'assets'),
        (str(ROOT / 'src' / 'resources'), 'src/resources'),
    ],
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(analysis.pure)
exe = EXE(
    pyz,
    analysis.scripts,
    analysis.binaries,
    analysis.datas,
    [],
    name='AsistenteONG',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon=str(ROOT / 'assets' / 'logo_g.png'),
)
