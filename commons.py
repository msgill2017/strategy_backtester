try:
    import pandas as pd
except ImportError:
    pass


def open_file(filename):
    try:
        return pd.read_csv(filename)
    except:
        print("File is Missing")