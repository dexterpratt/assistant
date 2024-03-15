from neo4j import GraphDatabase

class DBAccess:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def create_node(self, label, properties):
        with self.driver.session() as session:
            result = session.write_transaction(self._create_and_return_node, label, properties)
            return result

    @staticmethod
    def _create_and_return_node(tx, label, properties):
        query = (
            f"CREATE (n:{label} $properties) "
            "RETURN n"
        )
        result = tx.run(query, properties=properties)
        return result.single()[0]

    # Example of a read operation
    def find_node_by_name(self, label, name):
        with self.driver.session() as session:
            result = session.read_transaction(self._find_and_return_node, label, name)
            return result

    @staticmethod
    def _find_and_return_node(tx, label, name):
        query = (
            f"MATCH (n:{label}) "
            f"WHERE n.name = $name "
            "RETURN n"
        )
        result = tx.run(query, name=name).single()
        return result[0] if result else None
