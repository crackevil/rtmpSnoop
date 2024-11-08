import absimp
absimp.path_include_cwd(__file__)
import unittest
from Stream import Stream1, Stream2


class base_test_stream(unittest.TestCase):

	def setUp(self):
		try:
			self.ClassStream
		except AttributeError:
			self.skipTest('base class')

	def test_appendData(self):
		stream = self.ClassStream()
		data1 = b'abcdefg'
		stream.appendData(data1)
		self.assertEqual(stream.size, len(data1))

		data2 = b'012'
		stream.appendData(data2)
		self.assertEqual(stream.size, len(data1)+len(data2))

	def test_getBytes(self):
		stream = self.ClassStream()
		data1 = b'abcdefg'
		stream.appendData(data1)
		self.assertEqual(stream.getBytes(2), b'ab')
		self.assertEqual(stream.getBytes(2), b'cd')

	def test_readBytes(self):
		stream = self.ClassStream()
		data1 = b'abcdefg'
		stream.appendData(data1)
		self.assertEqual(stream.readBytes(2), b'ab')
		self.assertEqual(stream.readBytes(2), b'ab')

	def test_haveBytes(self):
		stream = self.ClassStream()
		data1 = b'abcdefg'
		stream.appendData(data1)
		self.assertTrue(stream.haveBytes())
		self.assertEqual(stream.readBytes(len(data1)), data1)
		self.assertEqual(stream.getBytes(len(data1)), data1)
		self.assertFalse(stream.haveBytes())


class test_Stream1(base_test_stream):
	ClassStream = Stream1


class test_Stream2(base_test_stream):
	ClassStream = Stream2

if __name__ == "__main__":
	unittest.main(verbosity=1)
