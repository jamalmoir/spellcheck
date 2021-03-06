import re, string, math

class Hashtable():
    """A hash table for storing and checking the existence of keys."""

    def  __init__(self, size):
        """Initiate hashtable with a size and list of empty keys."""
        self.keys = [None] * size
        self.size = size
        self.count = 0
        self.load_factor = 0

    def _generate_hash(self, key):
        """Generate the hash for the given key."""

        '''
        # ASCII product
        hash_num = 1;

        for char in key:
            hash_num *= ord(char)

        return hash_num % self.size
        '''

        # djb2 - http://www.cse.yorku.ca/~oz/hash.html
        hash_num = 5381

        for char in key:
            hash_num = hash_num * 33 + ord(char)

        return hash_num % self.size

    def _generate_hash2(self, key):
        """Generate the (secondary) hash for the given key."""
        hash_num = 5209 #3517

        for char in key:
            hash_num *= ord(char)

        return hash_num % self.size

    def probe(self, key):
        """Find the index where a key can be inserted or return False if found."""
        i = self._generate_hash(key)
        probes = 0

        while True:
            probes += 1

            if self.keys[i] == key:
                return (False, probes)

            if self.keys[i] is None or probes >= self.size: break

            # linear probing
            #i = (i + 1) % self.size

            # quadratic probing
            #i = (i + i**2) % self.size

            # double hashing
            i = (i + self._generate_hash2(key)) % self.size

        return (i, probes)

    def insert(self, key):
        """Insert a new key into the hashtable."""
        i, probes = self.probe(key)

        if i is not None:
            self.keys[i] = key
            self.count += 1
            self.load_factor = self.count / self.size

        return (i, probes)

    def exists(self, key):
        """Find out if a key is present in the hash table."""
        i, probes = self.probe(key)
        exists = True if i is False else False

        return (exists, probes)


def load_txt(path):
    """Load words from the specified txt file into an array."""
    words = []

    with open(path, 'r') as f:
        for line in f:
            words.extend(line.split())

    return words


def clean_txt(strings):
    """Remove punctuation from strings in a list and convert to lowercase."""
    punctuation_re = re.compile('[{}]'.format(re.escape(string.punctuation)))
    empty_re = re.compile(r'[\s]+')
    cleaned_strs= []

    for s in strings:
        cleaned = punctuation_re.sub('', s).lower()

        if cleaned:
            cleaned_strs.append(cleaned)

    return cleaned_strs


def spellcheck(dictionary, text, reporting=False):
    """Print any words from text that are not in dictionary."""
    dict_words = clean_txt(load_txt(dictionary))
    text_words = clean_txt(load_txt(text))
    hashtable = Hashtable(int(len(dict_words) * 2))
    found = [0, 0] # Total found, aggregate found probes
    not_found = [0, 0] # Total not found, aggregate not found probes

    for word in dict_words:
        hashtable.insert(word)

    for word in text_words:
        exists = hashtable.exists(word)

        if not exists[0]:
            if reporting:
                not_found[0] += 1
                not_found[1] += exists[1]

            print("Word not found: '{}'".format(word))

        elif reporting:
            found[0] += 1
            found[1] += exists[1]

    if reporting:
        print("Load factor: {}".format(hashtable.load_factor))
        print("Average found probes: {}".format(found[1] / found[0]))
        print("Average not found probes: {}".format(not_found[1] / not_found[0]))
        print("Average probes {}".format((found[1] + not_found[1]) / (found[0] + not_found[0])))


if __name__ == '__main__':
    spellcheck('dictionary.txt', 'test.txt', reporting=True)

