# Python functions to print colored text
def prRed(skk, e="\n"): print("\033[91m {}\033[00m" .format(skk), end=e)
def prGreen(skk, e="\n"): print("\033[92m {}\033[00m" .format(skk), end=e)
def prYellow(skk, e="\n"): print("\033[93m {}\033[00m" .format(skk), end=e)
def prLightPurple(skk, e="\n"): print("\033[94m {}\033[00m" .format(skk), end=e)
def prPurple(skk, e="\n"): print("\033[95m {}\033[00m" .format(skk), end=e)
def prCyan(skk, e="\n"): print("\033[96m {}\033[00m" .format(skk), end=e)
def prLightGray(skk, e="\n"): print("\033[97m {}\033[00m" .format(skk), end=e)
def prBlack(skk, e="\n"): print("\033[98m {}\033[00m" .format(skk), end=e)


def best_duration(t_nanoseconds):
    t_nanoseconds = int(t_nanoseconds)  # make sure input is a number

    t_us = t_nanoseconds / 1000
    t_ms = t_us / 1000
    t_s = t_ms / 1000
    t_m = t_s / 60
    t_h = t_m / 60
    t_d = t_h / 24

    if t_d >= 1:
        rem_h = t_h % 24
        rem_m = t_m % 60
        rem_s = t_s % (24 * 60 * 60) % 60
        return "{}d {}h {}m {}s".format(t_d, rem_h, rem_m, rem_s)
    elif t_h >= 1:
        rem_m = t_m % 60
        rem_s = t_s % (60 * 60) % 60
        return "{}h {}m {}s".format(t_h, rem_m, rem_s)
    elif t_m >= 1:
        rem_s = t_s % 60
        return "{}m {}s".format(t_m, rem_s)
    elif t_s >= 10:
        return "{} s".format(t_s)
    elif t_ms >= 10:
        return "{} ms".format(t_ms)
    elif t_us >= 1:
        return "{} μs".format(t_us)
    else:
        return "{} ns".format(t_nanoseconds)