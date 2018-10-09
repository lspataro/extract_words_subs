import click
from collections import Counter
from tokenizer import Tokenizer, partition_by_cores


def is_line_valid(line):
    if not line.isdigit() and '->' not in line:
        return True
    return False


def get_tokens(texts):
    tokens = Tokenizer().proc_all_mp(partition_by_cores(texts))
    return tokens


def get_final_words(words, rare_k=None, freq_threshold=None):
    c = Counter(words)
    if rare_k is not None:
        ordered_c = sorted(c.items(), key=lambda x: x[1])
        return [x[0] for x in ordered_c][:int(rare_k)]
    elif freq_threshold is not None:
        a = {item: count for item,count in c.items() if count <= int(freq_threshold)}
        return list(a.keys())
    return list(c.keys())


@click.command()
@click.option('--filename', default='/home/lorenzospataro/subs.srt',
              help="""filename of the srt file""")
@click.option('--rare_k', default=None,
              help="""to retrieve the least frequents k words from the 
              subtitles""")
@click.option('--freq_threshold', default=None,
              help="""to retrieve the words that occur less or equal than this 
              value""")
def extract_words(filename, rare_k, freq_threshold):
    lines = set()
    if (rare_k is not None and freq_threshold is not None) or \
            (rare_k is None and freq_threshold is None):
        raise Exception("specify only one between --rare_k and --freq_threshold")
    with open(filename) as f:
        for index, line in enumerate(f):
            line = line.strip()
            if is_line_valid(line):
                lines.add(line)
    tokens = get_tokens(list(lines))
    words = [word for sublist in tokens for word in sublist if word.isalpha() and len(word) > 1]
    words = get_final_words(words, rare_k=rare_k, freq_threshold=freq_threshold)
    with open(filename.replace('.srt', '.txt'), 'w') as out:
        for index, w in enumerate(words):
            out.write(w)
            if index < len(words) - 1:
                out.write(', ')


if __name__ == '__main__':
    extract_words()