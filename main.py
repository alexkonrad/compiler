import argparse

from compiler.parser import Parser
from compiler.graph import Graph

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="file to compile",
                        type=str)
    args = parser.parse_args()
    with open(args.file) as f:
        source = f.read()
    Parser.compile(source)
    g = Graph()
    g.render()

