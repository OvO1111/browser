import sys

ls = list()
alpha = 0.85

for line in sys.stdin:
	result = {'name': list(), 'PageRank': list(), 'links': list()}
	line.strip()
	words = line.split()
	result['name'] = int(words.pop(0))
	result['PageRank'] = float(words.pop(0))
	for li in words:
		result['links'].append(int(li))
	ls.append(result)

for result in ls:
	result['PageRank'] = (1-alpha)/len(ls)
	for ri in ls:
		if result['name'] in ri['link']:
			n = len(ri['link'])
			ave = alpha*ri['PageRank']/n
			result['PageRank'] += ave

for i in ls:
	print(i['name'], '\t', round(i['PageRank'], 4), '\t')
	for x in i['links']:
		print(x)
	print()

