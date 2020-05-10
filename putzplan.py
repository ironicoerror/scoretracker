#!/usr/bin/python3

MITBEWOHNER = ["Flo", "Laura", "Nico", "Paul", "Raffael", "Tobi"]
def _rotate_dist(tlist, distance):
	"""rotates a list given by the distance if positive forwards if negative backwards and returns it"""
	if distance > 0:
		for _ in range(distance):
			last = tlist.pop()
			tlist.insert(0, last)
	elif distance == 0:
		pass
	else:
		for _ in range(abs(distance)):
			first = tlist.pop(0)
			tlist.append(first)
	return tlist
def main(isocal, weeks):
	"""takes the actual calender date iso calender via datetime.now().date().isocalendar()
	and derives the last cleaning plans given by weeks and returns a list of lists"""
	putzplanliste = []
	y, cw, wd = isocal 
	dist_cw = cw - 19 
	for back_weeks in range(weeks):
		putzplan = ["Küche Do", "Containermüll",\
			 "Garten/Straße", "Küche So",\
			 "allg. Bereiche 2", "allg. Bereiche"]
		putzplanliste.append([str(cw - back_weeks), _rotate_dist(putzplan, dist_cw - back_weeks)])
	return putzplanliste[::-1]
if __name__ == "__main__":
	from datetime import datetime
	print(main(datetime.now().date().isocalendar(), 3))
