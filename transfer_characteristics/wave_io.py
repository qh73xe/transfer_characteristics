# -*- coding: utf-8 -*
"""ファイル等 IO 系処理"""


def save_wav(filename, signals, fs=96, is_32bit=True):
    """Create WAVE file.

    Args:
        filename (str) : 出力する WAVE ファイル名.
        signals (ndarray) : 音声信号.
        fs (int, optional) : サンプリングレート(単位は kHz. デフォルトでは 96 kHz)
        is_32bit (boolean, optional) : 32 bit 音源にするか否か.
            False の場合 16bit PCM 音源になる (デフォルトでは True).

    Returns:
        (None) : ファイルを作成するので返り値は存在しない．

    """
    from scipy.io.wavfile import write
    _fs = fs * 1000
    if is_32bit:
        from numpy import int32
        signals.astype(int32)
    else:
        from numpy import int16
        signals.astype(int16)
    write(filename, _fs, signals)


def play(signals, fs=96):
    import sounddevice as sd
    _fs = fs * 1000
    sd.play(signals, _fs)
    sd.wait()


def rec(duration, fs=96, channels=1, filename=None):
    import sounddevice as sd
    import soundfile as sf
    _fs = fs * 1000
    recording = sd.rec(int(duration * _fs), samplerate=fs, channels=channels)
    sd.wait()
    if filename:
        sf.write(filename, recording, _fs)
    else:
        return recording


def playrec(signals, filename=None, **kwargs):
    import sounddevice as sd
    import soundfile as sf

    fs = kwargs.get("fs", 96)
    _fs = fs * 1000
    recording = sd.rec(len(signals), samplerate=_fs, channels=2)
    sd.play(signals, _fs)
    sd.wait()
    if filename:
        sf.write(filename, recording, _fs)
    else:
        return recording
