
from pathlib import Path
import graph

score_path = Path("./score")

# keys should not include ':' or '#'
keys = {'LANE', 'GAME', 'NAME', 'PINS', 'SCORE'}


def read_records():
    """kinda prone to an SQL injection style attack."""
    keystore = {key: None for key in keys}
    records = []  # todo use pandas

    with score_path.open() as score_file:
        line = score_file.readline()

        i = 0
        while True:
            line = line.strip()

            # skip whitespace
            if line == "":
                line = score_file.readline()
                if line is "":
                    return records
                continue

            # save record
            if line == '#':
                record = {
                    'i': i
                }
                record.update({  # todo refactor
                    key: keystore[key] for key in keys
                })
                records.append(record)
                i += 1
                line = score_file.readline()
                continue

            # detect keys
            for key in keys:
                prefix = f'{key}:'
                if line.startswith(prefix):
                    mode = key
                    keystore[mode] = None
                    line = line.strip(prefix)
                    break
            else:
                # store key
                if keystore[mode] is None:
                    keystore[mode] = line
                else:
                    if not isinstance(keystore[mode], list):
                        keystore[mode] = [keystore[mode]]
                    keystore[mode].append(line)
                line = score_file.readline()


def validate(record):
    def inter(hit: str):
        if hit == '/':
            raise NotImplemented()
        if hit == '*':
            return 10  # fixme wrong for spare
        assert 0 <= int(hit) < 10
        return int(hit)

    score = record["SCORE"]
    pins = record["PINS"]
    rounds = len(score)

    if rounds == 10:
        assert len(pins) == 21
        if pins[-1] != '0':
            assert pins[18] == '*' or pins[19] == '/'
    else:
        assert len(pins) == rounds * 2

    running_score = 0
    for i in range(rounds):
        assert pins[(i*2) + 1] != '*'
        assert pins[i*2] != '/'

        next_round = (i + 1) * 2
        if pins[i*2] == '*':
            running_score += 10
            if i == 9:
                next_round -= 1
            else:
                assert inter(pins[(i * 2) + 1]) == 0
            if next_round < len(pins):
                running_score += inter(pins[next_round]) + inter(pins[next_round + 1])
        elif pins[(i*2)+1] == '/':
            running_score += 10
            if next_round < len(pins):
                running_score += inter(pins[next_round])
        else:
            running_score += inter(pins[i*2]) + inter(pins[(i*2)+1])

        assert int(score[i]) == running_score


def main():
    records = read_records()
    for record in records:
        validate(record)
    print(records)
    graph.display_bowling_result(records[0]['PINS'])


if __name__ == "__main__":
    main()
