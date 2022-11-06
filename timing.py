import argparse
import itertools
import datetime

from pytimeparse.timeparse import timeparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("chorus_splits")
    parser.add_argument("speed_up", type=float)

    args = parser.parse_args()

    song_chunk_totals = [
        float(timeparse(split)) for split in args.chorus_splits.split(",")
    ]

    assert song_chunk_totals == sorted(song_chunk_totals)
    assert len(song_chunk_totals) == len(frozenset(song_chunk_totals))

    song_chunks = []

    song_length_cum = 0.0
    for song_chunk_total in song_chunk_totals:
        song_chunk = song_chunk_total - song_length_cum
        song_chunks.append((song_chunk, song_length_cum))
        song_length_cum += song_chunk

    song_length = song_chunks[-1][0] + song_chunks[-1][1]

    schedule = []

    are_playing_song = False

    for song_chunk, cum_song_chunk in song_chunks:
        if are_playing_song:
            schedule.append((datetime.timedelta(seconds=song_length), True))
        else:
            schedule.append(
                (
                    datetime.timedelta(
                        seconds=(
                            (song_chunk * args.speed_up)
                            - (cum_song_chunk / args.speed_up)
                            - (
                                (song_length - (cum_song_chunk + song_chunk))
                                / args.speed_up
                            )
                        )
                    ),
                    False,
                )
            )

        are_playing_song = not are_playing_song

    for time_of_section, are_playing_song in schedule:
        if are_playing_song:
            print(f"SONG: {time_of_section}")
        else:
            print(f"FUCK AROUND: {time_of_section}")

    print("\ntotal: {}".format(sum((s[0] for s in schedule), datetime.timedelta())))


if __name__ == "__main__":
    main()
