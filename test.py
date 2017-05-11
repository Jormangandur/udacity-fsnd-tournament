import tournament

l = tournament.swissPairings()
result = []

for p1, p2 in zip(l[0::2], l[1::2]):
    result.append((p1[0], p1[1], p2[0], p2[1]))

print zip(l[0::2], l[1::2])
