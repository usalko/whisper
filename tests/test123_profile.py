from cProfile import Profile as CProfile
from cProfile import runctx as crunctx
from importlib import machinery
from io import StringIO, open_code
from os import remove
from pathlib import Path
from profile import Profile, runctx
from pstats import Stats
from sys import path
from tempfile import NamedTemporaryFile


def get_statistics(profile: Profile, lines_count: int = -1) -> str:
    '''
    Print statistics to output string
    '''
    str_buffer = StringIO()
    stats = Stats(stream=str_buffer)
    stats.init(profile)
    stats.print_title()
    stats.strip_dirs().sort_stats('calls').print_stats(lines_count).print_callers(lines_count)
    str_buffer.seek(0)
    return '\n'.join(str_buffer.readlines())


def profile_script(input_script_path: str, lines_count: int = -1) -> str:
    '''
    Profiling input script
    '''
    path.insert(0, str(Path(input_script_path).resolve().parent))
    with open_code(input_script_path) as fp:
        code = compile(fp.read(), input_script_path, 'exec')
    spec = machinery.ModuleSpec(name='__main__', loader=None, origin=input_script_path)
    globs = {
        '__spec__': spec,
        '__file__': spec.origin,
        '__name__': spec.name,
        '__package__': None,
        '__cached__': None,
    }

    outfile = ''
    with NamedTemporaryFile(delete=False, prefix=str(Path(input_script_path).name), suffix='.stats') as writer:
        writer.write(bytes('\n', encoding='utf-8'))
        outfile = writer.name
    assert outfile != ''

    try:
        runctx(code, globs, {}, outfile, True) # type: ignore
        str_buffer = StringIO()
        stats = Stats(stream=str_buffer)
        stats.init(outfile)
        stats.print_title()
        stats.strip_dirs().sort_stats('calls').print_stats(lines_count).print_callers(lines_count)
        str_buffer.seek(0)
        return '\n'.join(str_buffer.readlines())
    finally:
        remove(outfile)


def cprofile_script(input_script_path: str, lines_count: int = -1) -> str:
    '''
    cProfiling input script
    '''
    path.insert(0, str(Path(input_script_path).resolve().parent))
    with open_code(input_script_path) as fp:
        code = compile(fp.read(), input_script_path, 'exec')
    spec = machinery.ModuleSpec(name='__main__', loader=None, origin=input_script_path)
    globs = {
        '__spec__': spec,
        '__file__': spec.origin,
        '__name__': spec.name,
        '__package__': None,
        '__cached__': None,
    }

    outfile = ''
    with NamedTemporaryFile(delete=False, prefix=str(Path(input_script_path).name), suffix='.stats') as writer:
        writer.write(bytes('\n', encoding='utf-8'))
        outfile = writer.name
    assert outfile != ''

    try:
        crunctx(code, globs, {}, outfile, True) # type: ignore
        str_buffer = StringIO()
        stats = Stats(stream=str_buffer)
        stats.init(outfile)
        stats.print_title()
        stats.strip_dirs().sort_stats('calls').print_stats(lines_count).print_callers(lines_count)
        str_buffer.seek(0)
        return '\n'.join(str_buffer.readlines())
    finally:
        remove(outfile)


if __name__ == '__main__':
    output = cprofile_script('./tests/test123.py')
    with open('./profer.output.txt', 'w') as writer:
        writer.write(output)
    print(output)