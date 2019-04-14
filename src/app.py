import os.path
import sys
import time

from SRILM_handler import SRILMHandler


def get_main_server(folder):
    """
    TODO DOCUMENTATION
    :param folder:
    :return:
    """
    file_path = os.path.join(folder, "server.info")
    print('Waiting for master ip ...', end='')
    sys.stdout.flush()
    count = 0
    while not os.path.isfile(file_path) and count < 20:
        print('.', end='')
        sys.stdout.flush()
        time.sleep(1)
        count += 1

    if count == 20:
        print("KO")
        raise Exception('Server IP file not found')
    print(" OK")

    return open(file_path, 'r').readline()


if __name__ == '__main__':
    try:
        if len(sys.argv) < 3:
            print("Insert container name + shared folder")
            sys.exit(1)

        args = sys.argv
        print(args)

        container_name = args[1]
        shared_folder = args[2]

        if not os.path.isdir(shared_folder):
            raise IOError("Shared folder doesn't exist")

        main_server_uri = get_main_server(shared_folder)

        handler = SRILMHandler(container_name, main_server_uri)
        handler.register()
        handler.start()

    except Exception as e:
        print(e)
        sys.exit(3)
    finally:
        if 'handler' in locals():
            handler.stop()
