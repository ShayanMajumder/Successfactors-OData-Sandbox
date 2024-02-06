# xml_parser.py
import xml.etree.ElementTree as ET
import re
from .graph_utils import dijkstra, add_value_to_dict_set

def map_multiplicity(multiplicity):
    if multiplicity == "1":
        return "One"
    elif multiplicity == "*":
        return "Many"
    elif multiplicity == "0..1":
        return "One or Zero"
    else:
        print(multiplicity)
        return multiplicity

def delete_keys_from_hashmap(hashmap, keys_to_delete):
    # Split the comma-separated keys
    keys_list = keys_to_delete.split(',')

    # Remove leading and trailing whitespaces from each key
    keys_list = [key.strip() for key in keys_list]

    # Delete keys from the hashmap
    for key in keys_list:
        hashmap[key] = {}

def add_value_to_dict_set(dictionary, key, value=""):
    # Check if the key already exists in the dictionary
    if key in dictionary:
        # If the key exists, add the value to the existing set
        dictionary[key].add(value)
    else:
        # If the key does not exist, create a new set with the provided value
        dictionary[key] = {value}


def get_entity_list(xml_file_path):
    try:
        tree = ET.parse(xml_file_path)
        root = tree.getroot()

        namespace = {
            "edmx": "http://schemas.microsoft.com/ado/2007/06/edmx",
            "atom": "http://www.w3.org/2005/Atom",
            "m": "http://schemas.microsoft.com/ado/2007/08/dataservices/metadata",
            "default": "http://schemas.microsoft.com/ado/2008/09/edm",
            "sf": "http://www.successfactors.com/edm/sf",
            "sap": "http://www.successfactors.com/edm/sap",
        }

        entity_types = root.findall(".//default:EntityType", namespaces=namespace)
        entity_list = []
        for entity_type in entity_types:
            entity_type_name = entity_type.get("Name")
            entity_list.append(entity_type_name)
        entity_list = sorted(entity_list)
        return entity_list

    except Exception as e:
        print(f"Error: {e}")

def get_navigation_list(xml_file_path):
    try:
        tree = ET.parse(xml_file_path)
        root = tree.getroot()

        namespace = {
            "edmx": "http://schemas.microsoft.com/ado/2007/06/edmx",
            "atom": "http://www.w3.org/2005/Atom",
            "m": "http://schemas.microsoft.com/ado/2007/08/dataservices/metadata",
            "default": "http://schemas.microsoft.com/ado/2008/09/edm",
            "sf": "http://www.successfactors.com/edm/sf",
            "sap": "http://www.successfactors.com/edm/sap",
        }
        navigation_list = []
        entity_types = root.findall(".//default:EntityType", namespaces=namespace)
        for entity_type in entity_types:
            entity_type_name = entity_type.get("Name")
            # if(entity_type_name == "EmpEmployment"):
            # print(f"EntityType Name = {entity_type_name}")

            # Find all NavigationProperty elements within the current EntityType
            navigation_properties = entity_type.findall(
                ".//default:NavigationProperty", namespaces=namespace
            )

            for nav_property in navigation_properties:
                nav_name = nav_property.get("Name")
                navigation_list.append(nav_name)

            #    print(f"Navigation Property {nav_name} = {from_role},{to_role},{nav_name}")
        return navigation_list

    except Exception as e:
        print(f"Error: {e}")


def entity_types_parse_xml(xml_file_path, start, end,keys_to_delete = ""):
    try:
        tree = ET.parse(xml_file_path)
        root = tree.getroot()

        namespace = {
            "edmx": "http://schemas.microsoft.com/ado/2007/06/edmx",
            "atom": "http://www.w3.org/2005/Atom",
            "m": "http://schemas.microsoft.com/ado/2007/08/dataservices/metadata",
            "default": "http://schemas.microsoft.com/ado/2008/09/edm",
            "sf": "http://www.successfactors.com/edm/sf",
            "sap": "http://www.successfactors.com/edm/sap",
        }

        # Find all EntityType elements
        dict_of_navigations = {}

        entity_types = root.findall(".//default:EntityType", namespaces=namespace)
        for entity_type in entity_types:
            entity_type_name = entity_type.get("Name")
            # if(entity_type_name == "EmpEmployment"):
            # print(f"EntityType Name = {entity_type_name}")

            # Find all NavigationProperty elements within the current EntityType
            navigation_properties = entity_type.findall(
                ".//default:NavigationProperty", namespaces=namespace
            )

            for nav_property in navigation_properties:
                nav_name = nav_property.get("Name")
                add_value_to_dict_set(dict_of_navigations, entity_type_name, nav_name)
                # from_role = nav_property.get('FromRole')
                to_role = nav_property.get("ToRole")
                add_value_to_dict_set(dict_of_navigations, nav_name, to_role)

            #    print(f"Navigation Property {nav_name} = {from_role},{to_role},{nav_name}")

        association_sets = root.findall(
            ".//default:AssociationSet", namespaces=namespace
        )
        for association_set in association_sets:
            endpoints = association_set.findall(".//default:End", namespaces=namespace)
            for endpoint in endpoints:
                from_endpoint = endpoint.get("Role")
                to_endpoint = endpoint.get("EntitySet")
                add_value_to_dict_set(dict_of_navigations, from_endpoint, to_endpoint)
                add_value_to_dict_set(dict_of_navigations, to_endpoint, to_endpoint)
        
        delete_keys_from_hashmap(dict_of_navigations,keys_to_delete)
        shortest_distance, shortest_path = dijkstra(dict_of_navigations, start, end)
        return shortest_distance, shortest_path

        # print(len(dict_of_navigations["EmpJob"]))

    except Exception as e:
        print(f"Error: {e}")

