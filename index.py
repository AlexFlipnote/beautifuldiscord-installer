import sys

from utils import app as beautifuldiscord

if not sys.argv[1:]:
    print("Nothing...")
else:
    beautifuldiscord.main(
        " ".join(sys.argv[1:])
    )
