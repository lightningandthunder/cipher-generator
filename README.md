# cipher-generator
A quick and dirty cipher generator for a friend's D&amp;D campaign

This code generates a list of 26 ciphers, each containing every letter of the alphabet.
Moreover, taking the first letter of each cipher generates another cipher which contains the full alphabet,
as does taking the final letter of each cipher.

You end up with 29 pairs of words. The first 26 are assembled dynamically,
each clue being decrypted into the corresponding solution by mapping the matching cipher to the regular alphabet.

The 27th and 28th use the first-letters cipher and last-letters cipher respectively.

The 29th pair uses the first-letters cipher as its cipher, and the last-letters cipher
instead of the regular alphabet as its "base" to decode into.

This is not my best work ever; variable names are somewhat confusing, since this whole script
relies on juggling several different kinds of indexes at the same time, and comparing
similar lists of letters to each other. 
Some issues raise exceptions, and in other cases I just use `assert` (although I think I can justify those as being 2 different use cases).
There's a whole lot of `print`ing, rather than writing to a file.

But still, I'm proud of this due to how difficult it was to solve.