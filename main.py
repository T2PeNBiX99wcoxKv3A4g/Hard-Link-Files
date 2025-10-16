import os

import typer
from icecream import ic

app = typer.Typer()


class NotAFolderException(Exception):
    pass


reference_files: list[str] = []


def debug_output_control(debug: bool):
    if debug:
        ic.enable()
    else:
        ic.disable()


def create_hard_link_files(reference_folder_path: str, source_folder_path: str, link_folder_path: str,
                           replace2: bool = False):
    if not os.path.isdir(reference_folder_path):
        raise NotAFolderException(f"Reference path need to be folder.")
    if not os.path.isdir(source_folder_path):
        raise NotAFolderException(f"Source path need to be folder.")
    if not os.path.isdir(link_folder_path):
        raise NotAFolderException(f"Link path need to be folder.")
    for _, _, files in os.walk(reference_folder_path):
        for file in files:
            ic(file)
            reference_files.append(file)

    for file in reference_files:
        source_path = ic(os.path.join(source_folder_path, file))
        link_path = ic(os.path.join(link_folder_path, file))
        if not os.path.isfile(source_path):
            typer.echo(f"File {source_path} not found. skipping...")
            continue
        if os.path.isfile(link_path):
            if replace2:
                os.remove(link_path)
            else:
                typer.echo(f"File {link_path} already exists. skipping...")
                continue
        os.link(source_path, link_path)
        typer.echo(f"{source_path} -> {link_path}")


@app.command()
def reference(reference_folder_path: str, source_folder_path: str, link_folder_path: str, debug: bool = False):
    debug_output_control(debug)
    create_hard_link_files(reference_folder_path, source_folder_path, link_folder_path)


@app.command()
def replace(source_folder_path: str, link_folder_path: str, debug: bool = False):
    debug_output_control(debug)
    create_hard_link_files(link_folder_path, source_folder_path, link_folder_path, True)


if __name__ == '__main__':
    app()
