import pytest
from gooseberry.db.db_access import DBAccess

@pytest.fixture(scope="module")
def db_access():
    # Setup code to initialize DBAccess with test database credentials
    db = DBAccess(uri="bolt://localhost:7687", user="neo4j", password="samvimes")
    yield db
    # Teardown code to close connection, clean up test data, etc.
    db.close()

def test_create_node(db_access: DBAccess):
    properties = {"name": "TestNode"}
    node = db_access.create_node("TestLabel", properties)
    assert node is not None
    
    # Additional assertions to verify the node's properties, label, etc.
    assert node["name"] == "TestNode"  # Verify the "name" property
    assert node.labels == {"TestLabel"}  # Verify the label

    # Remove the node
    db_access.remove_node(node)

    # Verify the removal of the node
    removed_node = db_access.find_nodes_by_name("TestLabel", "TestNode")
    assert removed_node is None

