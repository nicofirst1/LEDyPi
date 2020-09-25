import argparse

import yappi

from patterns import Patterns
from rpi import NeoPixel, Dotstar
from utils.rgb import RGB

_NTHREAD = 3

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('pattern', type=str, help='Pattern')
    parser.add_argument('--rate', type=float, help='rate', default=0)
    parser.add_argument('--strip_type', type=str, help='rate', default='neopixel', choices=['neopixel', 'dotstar'])
    parser.add_argument('--pixels', type=int, help='rate', default=300)
    parser.add_argument('--profile', nargs='?', const=True, default=False,
                        help='If to start in debug mode')
    args = parser.parse_args()

    # set pattern, color and handler
    pat = Patterns[args.pattern]
    color = RGB(random=True)

    if args.strip_type == "neopixel":
        handler = NeoPixel(args.pixels)
    else:
        handler = Dotstar(args.pixels)

    # init app and run
    app = pat(handler=handler, rate=args.rate, pixels=args.pixels, color=color)

    # start yappi if profile flag
    if args.profile:
        yappi.start()

    try:
        # run while not stopped
        app.run()
    except KeyboardInterrupt:
        pass
    finally:
        # close app and handler
        app.close()
        handler.close()

    # report yappi stats
    if args.profile:

        yappi.stop()
        threads = yappi.get_thread_stats()
        lines = []
        for thread in threads:
            print(
                "Function stats for (%s) (%d)" % (thread.name, thread.id)
            )  # it is the Thread.__class__.__name__
            yappi.get_func_stats(ctx_id=thread.id).print_all()
