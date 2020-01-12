#!/usr/bin/env python3


def trace_calls(frame, event, arg):
    print(frame.f_code)
