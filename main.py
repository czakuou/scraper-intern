

def read_file(path):
    for row in open(path):
        yield row.strip()


    # with open(path, 'r') as f:
    #     keywords_list = f.readlines()
    #     for i, row in enumerate(keywords_list):
    #         row = row.replace('\n', '')
    #         keywords_list[i] = row
    #
    # return keywords_list






def main():
    for keyword in read_file('keywords.txt'):
        print(keyword)

    # print(read_file('keywords.txt'))



if __name__ == '__main__':
    main()

