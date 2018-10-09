import re
import os
import spacy
from typing import List, Optional
from concurrent.futures import ProcessPoolExecutor
os.system("python -m spacy download en")


def partition_by_cores(a):
    return partition(a, len(a) // num_cpus() + 1)


def partition(a, size):
    """splits iterables a in equal parts of size sz"""
    return [a[i:i + size] for i in range(0, len(a), size)]


def num_cpus() -> int:
    try:
        return len(os.sched_getaffinity(0))
    except AttributeError:
        cpu_count = os.cpu_count()
        if cpu_count is None:
            return 1
        else:
            return cpu_count


class Tokenizer:
    def __init__(self, lang: str = 'en') -> None:
        self.tokens = spacy.load(lang)
        for w in ('<eos>', '<bos>', '<unk>'):
            self.tokens.tokenizer.add_special_case(w, [{
                spacy.symbols.ORTH: w
            }])

    @staticmethod
    def replace_repeated_character(match) -> str:
        TK_REP = 'tk_rep'
        character, count = match.groups()
        return f' {TK_REP} {len(count)+1} {character} '

    @staticmethod
    def replace_repeated_word(match) -> str:
        TK_WREP = 'tk_wrep'
        word, count = match.groups()
        return f' {TK_WREP} {len(count.split())+1} {word} '

    @staticmethod
    def replace_caps_lock(text: str) -> str:
        TOK_UP = ' t_up '
        res: List[str] = []
        for word in re.findall(r'\w+|\W+', text):
            if word.isupper() and len(word) > 2:
                res += [TOK_UP, word.lower()]
            else:
                res += [word.lower()]
        return ''.join(res)

    def replace_br(self, string: str) -> str:
        re_br = re.compile(r'<\s*br\s*/?>', re.IGNORECASE)
        return re_br.sub("\n", string)

    def spacy_tokens(self, string: str) -> List[str]:
        return [t.text for t in self.tokens.tokenizer(self.replace_br(string))]

    re_repeated_character = re.compile(r'(\S)(\1{3,})')
    re_repeated_word = re.compile(r'(\b\w+\W+)(\1{3,})')


    def proc_text(self, text: str) -> List[str]:
        text = self.re_repeated_character.sub(
            Tokenizer.replace_repeated_character, text)
        text = self.re_repeated_word.sub(Tokenizer.replace_repeated_word, text)
        text = Tokenizer.replace_caps_lock(text)
        text = re.sub(r'([/#])', r' \1 ', text)
        text = re.sub(' {2,}', ' ', text)
        return self.spacy_tokens(text)

    @staticmethod
    def proc_all(texts: List[str], lang: str) -> List[List[str]]:
        tok = Tokenizer(lang)
        return [tok.proc_text(text) for text in texts]

    @staticmethod
    def proc_all_mp(texts: List[List[str]],
                    lang: str = 'en',
                    ncpus: Optional[int] = None):
        ncpus = ncpus or num_cpus() // 2
        with ProcessPoolExecutor(ncpus) as e:
            return sum(
                e.map(Tokenizer.proc_all, texts, [lang] * len(texts)), [])