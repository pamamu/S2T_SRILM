from ContainerHandler import ContainerHandler
import Pyro4

from utils.IO import read_json, save_last_model, save_response, get_last_model
from utils.srilm import generate_model, improve_model, split_data


@Pyro4.expose
class SRILMHandler(ContainerHandler):
    def __init__(self, container_name, main_uri):
        super(SRILMHandler, self).__init__(container_name, main_uri)

    def run(self, **kwargs):
        if 'input_json' in kwargs and 'output_folder' in kwargs:
            print("Container {}: Runned with {}".format(self.container_name, kwargs))
            self.running = True
            result = self.generate_lm(kwargs['input_json'], kwargs['output_folder'])
            self.running = False
            return result
        else:
            raise TypeError('input_json and output_folder required')

    def info(self):
        pass

    def generate_lm(self, input_json, output_folder):
        json_info = read_json(input_json)
        input_sentences_path = json_info['sentences_path']

        sentences_path, test_path = split_data(input_sentences_path)

        dic_path = json_info['dic_path']

        new_model = generate_model(sentences_path, dic_path)
        better_model = improve_model(new_model, test_path)

        save_last_model(better_model)

        return save_response(output_folder, get_last_model())


if __name__ == '__main__':
    handler = SRILMHandler('SRILM', 'PYRO:MainController@localhost:4040')
    print(handler.run(input_json='resources/tmp/input.json', output_folder='/srv/shared_folder'))
