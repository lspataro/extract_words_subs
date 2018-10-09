# extract_words_subs
Useful tool to extract the least common words from an srt file with the idea of improving english by studying these rare words
#### Install dependencies
```
pipenv install -e .
pipenv shell
```
#### run program
python main.py --filename='/home/user/file.srt' --rare_k=100 --freq_threshold=5

#### arguments
```
--filename is the path of the rst file  
--rare_k is a parameter to retrieve the least frequents k words from the subtitles  
--freq_threshold is a parameter to retrieve all the words that occur less or equal than this value

NOTE: only one of the parameters rare_k and freq_threshold  is accepted
```
