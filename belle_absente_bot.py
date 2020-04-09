import argparse
from typing import Dict, List
import glob

# Default alphabet is missing j, q, z (the 3 most infrequently used letters in English)
# in accordance with Georges Perec's approach to the Belle Absente
DEFAULT_ALPHABET = 'abcdefghiklmnoprstuvwxy'


def is_pangrammatic_lipogram(alphabet: str, fragment: str, lipogram_letter: str) -> bool:
    """
    Returns whether a text fragment is a pangrammatic lipogram.
    A pangrammatic lipogram is a text fragment that contains every letter of the alphabet except one (the lipogram letter).
    -- alphabet | characters whose presence in full constitutes a pangram
    -- fragment | the text fragment to examine
    -- lipogram_letter | letter to be excluded from pangram
    """

    # Lowercase the fragment.
    fragment = fragment.lower()

    # Remove non-alphabetic chars from the fragment.
    fragment = ''.join(char for char in fragment if 'a' <= char <= 'z')

    for letter in lipogram_letter:
        if letter not in alphabet:
            alphabet += letter

    if (set(alphabet) - set(fragment)) == set(lipogram_letter):
        return True
    else:
        return False

def extract_sentences_from_file(file: str) -> List[str]:
    try:
        with open (file, "r") as f:
            s = f.read()
    except UnicodeDecodeError:
        # ISO-8859-1 encoding is found in a lot of Project Gutenberg files.
        with open (file, "r", encoding='ISO-8859-1') as f:
            s = f.read().replace('\n', '')
    sentences = s.split('.')
    return sentences

def get_files_to_search(file: str, directory: str) -> List[str]:
    # Support users seaching a single file or all files in a directory.
    files_to_search = []
    if file:
        files_to_search.append(file)
        return files_to_search
    path = args.directory + '*'
    for f in glob.glob(path):
        if '.txt' in f:
            files_to_search.append(f)
        else:
            print(f'Skipping file {f} because it is not a .txt file.')
    return files_to_search

def get_lipogram_letters(lipogram_letter: str, belle_absente_letters: str) -> List[str]:
    # Support users specifying a single lipogram letter or multiple (as part of a Belle Absente).
    lipogram_letters = []
    if lipogram_letter:
        lipogram_letters.append(args.lipogram_letter)
    if belle_absente_letters:
        for letter in belle_absente_letters:
            lipogram_letters.append(letter)
    return lipogram_letters

def print_results(results_map: Dict[str, Dict[str, List[str]]], lipogram_letters: str) -> None:
    poetic_form = 'Belle Absentes' if len(lipogram_letters) > 1 else 'lipograms'
    print(f'Done searching for {poetic_form}.')
    if results_map.keys():
        print(f'Found {poetic_form} in the following files:')
        print(results_map.keys())
        print(f'\nPrinting {poetic_form} for each file...')
    else:
        print(f'Could not find any {poetic_form} for that letter combination. Please try again with different or fewer letters.')

    for file in results_map.keys():
        print(f'\n{poetic_form} for file: {file}')
        results_for_file = results_map[file]
        for letter in lipogram_letters:
            print(f'\nFound {len(results_for_file[letter])} pangrammatic lipograms for letter {letter}:')
            for index, fragment in enumerate(results_for_file[letter]):
                number = index + 1
                print(f'\n{number}. {fragment}')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Find pangrammatic lipograms.')
    parser.add_argument('-a', '-alphabet', dest="alphabet", action="store", default=DEFAULT_ALPHABET, type=str)
    parser.add_argument('-l', '-lipogram', dest="lipogram_letter", action="store", default='', type=str)
    parser.add_argument('-f', '-file', dest="file", action="store", default='', type=str)
    parser.add_argument('-d', '-directory', dest="directory", action="store", default='', type=str)
    parser.add_argument('-b', '-belle_absente', dest="belle_absente_letters", action="store", default='', type=str)
    args = parser.parse_args()

    lipogram_letters: List[str] = get_lipogram_letters(
        lipogram_letter=args.lipogram_letter,
        belle_absente_letters=args.belle_absente_letters,
    )

    """
    Initialize map of file name to {lipogram_letter, List[text_fragment]}. i.e.
    {
        'anna_karenina.txt' : {
            'b': ['Kutuzov only replied that movements arranged from a distance were always difficult to execute.'],
        }
    }
    """
    results_map: Dict[str, Dict[str, List[str]]] = {}

    print('Processing files...')

    files_to_search: List[str] = get_files_to_search(file=args.file, directory=args.directory)

    print('Searching files...')

    # Search every sentence in every file to build a list of pangrammatic lipograms for each file.
    for file in files_to_search:
        results_map[file] = {}
        fragments = extract_sentences_from_file(file)
        for i in range(0, len(fragments)):
            fragment = fragments[i]
            for letter in lipogram_letters:
                if is_pangrammatic_lipogram(alphabet=args.alphabet, fragment=fragment, lipogram_letter=letter):
                    results_for_file = results_map[file]
                    if results_for_file.get(letter):
                        # List of fragments for this letter already existr. Add to it.
                        results_for_file[letter].append(fragment)
                    else:
                        # Create a new list of fragments for this letter.
                        results_for_file[letter] = [fragment]

    # Filter files from the results list if they do not contain a Belle Absente
    # (i.e. they contain pangrammatic lipograms for some, but not all, of the ligogram letters.)
    filtered_results_map: Dict[str, Dict[str, List[str]]] = {}
    for file in results_map.keys():
        results_for_file = results_map[file]
        has_belle_absente = all(results_for_file.get(letter) for letter in lipogram_letters)
        if has_belle_absente:
            filtered_results_map[file] = results_map[file]

    print_results(results_map=filtered_results_map, lipogram_letters=lipogram_letters)
