import pickle

if __name__ == "__main__":
    variants = {}
    find_query = {}
    cnt = 0
    with open("2+2+3lem.txt", 'r') as lemma:
        for line in lemma:
            cnt += 1
            head_word = line.split("    ")[0].strip()
            related_word_list = line.split("    ")[-1].split(", ")
            variants[head_word] = related_word_list
            find_query[head_word] = head_word
            for related_word in related_word_list:
                find_query[related_word.strip()] = head_word
            print("\r{0:5}/34336".format(cnt), end="")
    with open("variants.pkl", "wb") as variants_file:
        pickle.dump(variants, variants_file)
    with open("find_query.pkl", "wb") as find_query_file:
        pickle.dump(find_query, find_query_file)
