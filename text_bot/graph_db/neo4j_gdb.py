from neo4j import GraphDatabase
from custom_logger.universal_logger import UniversalLogger
from text_bot.graph_db.neo4j_transactions import (add_node,
                                                  add_node_with_properties,
                                                  add_edge,
                                                  handle_properties,
                                                  edit_node,
                                                  edit_edge,
                                                  delete_node,
                                                  delete_edge,
                                                  delete_all_nodes)
from text_bot.nlp_model.config import (
    NEO4J_URI,
    NEO4J_USERNAME,
    NEO4J_PASSWORD
)

properties_to_use = ['general_info', 'type', 'code']

class Neo4jDB:


    def __init__(self):
        self.logger = UniversalLogger('./log_files/app.log', max_bytes=1048576, backup_count=3)
        self.gds = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))
        self.session = self.gds.session()

        try:
            with self.gds.session() as session:
                session.run("RETURN 1")
            self.logger.info("Connection successful!")
        except Exception as e:
            self.logger.error(f"Connection failed: {e}")



    def create_procedure_nodes(self, json_chunk):
        procedure_division = json_chunk.get('procedure_division', {})
        print(procedure_division['procedure_id'])

        properties = {key: value for key, value in procedure_division.items() if key in properties_to_use}
        self.session.execute_write(add_node_with_properties,
                              'code_block', #  node_type
                              procedure_division['procedure_id'], #  node_name
                              properties,
                              )

    def create_node(self, json_chunk, properties):
        node_type = json_chunk.get('node_type', "N/A")
        node_name = json_chunk.get('node_name', "N/A")
        program_id = json_chunk.get('program_id', "N/A")
        properties['program_id'] = program_id  # Add program_id to the properties

        properties_str = ', '.join([f'n.{key} = ${key}' for key in properties.keys()])

        with self.session.begin_transaction() as tx:
            query = f"""
                    MERGE (n:{node_type} {{node_name: $node_name, program_id: $program_id}})
                    ON CREATE SET {properties_str}
                    RETURN n
                    """
            if "code_structure_type" in properties:
                structure_type = properties["code_structure_type"]
                if node_name == "PROCEDURE DIVISION_0":
                    structure_type = "MAIN"
                query = f"""
                        MERGE (n:{node_type} {{node_name: $node_name, program_id: $program_id}})
                        ON CREATE SET n:{structure_type}, {properties_str}
                        RETURN n
                        """

            result = tx.run(query, node_name=node_name, **properties)
            summary = result.consume()
            if summary.counters.nodes_created > 0:
                self.logger.info(f"nodes_created {summary.counters.nodes_created}")
                self.logger.info("Node was added successfully!")
            else:
                self.logger.error("No nodes were added.")

    def create_nodes_and_edges(self, parent_label, child_label, nodes_properties, edge_type, common_field):
        for node in nodes_properties:
            if node['type'] == 'parent':
                self.create_node1(node, node['properties'])
            elif node['type'] == 'child':
                self.create_node1(node, node['properties'])

        for node in nodes_properties:
            if node['type'] == 'child':
                self.create_edge(
                    parent_label, child_label, edge_type, common_field, node['properties'][common_field]
                )

    def create_edges_on_parent(self, parent_node, dependencies_list, edge_type):
        print("dependencies_list "+str(dependencies_list))
        parent_node_type = parent_node.get('node_type', "N/A")
        parent_node_name = parent_node.get("node_name", "N/A")
        parent_program_id = parent_node.get("program_id", "N/A")  # Get the program_id for the parent node

        with self.session.begin_transaction() as tx:
            for dependency in dependencies_list:
                dependency_name = dependency.get("node_name", 'N/A')
                dependency_type = dependency.get("node_type", "N/A")
                dependency_program_id = dependency.get("program_id", "N/A")  # Get the program_id for the dependency

                print("parent_program_id "+parent_program_id)
                print("dependency_program_id " + dependency_program_id)
                query = f"""
                    MATCH (p:{parent_node_type} {{node_name: $parent_node_name, program_id: $parent_program_id}})
                    MATCH (c:{dependency_type} {{node_name: $dependency_name, program_id: $dependency_program_id}})
                    MERGE (p)-[:{edge_type}]->(c)
                """

                result = tx.run(query,
                                parent_node_name=parent_node_name,
                                parent_program_id=parent_program_id,
                                dependency_name=dependency_name,
                                dependency_program_id=dependency_program_id)

                summary = result.consume()
                if summary.counters.relationships_created > 0:
                    self.logger.info("relationships_created " + str(summary.counters.relationships_created))
                    self.logger.info("Edge was added successfully!")
                else:
                    self.logger.error("No edges were added.")

    def create_edges_on_parent1(self, parent_node, dependencies_list, edge_type):

        parent_node_type = parent_node.get('node_type', "N/A")
        parent_node_name = parent_node.get("node_name", "N/A")
        with self.session.begin_transaction() as tx:
            for dependency in dependencies_list:
                dependency_name = dependency.get("node_name", 'N/A')
                dependency_type = dependency.get("node_type", "N/A")

                query = f"""
                    MATCH (p:{parent_node_type} {{node_name: $parent_node_name}})
                    MATCH (c:{dependency_type} {{node_name: $dependency_name}})
                    MERGE (p)-[:{edge_type}]->(c)
                """

                result = tx.run(query,
                                parent_node_name=parent_node_name,
                                dependency_name=dependency_name)

                summary = result.consume()
                if summary.counters.relationships_created > 0:
                    self.logger.info("relationships_created "+str(summary.counters.relationships_created))
                    self.logger.info("Edge was added successfully!")
                else:
                    self.logger.error("No edges were added.")


    # 'code_block',
    # procedure_division['procedure_id'],
    # properties_to_use = ['general_info', 'type', 'code']

    def create_variabless_nodes(self, json_file):
        """

        :param json_file:
        :return:
        """
        for procedure, sub_procedures in json_file.items():
            self.session.execute_write(add_node, 'procedure', procedure)
            for section, properties in sub_procedures.items():
                self.session.execute_write(add_node_with_properties, 'section', section, properties)
                if 'variables' in properties:
                    for variable in properties['variables']:
                        self.session.execute_write(add_node, 'variable', variable)

    def create_edges(self, json_chunk):
        """

        :param session:
        :param json_chunk:
        :return:
        """
        procedure_division = json_chunk.get('procedure_division', {})
        root_node = procedure_division['procedure_id']

        for procedure in procedure_division['procedures_list']:
            dependencies_list = procedure.get('dependencies_list', [])

            for dependency in dependencies_list:
                target_node = dependency.get('dependency_name', 'N/A')
                self.session.execute_write(add_edge,
                                      'code_block',
                                      root_node,
                                      'code_block',
                                      target_node,
                                      'performs')

    def create_nodes(self, file_path):

        chunks = self.load_chunks(file_path)

        for file_name, chunk_info in chunks.items():
            print(f'Reading file {file_name}')
            self.create_procedure_nodes(self.session, chunk_info)

        for file_name, chunk_info in chunks.items():
            self.create_edges(self.session, chunk_info)


    def close_connection(self):
        """
        Closes the connection to the Neo4j database.
        """
        if self.session:
            self.session.close()
            self.logger.info("Neo4j Connection closed.")
        else:
            self.logger.info("No active connection to close.")