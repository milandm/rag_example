
def add_node(tx, node_type, name):
    """

    :param tx:
    :param node_type:
    :param name:
    :return:
    """
    query = f'CREATE (n: `{node_type}` {{name: "{name}"}}) RETURN n'
    return tx.run(query, node_type=node_type, name=name)

def add_node_with_properties(tx, node_type, procedure_id, properties_dict):
    # with driver.session() as session:
    #     session.write_transaction(create_nodes)
    #     node_count = session.read_transaction(check_nodes)
    #
    #     # Print the result
    #     print(f"Number of Person nodes: {node_count}")
    #
    #     # Verify if nodes were added
    #     if node_count > 0:
    #         print("Nodes were added successfully!")
    #     else:
    #         print("No nodes were added.")
    #
    # # Close the driver
    # driver.close()
    #
    """

    :param tx:
    :param node_type:
    :param procedure_id:
    :param properties_dict:
    :return:
    """
    properties = handle_properties(procedure_id, properties_dict)
    query = f'CREATE (n: `{node_type}` {{{properties}}}) RETURN n'
    return tx.run(query, node_type=node_type, procedure_id=procedure_id, properties_dict=properties_dict)

def handle_properties(procedure_id, properties):
    """

    :param procedure_id:
    :param properties:
    :return:
    """
    labels = f'procedure_id : "{procedure_id}"'
    properties = ', '.join(f'{key}: "{properties[key]}"' for key in properties.keys() if
                           key != 'variables_list' and key != 'dependencies_list')
    print(properties)
    if len(properties) != 0:
        return f'{labels}, {properties}'
    else:
        return labels

def add_edge(tx, node_type1, node1, node_type2, node2, relationship):
    """

    :param tx:
    :param node_type1:
    :param node1:
    :param node_type2:
    :param node2:
    :param relationship:
    :return:
    """
    query = f"""
            MATCH (a:{node_type1} {{procedure_id: "{node1}"}}), (b:{node_type2} {{procedure_id: "{node2}"}})
            MERGE (a)-[r:{relationship}]->(b)
            RETURN r
            """
    return tx.run(query,
                  node_type1=node_type1,
                  node1=node1,
                  node_type2=node_type2,
                  node2=node2,
                  relationship=relationship)

def edit_node(tx, node_type, node_name):
    """

    :param node_type:
    :param node_name:
    :return:
    """
    query = f"""
            MATCH (n:{node_type} {{name: "{node_name}"}}))
            SET n += \$props
            RETURN n
            """
    return tx.run(query, node_type=node_type, node_name=node_name)

def edit_edge(tx, node_type1, node1, node_type2, node2, relationship, changed_property):
    """

    :param node_type1:
    :param node1:
    :param node_type2:
    :param node2:
    :param relationship:
    :param changed_property:
    :return:
    """
    query = f"""
            MATCH (a:{node_type1} {{name: "{node1}"}})-[r:{relationship}]->(b:{node_type2} {{name: "{node2}"}})
            SET r.propertyName = {changed_property}'
            RETURN r
            """
    return tx.run(query,
                  node_type1=node_type1,
                  node1=node1,
                  node_type2=node_type2,
                  node2=node2,
                  relationship=relationship,
                  changed_property=changed_property)

def delete_node(tx, node_type, node_name):
    """

    :param node_type:
    :param node_name:
    :return:
    """
    query = f"""
            MATCH (n:{node_type} {{name: "{node_name}"}})
            DETACH DELETE n
            """
    return tx.run(query, node_type=node_type, node_name=node_name)

def delete_edge(tx, name):
    """

    :return:
    """
    query = f"""
            MATCH (n) WHERE name(n) = {name}
            SET n += \$props
            RETURN n
            """
    return tx.run(query, )

def delete_all_nodes(tx):
    """

    :param tx:
    :return:
    """
    query = "MATCH (n) DETACH DELETE n"
    return tx.run(query)
