class Line:
	def __init__(self, m, b):
		self.m = m
		self.b = b
		for i in range(3):
			print(i)

		self.count = 0

	def get_y(self, x):
		self.count += 1
		return self.m * x + self.b

	def set_slope(self, m):
		self.m = m

	def get_count(self):
		return self.count

	def height_difference(self, x, x2):
		self.count -= 1
		return self.get_y(x) - self.get_y(x2)


def main():
	firstLine = Line(1, 1)
	secondLine = Line(3, 10)
	print(type(firstLine))
	print(firstLine.get_y(3))
	print(secondLine.get_y(3))
	secondLine.set_slope(4)
	print(secondLine.get_y(3))

	print(secondLine.get_count())


if __name__ == '__main__':
	main()