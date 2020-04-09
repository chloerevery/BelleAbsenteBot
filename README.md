# Belle Absente Bot
Generate Belle Absente poems from works of literature! Can also be used to find naturally-occurring [lipograms](https://en.wikipedia.org/wiki/Lipogram).

## What is a Belle Absente?

**Belle Absente**: A poetic form developed by members of a [French collective of mathematician-poets](https://poets.org/text/brief-guide-oulipo) in the 1960s.

In a Belle Absente poem, each line is a **pangrammatic lipogram** (it contains every letter of the alphabet except for one). Together, the missing letters in each line spell out a person's name or initials.

As a form, the Belle Absente - which translates roughly to "Beautiful Outlaw" - plays with notions of loss, longing, and constraint. Taken line-by-line, the absence of a letter is rarely noticable. But as the reader progresses through the poem, the cumulative effect of the missing letters becomes increasingly visible.

## What is the Belle Absente Bot?

This program searches one or more input text files for sentences that are pangrammatic lipograms (the building blocks of a Belle Absente). It can also be used to search for sentences that are *just lipograms* (specify the `lipogram` flag instead of the `belle_absente` flag).

### Arguments ###

| Flag Name        | Description           | Notes  |
| ------------- |:-------------:| -----:|
| `directory`      | Directory to search for Belle Absentes | Must specify either `directory` or `file` |
| `file`     | Single file to search for Belle Absentes      | Must specify either `directory` or `file` |
| `alphabet` | Letters whose presence in a sentence constitutes a pangram     |    Defaults to `'abcdefghiklmnoprstuvwxy'`<sup>1</sup> |
| `lipogram` | Letter to be avoided     |    Must specify either `lipogram` (find lipograms) or `belle_absente` (find pangrammatic lipograms) |
| `belle_absente` | Letters to avoid (using Belle Absente formula)     |    Must specify either `lipogram` (find lipograms) or `belle_absente` (find pangrammatic lipograms)


<sup>1</sup> The default alphabet is missing j, q, z (the 3 most infrequently used letters in the English language), in accordance with [Georges Perec's](https://en.wikipedia.org/wiki/Georges_Perec) approach to the Belle Absente. This accommodation results in better poetry.

### Output ###

A text file containing:
1. A list of files (if directory was specified) that contain a Belle Absente
2. A per-file breakdown of every pangrammatic lipogram for each of the Belle Absente letters

## Installation


```bash
git clone https://github.com/chloerevery/BelleAbsenteBot.git
```

## Example Usage

Make a Belle Absente for Ruth Bader Ginsburg using contents of the `/books` directory:

```bash
python3 belle_absente_bot.py -directory books/ -belle_absente rgb
```

Make a Belle Absente for Ruth Bader Ginsburg using the text of Don Quixote:

```bash
python3 belle_absente_bot.py -file books/quixote.txt -belle_absente rgb
```

Find lipograms missing the letter J in Les Miserables:

```bash
python3 belle_absente_bot.py -file books/miz.txt -lipogram j
```

Make a Belle Absente for Jean Valjean using the text of Les Miserables:

```bash
python3 belle_absente_bot.py -file books/miz.txt -belle_absente jvj
```

## License
[MIT](https://choosealicense.com/licenses/mit/)