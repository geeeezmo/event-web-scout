__spec__ = "test_utils"

import random
import string
import subprocess


def install_dependencies(editable_dependencies: list[str], dependencies: list[str] = None) -> list[int]:
    if dependencies is None:
        dependencies = list()
    return_codes = []
    # Install the dependencies using pip
    for dependency in dependencies:
        print(f'installing dependency: {dependency}')
        return_codes.append(subprocess.run(['pip3', 'install', dependency]).returncode)

    # Install editable dependencies using pip
    for dependency in ['.'] + editable_dependencies:
        print(f'installing editable dependency: {dependency}')
        return_codes.append(subprocess.run(['pip3', 'install', '-e', dependency]).returncode)

    return return_codes

    # Clean up (optional): Uninstall the dependencies, if needed
    # if clean_up:
    #     for dependency in dependencies + editable_dependencies:
    #         print(f'uninstalling dependency: {dependency}')
    #         subprocess.run(['pip3', 'uninstall', '-y', dependency])


def random_string(min_length: int = 3, max_length: int = 10):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(random.randint(min_length, max_length)))
