from textnode import *

def main ():
    sample = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(sample)

main()