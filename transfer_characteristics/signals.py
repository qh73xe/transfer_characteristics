# -*- coding: utf-8 -*
"""信号処理一般関数"""


def gen_chirp(duration, fs=96, **kwargs):
    """Generate chirp signal.

    特定の長さのチャープ信号を返します．

    Args:
        duration (float) : 生成する信号の持続時間 (単位は sec).
        fs (int, optional) : 生成する信号のサンプリング周波数
            (単位は kHz. デフォルトでは 96kHz)
        **kwargs: scipy.signal.chirp 関数に渡すその他の引数.
            これには以下のものがあります．
            f0 (float) : Frequency (e.g. Hz) at time t=0.
            f1 (float) : Frequency (e.g. Hz) of the waveform at time t1.

    Returns:
        (t, y) : 時刻列 t と 信号列 y を返します．
            なお, これらは全て numpy/ndarray 型です．

    Examples:
        以下に 10 秒間のチャープ信号を作成する例を示します.

        >>> t, y = gen_chirp(10)
        >>> y.size
        960000
        >>> t.size
        960000

    """
    from numpy import linspace
    from scipy.signal import chirp
    _fs = fs * 1000
    _f0 = kwargs.get("f0", 20)
    _f1 = kwargs.get("f1", 40000)
    t = linspace(0, duration, _fs * duration)
    w = chirp(t, f0=_f0, f1=_f1, t1=duration)
    return t, w


def fft(signals, fs=96):
    """Return amplitude spectrum of real sequence.

    引数 signals で与えられた波形列を fft した結果を返します．
    正確には信号の振幅スペクトル

    Examples:

        >>> t, y = gen_chirp(10)
        >>> freq, amp = fft(y)

    """
    from scipy import fftpack
    from numpy import abs
    _fs = fs * 1000
    _n = signals.size
    fft = fftpack.fft(signals) / (_n / 2)
    freq = fftpack.fftfreq(n=_n, d=1 / _fs)
    return freq[1:int(freq.size / 2)], abs(fft[1:int(fft.size / 2)])


def to_dB(amplitudes):
    """amplitudes を db に変換します."""
    from numpy import log10
    from sys import float_info
    return 20 * log10(amplitudes + float_info.min)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
