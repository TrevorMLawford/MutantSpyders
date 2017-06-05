# Check whether these two recs have collided
def collision(x1, y1, x1w, y1h, x2, y2, x2w, y2h):
	if x2>x1+x1w or x2+x2w<x1 or y2>y1+y1h or y2+y2h<y1:
		return False
	else:
		return True
