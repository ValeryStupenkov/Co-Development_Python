from cowsay import cowsay, list_cows
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-e", type=str)
parser.add_argument("-f", type=str)
parser.add_argument("message", type=str)

args = parser.parse_args()

dict_args = {}

if args.e:
    dict_args["eyes"] = args.e[:2]
if args.f:
    dict_args["cowfile"] = args.f

dict_args["message"] = args.message
print(cowsay(**dict_args))