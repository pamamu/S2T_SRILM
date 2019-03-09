import os.path
import subprocess

from utils.IO import check_file, get_srilm_bin_path, tmp_folder, get_last_model, get_base_model, get_test_devel


def split_data(sentences_path):
    """
    TODO DOCUMENTATION
    :param sentences_path:
    :return:
    """
    check_file(sentences_path)

    file = open(sentences_path)

    lines = file.readlines()

    file.close()

    test_sentences_sum = int(len(lines) * get_test_devel() / 100)

    sentences_out_path = os.path.join(tmp_folder, 'senteces.txt')
    test_out_path = os.path.join(tmp_folder, 'senteces_tests.txt')

    sentences_out = open(sentences_out_path, 'w')
    for sentence in lines[test_sentences_sum:]:
        sentences_out.write(sentence)
    sentences_out.close()

    test_out = open(test_out_path, 'w')
    for sentence in lines[:test_sentences_sum]:
        test_out.write(sentence)
    test_out.close()

    return sentences_out_path, test_out_path


def generate_model(sentences_path, dic_path):
    """
    TODO DOCUMENTATION
    :param dic_path:
    :param sentences:
    :return:
    """
    check_file(sentences_path)
    check_file(dic_path)
    command = os.path.join(get_srilm_bin_path(), 'ngram-count')
    out_model = os.path.join(tmp_folder, 'model.lm')

    script = [command, '-text', sentences_path, '-lm', out_model, '-kndiscount', '-vocab', dic_path]

    p = subprocess.call(script)

    if p != 0:
        script += ['-order', '2']
        p = subprocess.call(script)
        if p != 0:
            raise Exception('Error in language model generation')

    return out_model


def improve_model(model_path, test_file):
    """
    TODO DOCUMENTATION
    :param test_file:
    :param model_path:
    :return:
    """

    check_file(model_path)

    # MASTER MODEL
    command = os.path.join(get_srilm_bin_path(), 'ngram')

    last_model = get_last_model()
    if last_model == '':
        last_model = get_base_model()

    script = [command, '-lm', last_model, '-ppl', test_file, '-debug', str(2)]
    master_test_path = os.path.join(tmp_folder, 'master_test.ppl')
    master_test = open(master_test_path, 'w')

    p = subprocess.call(script, stdout=master_test)

    master_test.close()

    if p != 0:
        raise Exception('Error in improving model')

    # SLAVE MODEL
    script = [command, '-lm', model_path, '-ppl', test_file, '-debug', str(2)]
    slave_test_path = os.path.join(tmp_folder, 'slave_test.ppl')
    slave_test = open(slave_test_path, 'w')

    p = subprocess.call(script, stdout=slave_test)

    slave_test.close()

    if p != 0:
        raise Exception('Error in improving model')

    # LAMBDA CALC
    command = os.path.join(get_srilm_bin_path(), 'compute-best-mix')
    script = [command, slave_test_path, master_test_path]

    p = subprocess.Popen(script, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    a = p.wait()

    if a != 0:
        raise Exception('Error in mixing model')

    output = p.stdout.read().decode('utf8')
    lambda_value = output.split('\n')[-2].split()[-1][:-1]
    print(output)

    # MIX MODELS
    command = os.path.join(get_srilm_bin_path(), 'ngram')
    output_model = os.path.join(tmp_folder, 'out.lm')
    script = [command, '-lm', last_model, '-mix-lm', model_path, '-lambda', lambda_value, '-write-lm', output_model]

    p = subprocess.call(script)

    if p != 0:
        raise Exception('Error in improving model')

    return output_model
