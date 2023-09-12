from typing import Optional, Callable
from json import load, dump
from os import listdir, mkdir
from os.path import split as splitpath, splitext, isdir, isfile, join as joinpath


def default_on_file_hook(filename, data):
    return data


def main(
    input_directory: str,
    output_directory: str,
    output_filename: str,
    on_file_hook: Optional[Callable] = default_on_file_hook,
    extend_lists: bool = True,
    allow_overwrite: bool = True,
):
    outfile = joinpath(output_directory, output_filename)
    if not isdir(output_directory):
        mkdir(output_directory)
    if not allow_overwrite and isfile():
        raise IOError("Preventing overwrites on " + outfile)

    files = listdir(input_directory)
    jsons = list(filter(lambda fp: splitext(fp)[1].lower() == '.json', files))
    jsons_names = list(map(lambda fp: splitpath(fp)[1], jsons))

    data = []
    def prefix_dir(f): return joinpath(input_directory, f)
    for i, jsp in enumerate(map(prefix_dir, jsons)):
        with open(jsp, "r", encoding="utf8") as fi:
            file_data = load(fi)
        if callable(on_file_hook):
            file_data = on_file_hook(jsons_names[i], file_data)
        if extend_lists and isinstance(file_data, list):
            data.extend(file_data)
        else:
            data.append(file_data)

    with open(outfile, "w", encoding='utf8') as fo:
        dump(data, fo)
    print(f"Merged {len(data)} items")


class Defaults:
    INPUT_DIRECTORY: str = "dist"
    OUTPUT_DIRECTORY: str = "dist/compact"
    OUTPUT_FILENAME: str = "merged.json"
    EXTEND_LISTS: bool = True
    ALLOW_OVERWRITE: bool = True


def mainargs(*args, **kwargs):
    from argparse import ArgumentParser
    parser = ArgumentParser(description="Insert Module CLI description")
    parser.add_argument(
        "-i",
        "--input",
        default=Defaults.INPUT_DIRECTORY,
        dest="input_directory",
        help=f"input directory, default: {Defaults.INPUT_DIRECTORY}",
    )
    parser.add_argument(
        "-d",
        "--output-dir",
        default=Defaults.OUTPUT_DIRECTORY,
        dest="output_directory",
        help=f"output filename, default: {Defaults.OUTPUT_DIRECTORY}",
    )
    parser.add_argument(
        "-o",
        "--output",
        default=Defaults.OUTPUT_FILENAME,
        dest="output_filename",
        help=f"output filename, default: {Defaults.OUTPUT_FILENAME}",
    )
    parser.add_argument(
        "-s",
        "--safe",
        action="store_false",
        dest="allow_overwrite",
        help=f"safe mode prevents overwriting"
    )
    parser.add_argument(
        "-a",
        "--append",
        action="store_false",
        dest="extend_lists",
        help=f"append mode will append each file to the merge instead of extending them"
    )

    _args = parser.parse_args(args)

    return {
        "input_directory": kwargs.get("input_directory", _args.input_directory),
        "output_directory": kwargs.get("output_directory", _args.output_directory),
        "output_filename": kwargs.get("output_filename", _args.output_filename),
        "extend_lists": kwargs.get("extend_lists", _args.extend_lists),
        "allow_overwrite": kwargs.get("allow_overwrite", _args.allow_overwrite),
    }


if __name__ == "__main__":
    import sys
    sys.exit(main(**mainargs(*sys.argv[1:])))
