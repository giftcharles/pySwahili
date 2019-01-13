import codecs

letters = ["b", "ch", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "r", "s", "t", "v", "w", "y", "bw",
 "dh", "sh", "ny", "nz", "sw", "mb", "ms", "mz", "ng'", "ky", "kw", "mch", "md", "nd", "fy", "by", "ly", "mw", "my",
  "th", "tw", "vy", "z", "zw"]

vowels = ["a", "e", "i", "o", "u"]

combo = list()

for letter in letters:
    for vowel in vowels:
        combo.append(letter + vowel)

print(len(combo) * 3)
		
with codecs.open('letters.txt', 'w+', 'utf-8') as f:
    for wyb in combo:
        f.write(wyb + "\n")

print("done")
input("end...")
