import lark
from typing import List, Union, Dict, Any
import logging
import json

JSONType = Union[str, int, float, bool, None, Dict[str, Any], List[Any]]

class JsonExplorer:
    """
    Class to execute the main features
    """
    def __init__(self):
        self.lang = """
            start: expr_list

            key_string: string
                | CNAME

            key_int: INT
                | wildcard

            expr_list: list_req
                | list
                | expr

            expr: key_int
                | key_string

            list: "{" [expr("," expr_list)*] "}"
            list_req: [expr("." expr_list)*]

            string : ESCAPED_STRING
            wildcard: "*"
            %import common.ESCAPED_STRING
            %import common.INT
            %import common.CNAME
            %import common.WS
            %ignore WS
        """
        self.l = lark.Lark(self.lang)
        self.parsed_key = None
        self.parsed_result = None
        self.node_visitors = NodeVisitors()

    def parse(self, key: str) -> lark.Tree:
        """
        Parse the key
        @param key
        @return Lark Tree
        """
        self.parsed_key = self.l.parse(key)
        return self.parsed_key

    def explore(self, data: JSONType) -> List[Any]:
        """
        Get the data matching with the self.parsed_key
        @param Dict to filter
        @return List of results
        """
        if(self.parsed_key is not None):
            self.parsed_result = self.node_visitors.entrypoint(self.parsed_key, data)
            return self.parsed_result
        raise Exception('Need to use parse method before explore')

    def parse_and_explore(self, key: str, data: JSONType) -> List[Any]:
        """
        Parse the key & get the data matching with the key
        @param Key to parse
        @param Data to filter
        @return List of results
        """
        self.parse(key)
        return self.explore(data)
    
    def flatten_results(self) -> List[List[Union[str, int]]]:
        if(isinstance(self.parsed_result, list)):
            list_final = []
            for result in self.parsed_result:
                list_final.append(self.flatten(result))
            return list_final
        else:
            return [[self.parsed_result]]

    def flatten(self, obj_to_flat: List[Any]) -> List[Union[str, list]]:
        if(isinstance(obj_to_flat, list)):
            result = []
            for item in obj_to_flat:
                result += self.flatten(item)
            return result
        else:
            return [obj_to_flat]

NODE_NORMAL = 0
NODE_WILDCARD = 1

class NodeVisitors:
    def __init__(self):
        # logging.basicConfig(level=logging.DEBUG)
        self.result = []
        self.ptr = self.result

    def entrypoint(self, tree, data):
        logging.debug("Entrypoint:\nTree: %s\nData: %s" % (str(tree), json.dumps(data, indent=4)))
        self.result = []
        self.ptr = self.result
        return self.node_expr_list(tree.children[0], data)

    def node_expr_list(self, tree, data):
        assert tree.data == "expr_list"
        logging.debug("node_expr_list:\nTree: %s\nData: %s" % (str(tree), json.dumps(data, indent=4)))
        children_data = tree.children[0].data
        if(children_data == "list_req"):
            return self.node_list_req(tree.children[0], data)
        elif(children_data == "list"):
            return self.node_list(tree.children[0], data)
        elif(children_data == "expr"):
            res_expr, _ = self.node_expr(tree.children[0], data)
            return res_expr
    
    def node_list_req(self, tree, data):
        """
        list "."
        """
        assert tree.data == "list_req"
        logging.debug("node_list_req:\nTree: %s\nData: %s" % (str(tree), json.dumps(data, indent=4)))
        res_expr, node_type = self.node_expr(tree.children[0], data)
        if(len(tree.children) >= 2):
            if(node_type == NODE_NORMAL):
                return self.node_expr_list(tree.children[1], res_expr)
            elif(isinstance(res_expr, list)):
                return [self.node_expr_list(tree.children[1], res_expr[i]) for i in range(len(res_expr))]
        else:
            return res_expr
    
    def node_list(self, tree, data):
        """
        list or ","
        """
        assert tree.data == "list"
        logging.debug("list:\nTree: %s\nData: %s" % (str(tree), json.dumps(data, indent=4)))
        list_res = []
        res_expr, _ = self.node_expr(tree.children[0], data)
        list_res.append(res_expr)
        for id_children, children in enumerate(tree.children[1:]):
            list_res.append(self.node_expr_list(children, data))
        return list_res

    def node_key_string(self, tree, data):
        logging.debug("key_string:\nTree: %s\nData: %s" % (str(tree), json.dumps(data, indent=4)))
        assert tree.data == "key_string"
        # import pdb ; pdb.set_trace()
        if("value" in dir(tree.children[0])):
            return data[tree.children[0].value], NODE_NORMAL
        elif("data" in dir(tree.children[0]) and tree.children[0].data == "string"):
            return self.node_string(tree.children[0], data), NODE_NORMAL

    def node_key_int(self, tree, data):
        assert tree.data == "key_int"
        logging.debug("key_int:\nTree: %s\nData: %s" % (str(tree), json.dumps(data, indent=4)))
        if("data" in dir(tree.children[0])):
            if(tree.children[0].data == "wildcard"):
                return [data[i] for i in range(len(data))], NODE_WILDCARD
            else:
                raise Exception("Children data field undefined: %s" % tree.children[0].data)
        elif("type" in dir(tree.children[0])):
            if(tree.children[0].type == "INT"):
                return data[int(tree.children[0])], NODE_NORMAL
            else:
                raise Exception("Children type field undefined: %s" % tree.children[0].type)

    def node_expr(self, tree, data, multiple=False) -> List[str]:
        assert tree.data == "expr"
        logging.debug("node_expr:\nTree: %s\nData: %s" % (str(tree), json.dumps(data, indent=4)))
        if(tree.children[0].data == "key_string"):
            return self.node_key_string(tree.children[0], data)
        elif(tree.children[0].data == "key_int"):
            return self.node_key_int(tree.children[0], data)
        else:
            raise Exception("Children data field undefined: %s" % tree.children[0].data)
    
    def node_string(self, tree, data):
        assert tree.data == "string"
        logging.debug("node_string:\nTree: %s\nData: %s" % (str(tree), json.dumps(data, indent=4)))
        return data[tree.children[0].value[1:-1]]







