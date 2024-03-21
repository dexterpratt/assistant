from neo4j import GraphDatabase, exceptions

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
        try:
            return result.single()[0]
        except TypeError:
            return None

    def find_nodes_by_name(self, label, name):
        with self.driver.session() as session:
            result = session.read_transaction(self._find_and_return_nodes, label, name)
            return result

    @staticmethod
    def _find_and_return_nodes(tx, label, name):
        query = f"MATCH (n:{label}) WHERE n.name = $name RETURN n"
        result = tx.run(query, name=name)
        return [record["n"] for record in result]

    def remove_node(self, node_element_id):
        with self.driver.session() as session:
            session.write_transaction(self._remove_node, node_element_id)

    @staticmethod
    def _remove_node(tx, node_element_id):
        query = (
            "MATCH (n) "
            "WHERE id(n) = $node_element_id "
            "DELETE n"
        )
        tx.run(query, node_element_id=node_element_id)

    def clear_database(self):
        with self.driver.session() as session:
            session.write_transaction(self._clear_database)

    @staticmethod
    def _clear_database(tx):
        tx.run("MATCH (n) DETACH DELETE n")

# Usage example
if __name__ == "__main__":
    db = DBAccess(uri="bolt://localhost:7687", user="neo4j", password="samvimes")
    try:
        # Example operations
        db.clear_database()
        node_props = {"name": "Example Node"}
        created_node = db.create_node("ExampleLabel", node_props)
        print("Created Node:", created_node)
        found_nodes = db.find_nodes_by_name("ExampleLabel", "Example Node")
        print("Found Nodes:", found_nodes)
        # Clean up and close connection
        db.clear_database()
    except exceptions.Neo4jError as e:
        print(f"Database operation failed: {e}")
    finally:
        db.close()
