import os
import argparse

if __name__=="__main__":
    parser = argparse.ArgumentParser("lister", "this program rename all of the files in the inputed folder")
    parser.add_argument("add", default="_test")
    parser.add_argument("--path", "-p", help="the path to explore")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()
    
    path = os.path.join(str(args.path))
    if not os.path.isdir(path):
        raise ValueError(f"The value {args.path} isn't a valid directory")
    
    for root, _, files in os.walk(path):
        for file in files:
            old_path = os.path.join(root, file)
            new_path = os.path.join(root, os.path.basename(file)+args.add)
            os.rename(old_path, new_path)
            if args.verbose:
                print(f"[{root}] {file} -> {os.path.basename(file)+args.add}")