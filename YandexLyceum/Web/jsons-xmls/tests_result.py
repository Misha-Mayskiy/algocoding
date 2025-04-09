import json
import sys


def main():
    with open("scoring.json", "r", encoding="utf-8") as f:
        scoring_data = json.load(f)
    scoring = scoring_data["scoring"]

    verdicts = {}
    for idx, line in enumerate(sys.stdin, start=1):
        verdict = line.strip().lower()
        if verdict:
            verdicts[idx] = verdict

    total_score = 0
    for group in scoring:
        required_tests = group["required_tests"]
        group_points = group["points"]
        points_per_test = group_points // len(required_tests)
        for test_num in required_tests:
            if verdicts.get(test_num, "") == "ok":
                total_score += points_per_test

    print(total_score)


if __name__ == "__main__":
    main()
