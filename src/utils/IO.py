import json
import os
import re

import shutil
import socket

info_file = 'resources/info.json'
config_file = 'config.json'
models_folder = 'resources/models'
tmp_folder = 'resources/tmp'


# IO

def check_file(path):
    """
    TODO DOCUMENTATION
    :param path:
    :return:
    """
    if not os.path.isfile(path):
        raise Exception("File not found")


def read_json(path):
    """
    TODO DOCUMENTATION
    :param path:
    :return:
    """
    check_file(path)
    with open(path) as f:
        data = json.load(f)
    return data


def save_json(data, path):
    """
    TODO DOCUMENTATION
    :param data:
    :param path:
    :return:
    """
    with open(path, 'w') as out:
        json.dump(data, out, indent=4, ensure_ascii=False)
    return path


def read_info_file():
    """
    TODO DOCUMENTATION
    :return:
    """
    check_file(info_file)
    return json.load(open(info_file))


def read_config_file():
    """
    TODO DOCUMENTATION
    :return:
    """
    check_file(config_file)
    return read_json(config_file)


# GETS
def get_last_model():
    """
    TODO DOCUMENTATION
    :return:
    """
    return read_info_file()['last_model']


def get_base_model():
    """
    TODO DOCUMENTATION
    :return:
    """
    return read_config_file()['base_model']


def get_test_devel():
    """
    TODO DOCUMENTATION
    :return:
    """
    return read_config_file()['test_devel']


def get_srilm_bin_path():
    """
    TODO DOCUMENTATION
    :return:
    """
    return read_config_file()['srilm_bin_path']


def get_last_model_number():
    """
    TODO DOCUMENTATION
    :return:
    """
    number = "".join(re.findall(r"\d+", get_last_model().split('/')[-1].split('.')[0]))
    if number != "":
        return int(number)
    return 0


# SAVE
def save_last_model(path):
    """
    TODO DOCUMENTATION
    :param path:
    :return:
    """
    dest_path = os.path.join(models_folder, 'model{}.lm'.format(get_last_model_number() + 1))
    shutil.move(path, dest_path)
    info = read_info_file()
    info['last_model'] = dest_path
    save_json(info, info_file)
    return path


def save_response(output_path, files):
    """
    TODO DOCUMENTATION
    :param output_path:
    :param files:
    :return:
    """
    if type(files) is not list:
        files = [files]
    out = []
    for i in files:
        output = os.path.join(output_path, "es.lm")
        shutil.copyfile(i, output)
        out.append(output)

    return out


# CLEAN
def clean_older_models():
    """
    TODO DOCUMENTATION
    :return:
    """
    models = [os.path.join(models_folder, i) for i in os.listdir(models_folder) if re.match(r"model[0-9]*\.lm", i)]
    models.remove(get_last_model())
    for model in models:
        os.remove(model)


def clean_tmp_folder():
    """
    TODO DOCUMENTATION
    :return:
    """
    shutil.rmtree(tmp_folder)


def get_ip():
    """
    TODO DOCUMENTATION
    :return:
    """
    return socket.gethostbyname(socket.gethostname())
