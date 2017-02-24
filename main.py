#!/usr/bin/python3
from app import App


def main():
    inputs = [
        "tests/me_at_the_zoo.in",
        "tests/videos_worth_spreading.in",
        "tests/trending_today.in",
        "tests/kittens.in"
    ]

    app = App(inputs[2])

    app.sortEdges()
    app.solveAllEdges()
    print(app.generateOutput())


if __name__ == '__main__':
    main()
