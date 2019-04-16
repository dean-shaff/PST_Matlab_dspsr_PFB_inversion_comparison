import os
import subprocess
import shlex
import json

import matplotlib.pyplot as plt
import numpy as np

__all__ = [
    "updir",
    "curdir",
    "run_cmd",
    "find_existing_test_data",
    "create_output_file_names",
    "matlab_dtype_lookup"
]


meta_data_file_name = "meta.json"


matlab_dtype_lookup = {
    np.float32: "single",
    np.float64: "double",
    np.complex64: "single",
    np.complex128: "double"
}


def find_existing_test_data(base_dir, domain_name, params):
    """
    Determine if any existing test data exist in given base_dir

    Args:
        base_dir (str): The base directory from where search will begin
        domain_name (str): "time" or "freq"
        params (tuple or dict): Dictionary or tuple of arguments for
            test vector creation
    """

    arg_order = {
        "time": ("offset", "width"),
        "freq": ("frequency", "phase", "bin_offset")
    }

    sub_dir_format_map = {
        "time": "o-{offset:.3f}_w-{width:.3f}",
        "freq": "f-{frequency:.3f}_b-{bin_offset:.3f}_p-{phase:.3f}"
    }

    sub_dir_formatter = sub_dir_format_map[domain_name]

    if not hasattr(params, "keys"):
        params_dict = {
            arg_name: params[i]
            for i, arg_name in enumerate(arg_order[domain_name])
        }
    else:
        params_dict = params

    sub_dir = sub_dir_formatter.format(**params_dict)

    sub_dir_full = os.path.join(base_dir, domain_name, sub_dir)
    meta_data = None
    if os.path.exists(sub_dir_full):
        meta_data_file_path = os.path.join(sub_dir, meta_data_file_name)
        with open(meta_data_file_path, 'r') as f:
            meta_data = json.load(f)

    return meta_data


def run_cmd(cmd_str: str, log_file_path: str = None):

    cmd_split = shlex.split(cmd_str)
    if log_file_path is not None:
        with open(log_file_path, "w") as log_file:
            cmd = subprocess.run(cmd_split,
                                 stdout=log_file,
                                 stderr=log_file)
    else:
        cmd = subprocess.run(cmd_split)

    if cmd.returncode != 0:
        raise RuntimeError("Exited with non zero status")

    return cmd


def create_output_file_names(output_file_name, default_base):
    if output_file_name is None:
        output_base = default_base
        output_file_name = output_base + ".dump"
    else:
        output_base = os.path.splitext(output_file_name)[0]
    log_file_name = output_base + ".log"

    return output_base, log_file_name, output_file_name


def report2plot(report_file_path, output_dir="./", output_file_name=None):
    """
    Take a report generated by a testing pipeline and create a plot.
    """
    if output_file_name is None:
        output_file_name = os.path.splitext(
            os.path.basename(report_file_path))[0] + ".png"
    output_file_path = os.path.join(output_dir, output_file_name)

    


def updir(base_dir, levels):
    """
    Go up `levels` number of directories
    """
    if levels == 0:
        return base_dir
    else:
        return updir(os.path.dirname(base_dir), levels - 1)


def curdir(file_path):
    """
    Get the current directory where a given file resides
    """
    return os.path.dirname(os.path.abspath(file_path))
