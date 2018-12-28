import argparse
from utils import mix_speechs

def main(args):
    mix_speechs(args)
if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--data_dir',default='data/speechs', type=str)
    parser.add_argument('-o', '--outdir',default='data/output', type = str)
    parser.add_argument("-i", "--initial_position", default=3, type = int)
    parser.add_argument("-l", "--overlay_type", choices=["successive", "same"], default="successive")
    parser.add_argument("-n", "--num_overlay", default=2,type=int)
    parser.add_argument('-f', '--format', nargs='+', type=str, default=["flac"])
    parser.add_argument('-r', '--decibel_range', default=4, type=int)

    args = parser.parse_args()
    main(args)