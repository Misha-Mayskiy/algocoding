import argparse


def main():
    parser = argparse.ArgumentParser(description='P&L Calculator')

    parser.add_argument('--per-day', type=float, default=0, help='Income/expense per day')
    parser.add_argument('--per-week', type=float, default=0, help='Income/expense per week')
    parser.add_argument('--per-month', type=float, default=0, help='Income/expense per month')
    parser.add_argument('--per-year', type=float, default=0, help='Income/expense per year')
    parser.add_argument('--get-by', choices=['day', 'month', 'year'], default='day',
                        help='Period for calculation (day, month, year)')

    args = parser.parse_args()

    per_day_total = (
            args.per_day +
            args.per_week / 7 +
            args.per_month / 30 +
            args.per_year / 360
    )

    if args.get_by == 'day':
        total = per_day_total
    elif args.get_by == 'month':
        total = per_day_total * 30
    elif args.get_by == 'year':
        total = per_day_total * 360

    print(int(total))


if __name__ == "__main__":
    main()
