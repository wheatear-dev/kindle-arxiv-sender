import argparse

from utils import main


parser = argparse.ArgumentParser(
    'k2pdfopt.py'
)

parser.add_argument(
    'email_from',
    type=str,
    help=(
        'Your personal gmail address '
        '(from which to send the pdfs).'
    ),
)

parser.add_argument(
    'email_to',
    type=str,
    help=(
        "The kindle's amazon email address "
        '(to which to send the pdfs).'
    ),
)

parser.add_argument(
    'password',
    type=str,
    help='Your SMTP password for gmail.',
)

parser.add_argument(
    'arxiv_ids',
    nargs='+',
    help="The ID's of the requested arXiv papes",
)


if __name__ == '__main__':
    p = parser.parse_args()

    main(
        p.email_from,
        p.email_to,
        p.password,
        p.arxiv_ids
    )
