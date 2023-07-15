import csv
import os
import chardet
import numpy as np
from natsort import natsorted


def __detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        return result['encoding'], result['confidence']


def __read_header_from_csv(filename, ts_delimiter, has_header):
    if has_header:
        header = np.genfromtxt(filename, delimiter=ts_delimiter, names=has_header, max_rows=1, dtype=str).dtype.names
    else:
        first_row = np.loadtxt(filename, delimiter=ts_delimiter, max_rows=1)
        header = ['column-' + str(i) for i in range(len(first_row))]
    return header


def __detect_line_delimiter(filename):
    encoding, _ = __detect_encoding(filename)
    with open(filename, 'r', newline='', encoding=encoding) as file:
        ts_delimiter = csv.Sniffer().sniff(file.readline()).delimiter

    return ts_delimiter


def load_ts_from_csv(filename, has_header=None):
    ts_delimiter = __detect_line_delimiter(filename)

    header = __read_header_from_csv(filename, ts_delimiter, has_header)
    skiprows = 1 if has_header else 0

    return np.loadtxt(filename, delimiter=ts_delimiter, skiprows=skiprows), header


def load_ts_from_path(path, header_ts1, has_header=None):
    if not os.path.exists(path):
        raise FileNotFoundError(f' Path {path} does not exist')
    time_series = {}
    if os.path.isfile(path):
        ts2, header_ts2 = load_ts_from_csv(path, has_header)
        __check_headers(header_ts1, header_ts2)
        time_series[os.path.basename(path)] = ts2
    elif os.path.isdir(path):
        for _, _, files in os.walk(path):
            files = [file for file in files if not file.startswith('.')]
            files = natsorted(files)
            for file in files:
                ts2, header_ts2 = load_ts_from_csv(f'{path}/{file}', has_header)
                __check_headers(header_ts1, header_ts2)
                time_series[file] = ts2

    return time_series


def __check_headers(header_ts1, header_ts2):
    if header_ts1 != header_ts2:
        raise ValueError('All time series must have the same header column names.')
