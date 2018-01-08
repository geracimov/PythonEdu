import ast
import os
import collections

from nltk import pos_tag


def get_all_names(tree):
    return [node.id for node in ast.walk(tree) if isinstance(node, ast.Name)]


def get_all_words_in_path(_path):
    trees = [t for t in get_trees(_path) if t]
    function_names = [f for f in flat([get_all_names(t) for t in trees]) if
                      not (f.startswith('__') and f.endswith('__'))]

    def split_snake_case_name_to_words(name):
        return [n for n in name.split('_') if n]

    return flat([split_snake_case_name_to_words(function_name) for function_name in function_names])


def get_top_functions_names_in_path(_path, _top_size=10):
    t = get_trees(_path)
    nms = [f for f in
           flat([[node.name.lower() for node in ast.walk(t) if isinstance(node, ast.FunctionDef)] for t in t]) if
           not (f.startswith('__') and f.endswith('__'))]
    return collections.Counter(nms).most_common(_top_size)


def is_verb(_word):
    if not _word:
        return False
    pos_info = pos_tag([_word])
    return pos_info[0][1] == 'VB'


def flat(_list):
    """ [(1,2), (3,4)] -> [1, 2, 3, 4]"""
    return sum([list(item) for item in _list], [])


def get_trees(_path, with_filenames=False, with_file_content=False):
    filenames = []
    trees = []
    _path = Path if _path is None else _path
    for dirname, dirs, files in os.walk(_path, topdown=True):
        files_gen = (file for file in files if file.endswith('.py'))
        for file in list(files_gen)[0:101]:
            filenames.append(os.path.join(dirname, file))
    print('total %s files' % len(filenames))

    for filename in filenames:
        with open(filename, 'r', encoding='utf-8') as attempt_handler:
            main_file_content = attempt_handler.read()
        try:
            tree = ast.parse(main_file_content)
        except SyntaxError as e:
            print(e)
            tree = None

        if with_filenames:
            if with_file_content:
                trees.append((filename, main_file_content, tree))
            else:
                trees.append((filename, tree))
        else:
            trees.append(tree)
    print('trees generated')
    return trees


def get_verbs_from_function_name(function_name):
    return [_word for _word in function_name.split('_') if is_verb(_word)]


def get_top_verbs_in_path(_path, _top_size=10):
    global Path
    Path = _path
    trees = [t for t in get_trees(None) if t]
    fncs = [f for f in get_functions_in_trees(trees) if not (f.startswith('__') and f.endswith('__'))]
    print('functions extracted')
    verbs = flat([get_verbs_from_function_name(function_name) for function_name in fncs])
    return collections.Counter(verbs).most_common(_top_size)


def get_functions_in_trees(_trees):
    def get_functions_in_tree(_tree):
        return [node.name.lower() for node in ast.walk(_tree) if isinstance(node, ast.FunctionDef)]

    return flat([get_functions_in_tree(tree) for tree in _trees])


Path = ''
wds = []
projects = [
    'django',
    'flask',
    'pyramid',
    'reddit',
    'requests',
    'sqlalchemy',
]
for project in projects:
    path = os.path.join('.', project)
    wds += get_top_verbs_in_path(path)

top_size = 200
print('total %s words, %s unique' % (len(wds), len(set(wds))))
for word, occurence in collections.Counter(wds).most_common(top_size):
    print(word, occurence)
