import numpy


a = numpy.array([[0.3, 0.7]])
b = numpy.array([[0.1, 0.1, 0.8], [0.4, 0.5, 0.1]])
c = numpy.array([[0.3, 0.7], [0.3, 0.7], [0.4, 0.6]])

# print(a)
# print(b)
# print(c)


product_a_b = numpy.dot(a, b)
product_a_b_c = numpy.dot(product_a_b, c)
#
#
print(product_a_b)
print(product_a_b_c)