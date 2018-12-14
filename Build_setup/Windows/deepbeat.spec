# -*- mode: python -*-

block_cipher = None

specpath = os.path.dirname(os.path.abspath(SPEC))

a = Analysis(['Deepbeat.py'],
             pathex=['C:\\Users\\eugene.upston\\Desktop\\mypython\\Deepbeat Gui\\Deepbeat Gui'],
             binaries=[],
             datas=[
             ('C:/Users/eugene.upston/Desktop/mypython/Deepbeat Gui/deepbeatv4/resources/drumkits/Drum_Kit_1/hihat.wav', '/resources/drumkits/Drum_Kit_1/'),
             ('C:/Users/eugene.upston/Desktop/mypython/Deepbeat Gui/deepbeatv4/resources/drumkits/Drum_Kit_1/kick.wav', '/resources/drumkits/Drum_Kit_1/'),
             ('C:/Users/eugene.upston/Desktop/mypython/Deepbeat Gui/deepbeatv4/resources/drumkits/Drum_Kit_1/snare.wav', '/resources/drumkits/Drum_Kit_1/'),
             ('C:/Users/eugene.upston/Desktop/mypython/Deepbeat Gui/deepbeatv4/resources/drumkits/Drum_Kit_2/hihat.wav', '/resources/drumkits/Drum_Kit_2/'),
             ('C:/Users/eugene.upston/Desktop/mypython/Deepbeat Gui/deepbeatv4/resources/drumkits/Drum_Kit_2/kick.wav', '/resources/drumkits/Drum_Kit_2/'),
             ('C:/Users/eugene.upston/Desktop/mypython/Deepbeat Gui/deepbeatv4/resources/drumkits/Drum_Kit_2/snare.wav', '/resources/drumkits/Drum_Kit_2/'),
             ('C:/Users/eugene.upston/Desktop/mypython/Deepbeat Gui/deepbeatv4/resources/drumkits/Drum_Kit_3/hihat.wav', '/resources/drumkits/Drum_Kit_3/'),
             ('C:/Users/eugene.upston/Desktop/mypython/Deepbeat Gui/deepbeatv4/resources/drumkits/Drum_Kit_3/kick.wav', '/resources/drumkits/Drum_Kit_3/'),
             ('C:/Users/eugene.upston/Desktop/mypython/Deepbeat Gui/deepbeatv4/resources/drumkits/Drum_Kit_3/snare.wav', '/resources/drumkits/Drum_Kit_3/'),
             ('C:/Users/eugene.upston/Desktop/mypython/Deepbeat Gui/deepbeatv4/resources/drumkits/Drum_Kit_4/hihat.wav', '/resources/drumkits/Drum_Kit_4/'),
             ('C:/Users/eugene.upston/Desktop/mypython/Deepbeat Gui/deepbeatv4/resources/drumkits/Drum_Kit_4/kick.wav', '/resources/drumkits/Drum_Kit_4/'),
             ('C:/Users/eugene.upston/Desktop/mypython/Deepbeat Gui/deepbeatv4/resources/drumkits/Drum_Kit_4/snare.wav', '/resources/drumkits/Drum_Kit_4/'),
             ('C:/Users/eugene.upston/Desktop/mypython/Deepbeat Gui/deepbeatv4/resources/beatbox.mid','/resources/'),
             ('C:/Users/eugene.upston/Desktop/mypython/Deepbeat Gui/deepbeatv4/resources/output.wav','/resources/'),
             ('C:/Users/eugene.upston/Desktop/mypython/Deepbeat Gui/deepbeatv4/resources/beatbox_model2.hdf5','/resources/'),
             ('C:/Users/eugene.upston/Desktop/mypython/Deepbeat Gui/deepbeatv4/resources/images/convert_to_midi5.png','/resources/images'),
             ('C:/Users/eugene.upston/Desktop/mypython/Deepbeat Gui/deepbeatv4/resources/images/metronome_shadow.png','/resources/images'),
             ('C:/Users/eugene.upston/Desktop/mypython/Deepbeat Gui/deepbeatv4/resources/images/metronome_unchecked.png','/resources/images'),
             ('C:/Users/eugene.upston/Desktop/mypython/Deepbeat Gui/deepbeatv4/resources/images/midi_loop_shadow.png','/resources/images'),
             ('C:/Users/eugene.upston/Desktop/mypython/Deepbeat Gui/deepbeatv4/resources/images/midi_loop_unchecked.png','/resources/images'),
             ('C:/Users/eugene.upston/Desktop/mypython/Deepbeat Gui/deepbeatv4/resources/images/midi_pausebutton_shadow.png','/resources/images'),
             ('C:/Users/eugene.upston/Desktop/mypython/Deepbeat Gui/deepbeatv4/resources/images/midi_playbutton_shadow.png','/resources/images'),
             ('C:/Users/eugene.upston/Desktop/mypython/Deepbeat Gui/deepbeatv4/resources/images/pause_shadow.png','/resources/images'),
             ('C:/Users/eugene.upston/Desktop/mypython/Deepbeat Gui/deepbeatv4/resources/images/playbutton_shadow.png','/resources/images'),
             ('C:/Users/eugene.upston/Desktop/mypython/Deepbeat Gui/deepbeatv4/resources/images/recbutton_shadow.png','/resources/images'),
             ('C:/Users/eugene.upston/Desktop/mypython/Deepbeat Gui/deepbeatv4/resources/images/scissors_shadow.png','/resources/images'),
             ('C:/Users/eugene.upston/Desktop/mypython/Deepbeat Gui/deepbeatv4/resources/images/stopbutton_shadow.png','/resources/images'),

             ],
             hiddenimports=['sklearn', 'sklearn.ensemble', 'sklearn.neighbors.typedefs', 'sklearn.neighbors.quad_tree', 'sklearn.tree._utils'],
             hookspath=[],
             runtime_hooks=[],
             excludes=['PyQt4'],
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
          name='Deepbeat',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          icon='resources/images/Deepbeat_Icon3.ico',
          console=False )
