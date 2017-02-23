#!/usr/bin/python3
from app import App


def main():
    app = App("tests/me_at_the_zoo.in")
    # app = App("videos_worth_spreading.in")
    # app = App("trending_today.in")
    # app = App("kittens.in")

    app.sortEdges()
    app.solveAllEdges()
    print(app.generateOutput())


if __name__ == '__main__':
    main()
