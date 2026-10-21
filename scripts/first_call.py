import sys

from app.llm import ask


def main(argv: str):
    if not argv:
        print(f"missing field to run the app, total arguments provided {len(argv)}", file=sys.stderr)
        print(f"usage: python -m scripts.first_call <Prompt> <cap>;", file=sys.stderr)
        return 1
    ris = ask(argv[0], argv[1])
    if ris.status == "completed":
        print(f"prompt request successful with status {ris.status}, values => {ris}")
        return 0
    #https://developers.openai.com/api/reference/python/resources/responses/methods/create#(resource)%20responses%20%3E%20(method)%20create%20%3E%20(params)%20default.non_streaming%20%3E%20(param)%20max_output_tokens%20%3E%20(schema)
    else:
        print(f"prompt request failed with status {ris.status}, reason is {ris.incomplete_reason}" , file=sys.stderr)
        return 2
    

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
'''
from collections import Counter
import sys
from app.shipment import parse_shipment, Shipment


def main(argv: list[str]):

    try:
        if not argv:
            print(f"missing field to run the app, total arguments provided {len(argv)}", file=sys.stderr)
            print(f"usage: python -m scripts.summary 'ID,WEIGHT_KG,COUNTRY' ['ID,WEIGHT_KG,COUNTRY' ...]", file=sys.stderr)

            return 1
        args: list[Shipment] = [parse_shipment(raw) for raw in argv]
    except ValueError as e:
        print(f"ERROR caught an exception {e}", file=sys.stderr)
        return 2

    #Print count
    print(f"total count of arguments {len(args)}")
    
    #Total weight
    print(f"total weight is {sum(s.weight_kg for s in args):.2f}")
    
    #Print total shipments per country
    print(f"total number of shipments per country are {Counter(s.country for s in args)}")


if __name__ == "__main__":                       # ≈ public static void main
    sys.exit(main(sys.argv[1:]))                 # argv[0] is the script name itself

'''