def get_property_list(xml_file_path,name):
    try:
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
        dict_of_entity_elements = {}
        namespace = {
            "edmx": "http://schemas.microsoft.com/ado/2007/06/edmx",
            "atom": "http://www.w3.org/2005/Atom",
            "m": "http://schemas.microsoft.com/ado/2007/08/dataservices/metadata",
            "default": "http://schemas.microsoft.com/ado/2008/09/edm",
            "sf": "http://www.successfactors.com/edm/sf",
            "sap": "http://www.successfactors.com/edm/sap",
        }

        association_dict = {}
        association_sets = root.findall(
            ".//default:AssociationSet", namespaces=namespace
        )
        for association_set in association_sets:
            association_name = association_set.get("Association")
            endpoints = association_set.findall(".//default:End", namespaces=namespace)
            endpoint = endpoints[1]
            to_endpoint = endpoint.get("EntitySet")
            association_dict[association_name] = to_endpoint
        
        multiplicity_dict = {}
        association_sets = root.findall(
            ".//default:Association", namespaces=namespace
        )
        for association_set in association_sets:
            association_name = association_set.get("Name")
            endpoints = association_set.findall(".//default:End", namespaces=namespace)
            startpoint = endpoints[0]
            endpoint = endpoints[1]
            from_point  = map_multiplicity(str(startpoint.get("Multiplicity")))
            to_endpoint = map_multiplicity(str(endpoint.get("Multiplicity")))
            multiplicity_dict[association_name] = str(from_point) + " to " + str(to_endpoint)

        entity_types = root.findall(".//default:EntityType", namespaces=namespace)
        for entity_type in entity_types:
            entity_type_name = entity_type.get("Name")
            properties = entity_type.findall(
                ".//default:Property", namespaces=namespace
            )
            for property in properties:
                upsertable_attr = next((attr for attr in property.attrib if re.match(r"{.*}upsertable", attr)), None)

                upsertable = property.get(upsertable_attr, "None") if upsertable_attr else "None"

                required_attr = next((attr for attr in property.attrib if re.match(r"{.*}required", attr)), None)

                required = property.get(required_attr, "None") if required_attr else "None"

                picklist_attr = next((attr for attr in property.attrib if re.match(r"{.*}required", attr)), None)

                picklist = property.get(picklist_attr, "None") if picklist_attr else "None"
                
                property_name = (
                    property.get("Name")
                    + " (Property) "
                    + "( upsertable="
                    + upsertable
                    +",required="
                    + required
                    +",picklist="
                    + picklist
                    + ")"
                )
                add_value_to_dict_set(dict_of_entity_elements, entity_type_name, property_name)

            properties = entity_type.findall(
                ".//default:PropertyRef", namespaces=namespace
            )
            for property in properties:
                property_name = property.get("Name")
                property_name = (
                    property.get("Name")
                    + " (Key) "
                )
                add_value_to_dict_set(dict_of_entity_elements, entity_type_name, property_name)
            
            properties = entity_type.findall(
                ".//default:NavigationProperty", namespaces=namespace
            )
            for property in properties:
                points_to = association_dict.get(property.get("Relationship"), "Not found")
                #print(multiplicity_dict)
                multiplicity = multiplicity_dict.get(re.sub(f"SFOData\.", "", property.get("Relationship")), "Multiplicity Not Found")
                upsertable_attr = next((attr for attr in property.attrib if re.match(r"{.*}upsertable", attr)), None)

                upsertable = property.get(upsertable_attr, "None") if upsertable_attr else "None"

                required_attr = next((attr for attr in property.attrib if re.match(r"{.*}required", attr)), None)

                required = property.get(required_attr, "None") if required_attr else "None"
                
                property_name = (
                    property.get("Name")
                    + " (NavigationProperty) "
                    + "(Entity="
                    + points_to
                    + ",upsertable="
                    + upsertable
                    +",required="
                    +required
                    +",multiplicity="
                    +multiplicity
                    +")"
                )
                add_value_to_dict_set(dict_of_entity_elements, entity_type_name, property_name)

        result_string = "\n".join(dict_of_entity_elements[name])
        return result_string

    except Exception as e:
        print(f"Error: {e}")