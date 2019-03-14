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
    if is_32bit == 32:
        from numpy import int32
        signals.astype(int32)
    else:
        from numpy import int16
        signals.astype(int16)

    _fs = fs * 1000
    write(filename, _fs, signals)
