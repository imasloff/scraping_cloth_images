import os
from itertools import product


def enumerate_files(dir_path):
    file_list = sorted(os.listdir(dir_path), key=lambda x: int(x.split('_')[0]))
    for idx, f_path in enumerate(file_list, start=1):
        path_list = f_path.split('_')
        name = path_list[1].split('.')[0] if '.' in path_list[1] else path_list[1]
        postfix = path_list[-1].split('.')[-1]
        os.rename(f"{dir_path}/{f_path}", f'{dir_path}/{idx}_{name}.{postfix}')


if __name__ == '__main__':
    for cat, par_dir in product(['dresses', 'lower_body', 'upper_body'], ['cloth', 'person']):
        dir_path = f"shopcider/{cat}/women/{par_dir}"
        enumerate_files(dir_path)
        
