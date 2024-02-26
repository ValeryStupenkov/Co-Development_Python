from cowsay import cowsay, list_cows
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-e", type=str)
parser.add_argument("-f", type=str)
parser.add_argument("-T", type=str)
parser.add_argument('-b', action='store_true')
parser.add_argument('-d', action='store_true')
parser.add_argument('-g', action='store_true')
parser.add_argument('-p', action='store_true')
parser.add_argument('-s', action='store_true')
parser.add_argument('-t', action='store_true')
parser.add_argument('-w', action='store_true')
parser.add_argument('-y', action='store_true')
parser.add_argument("-W", type=int)
parser.add_argument("-l", action='store_true')
parser.add_argument("message", nargs='?', default=None)

args = parser.parse_args()
dict_args = {}

if args.e:
    dict_args["eyes"] = args.e[:2]
if args.f:
    dict_args["cowfile"] = args.f
if args.T:
    dict_args["tongue"] = args.T
if args.W:
    dict_args["width"] = args.W

if args.b:
    dict_args['preset'] = "b"
if args.d:
    dict_args['preset'] = "d"
if args.g:
    dict_args['preset'] = "g"
if args.p:
    dict_args['preset'] = "p"
if args.s:
    dict_args['preset'] = "s"
if args.t:
    dict_args['preset'] = "t"
if args.w:
    dict_args['preset'] = "w"
if args.y:
    dict_args['preset'] = "y"

if args.l:
    print(list_cows())

dict_args["message"] = args.message

if args.message is not None and not args.l:
    print(cowsay(**dict_args))