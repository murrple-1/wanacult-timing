import argparse
import itertools


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("chorus_splits")
    parser.add_argument("speed_up", type=float)
    parser.add_argument("-s", "--start-slow", action="store_true")

    args = parser.parse_args()

    is_slow = args.start_slow

    song_chunks = args.chorus_splits.split(";")

    for song_chunk in song_chunks:
        print(song_chunk)


if __name__ == "__main__":
    main()
