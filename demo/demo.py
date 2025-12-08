if __name__ == "__main__":
    import sys

    sys.path.insert(0, ".")


from demo.demo_09 import demo

if __name__ == "__main__":
    # TODO: docx, html - demo_03
    demo("html")
    demo("xlsx")
    demo("docx")
    demo("pdf")
