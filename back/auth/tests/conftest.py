import sys
import pathlib

auth_dir = pathlib.Path(__file__).parents[1].resolve()
sys.path.append(str(auth_dir))
