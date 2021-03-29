import jsonexplorer
import unittest
import subprocess

class TestParser(unittest.TestCase):
	def test_console_help(self):
		ps = subprocess.Popen(["python3", "-m", "jsonexplorer", "--help"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		_, err = ps.communicate()
		self.assertEqual(0, ps.returncode)
		self.assertEqual("", err.decode("utf8"))

	def test_console_input(self):
		ps = subprocess.Popen(
			["python3", "-m", "jsonexplorer", "--input", '{"object": "res_object", "object2": "res_object2"}', "object"],
			stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		out, err = ps.communicate()
		self.assertEqual(0, ps.returncode)
		self.assertEqual("res_object", out.decode("utf8").strip())
		self.assertEqual("", err.decode("utf8"))
	
	def test_console_input_file(self):
		ps = subprocess.Popen(
			["python3", "-m", "jsonexplorer", "--input-file", "data/test.json", "object.*.name"],
			stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		out, err = ps.communicate()
		self.assertEqual(0, ps.returncode)
		self.assertListEqual(["alpha", "beta", "charlie"],
			[line.strip() for line in out.decode("utf8").split("\n") if(line.strip() != "")])
		self.assertEqual("", err.decode("utf8"))
	
	def test_key_string_cname(self):
		data = {
  			"object": "res_object",
			"object2": "res_object2"
		}
		obj = jsonexplorer.JsonExplorer()
		self.assertTrue(obj.parse_and_explore("object", data) == "res_object")
		self.assertTrue(obj.parse_and_explore("object2", data) == "res_object2")

	def test_key_string_string(self):
		data = {
  			"object test": "res_object",
			"object2 test2": "res_object 2"
		}
		obj = jsonexplorer.JsonExplorer()
		self.assertTrue(obj.parse_and_explore("\"object test\"", data) == "res_object")
		self.assertTrue(obj.parse_and_explore("\"object2 test2\"", data) == "res_object 2")
	
	def test_key_int_int(self):
		data = [
			"a",
			"b"
		]
		obj = jsonexplorer.JsonExplorer()
		self.assertTrue(obj.parse_and_explore("0", data) == "a")
		self.assertTrue(obj.parse_and_explore("1", data) == "b")
	
	def test_key_int_wildcard(self):
		data = [
			"a",
			"b"
		]
		obj = jsonexplorer.JsonExplorer()
		res = obj.parse_and_explore("*", data)
		self.assertListEqual(res, ["a", "b"])
	
	def test_list_req(self):
		data = {
			"object": {
				"name": "toto",
				"value": 2
			}
		}
		obj = jsonexplorer.JsonExplorer()
		self.assertTrue(obj.parse_and_explore("object.name", data) == "toto")
		self.assertTrue(obj.parse_and_explore("object.value", data) == 2)
	
	def test_list(self):
		data = {
			"object": {
				"name": "toto",
				"value": 2,
				"second": 3,
				"last name": "toto last"
			}
		}
		obj = jsonexplorer.JsonExplorer()
		self.assertListEqual(obj.parse_and_explore("object.{name,value}", data), ["toto", 2])
		self.assertListEqual(obj.parse_and_explore("object.{name,\"last name\"}", data), ["toto", "toto last"])
		self.assertListEqual(obj.parse_and_explore("object.{name,\"last name\",value}", data), ["toto", "toto last", 2])
	
	def test_key_int_list_req(self):
		data = {
			"object": [
				{
					"name": "a",
					"last_name": "alast"
				},
				{
					"name": "b",
					"last_name": "blast"
				}
			]
		}
		obj = jsonexplorer.JsonExplorer()
		self.assertListEqual(obj.parse_and_explore("object.*.{name,last_name}", data), [["a", "alast"], ["b", "blast"]])
		self.assertListEqual(obj.parse_and_explore("object.0.{name,last_name}", data), ["a", "alast"])

	def test_key_int_list_req_list(self):
		data = {
			"object": [
				{
					"name": "a",
					"last_name": "alast",
					"extra": {
						"value": 0,
						"date": "01/01"
					}
				},
				{
					"name": "b",
					"last_name": "blast",
					"extra": {
						"value": 1,
						"date": "06/06"
					}
				}
			]
		}
		obj = jsonexplorer.JsonExplorer()
		self.assertListEqual(obj.parse_and_explore("object.*.{name,extra.value}", data), [["a", 0], ["b", 1]])
		self.assertListEqual(obj.parse_and_explore("object.0.{name,extra.value,extra.date}", data), ["a", 0, "01/01"])