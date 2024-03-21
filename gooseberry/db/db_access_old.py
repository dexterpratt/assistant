from neo4j import GraphDatabase

class DBAccess:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def create_node(self, label, properties):
        with self.driver.session() as session:
            result = session.execute_write(self._create_and_return_node, label, properties)
            return result

    @staticmethod
    def _create_and_return_node(tx, label, properties):
        query = (
            f"CREATE (n:{label} $properties) "
            "RETURN n"
        )
        result = tx.run(query, properties=properties)
        return result.single()[0]

    def find_nodes_by_name(self, label, name):
        with self.driver.session() as session:
            result = session.execute_read(self._find_and_return_nodes, label, name)
            return result

    @staticmethod
    def _find_and_return_nodes(tx, label, name):
        query = f"MATCH (n:{label}) WHERE n.name = $name RETURN n"
        result = tx.run(query, name=name)
        return [record["n"] for record in result]

    def remove_node(self, node):
        with self.driver.session() as session:
            session.execute_write(self._remove_node, node)  # No return value

    @staticmethod
    def _remove_node(tx, node):
        query = (
            "MATCH (n) "
            "WHERE id(n) = $node_id "
            "DELETE n"
        )
        tx.run(query, node_id=node.element_id)  # No return value
        
