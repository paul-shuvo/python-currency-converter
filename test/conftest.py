import sys
from os.path import dirname, join, abspath

root_dir = dirname(dirname(abspath(__file__)))
sys.path.append(join(root_dir, "currency-converter"))
