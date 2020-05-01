from Analyzer import Analyzer


def main():
    text = open('tt.txt').read()
    Analyzer(text, 'output')


if __name__ == '__main__':
    main()


