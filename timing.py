import argparse
import itertools
import datetime

from pytimeparse.timeparse import timeparse


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("chorus_splits")
    parser.add_argument("speed_up", type=float)
    parser.add_argument("-s", "--start-slow", action="store_true")
    parser.add_argument("-c", "--start-chorus", action="store_true")

    args = parser.parse_args()

    is_slow = args.start_slow

    song_chunk_totals = [float(timeparse(split)) for split in args.chorus_splits.split(",")]

    assert song_chunk_totals == sorted(song_chunk_totals)

    song_chunks = []

    previous_song_chunk = 0.0
    for song_chunk_total in song_chunk_totals:
        song_chunk = song_chunk_total - previous_song_chunk
        song_chunks.append(song_chunk)
        previous_song_chunk = song_chunk

    at_speed_song_chunks = []

    for song_chunk in song_chunks:
        if is_slow:
            at_speed_song_chunks.append((datetime.timedelta(seconds=song_chunk), is_slow))
        else:
            at_speed_song_chunks.append((datetime.timedelta(seconds=song_chunk * args.speed_up), is_slow))

        is_slow = not is_slow
    
    for seconds, is_slow in at_speed_song_chunks:
        if is_slow:
            print(f"SLOW: {seconds}")
        else:
            print(f"FAST: {seconds}")

    print("\ntotal: {}".format(sum((sc[0] for sc in at_speed_song_chunks), datetime.timedelta())))


if __name__ == "__main__":
    main()
