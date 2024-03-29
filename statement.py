import locale


def statement(invoice, plays):
    total_amount = 0
    volume_credits = 0
    result = f"Statement for {invoice['customer']}\n"

    def format(amount):
        locale.setlocale(locale.LC_ALL, "")
        return locale.currency(amount, grouping=True)

    for perf in invoice["performances"]:
        play = plays[perf["playID"]]
        this_amount = 0

        if play["type"] == "tragedy":
            this_amount = 40000
            if perf["audience"] > 30:
                this_amount += 1000 * (perf["audience"] - 30)
        elif play["type"] == "comedy":
            this_amount = 30000
            if perf["audience"] > 20:
                this_amount += 10000 + 500 * (perf["audience"] - 20)
            this_amount += 300 * perf["audience"]
        else:
            raise RuntimeError(f"Unknown type: {play['type']}")

        # Add volume credits
        volume_credits += max(perf["audience"] - 30, 0)
        # Add credit for every ten comedy attendees
        if "comedy" == play["type"]:
            volume_credits += perf["audience"] // 5

        # Print line for this order
        result += f"  {play['name']}: {format(this_amount / 100)} ({perf['audience']} seats)\n"
        total_amount += this_amount

    result += f"Amount owed is {format(total_amount / 100)}\n"
    result += f"You earned {volume_credits} credits\n"
    return result
