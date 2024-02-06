import tkinter as tk
from tkinter import ttk, filedialog
from odata_utils.xml_parser import get_entity_list, entity_types_parse_xml, get_property_list , get_navigation_list
import re
import pyperclip 

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("OData Metadata Sandbox")

        self.xml_file_path = tk.StringVar()
        self.start_entity = tk.StringVar()
        self.end_entity = tk.StringVar()

        self.include_entity = tk.StringVar(value="")
        
        self.selected_property = ""
        # Include Entity Entry
        include_entity_frame = tk.Frame(root)
        include_entity_frame.grid(row=5, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W)
        tk.Label(include_entity_frame, text="Include Navigations(A,B):").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.include_entity_entry = tk.Entry(include_entity_frame, textvariable=self.include_entity)
        self.include_entity_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        self.skip_entities = tk.StringVar(value="lastModifiedByNav,createdByNav")

        # Skip Entities Entry
        skip_entities_frame = tk.Frame(root)
        skip_entities_frame.grid(row=4, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W)
        tk.Label(skip_entities_frame, text="Skip Navigations(A,B)    :").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.skip_entities_entry = tk.Entry(skip_entities_frame, textvariable=self.skip_entities)
        self.skip_entities_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        # File Upload
        tk.Label(root, text="Select EDMX File:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.file_frame = tk.Frame(root)
        self.file_frame.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky=tk.W)
        self.file_entry = ttk.Entry(self.file_frame, textvariable=self.xml_file_path, state='readonly', width=50)
        self.file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(self.file_frame, text="Browse", command=self.browse_file).pack(side=tk.LEFT, padx=5)

        # Entity Selection
        entity_frame = tk.Frame(root)
        entity_frame.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky=tk.NSEW)

        # Select Starting Entity
        start_entity_frame = tk.Frame(entity_frame)
        start_entity_frame.grid(row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)
        start_entity_label = tk.Label(start_entity_frame, text="Select Starting Entity:")
        start_entity_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.start_entity_entry = tk.Entry(start_entity_frame, textvariable=self.start_entity)
        self.start_entity_entry.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.start_entity_listbox_frame = tk.Frame(start_entity_frame)
        self.start_entity_listbox_frame.grid(row=2, column=0, sticky=tk.NSEW)
        self.start_entity_listbox = tk.Listbox(self.start_entity_listbox_frame, selectmode=tk.SINGLE, height=10)
        self.start_entity_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.start_entity_scrollbar = tk.Scrollbar(self.start_entity_listbox_frame, orient=tk.VERTICAL)
        self.start_entity_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.start_entity_listbox.config(yscrollcommand=self.start_entity_scrollbar.set)
        self.start_entity_scrollbar.config(command=self.start_entity_listbox.yview)
        self.start_entity_listbox.bind('<Double-Button-1>', self.select_entity)

        # Display Listbox for Starting Entity
        self.start_display_frame = tk.Frame(start_entity_frame)
        self.start_display_frame.grid(row=0, column=1, rowspan=3, padx=5, pady=5, sticky=tk.NSEW)
        self.start_display_label = tk.Label(self.start_display_frame, text="Display Starting Entity:")
        self.start_display_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

        # Use Listbox instead of Text
        self.start_display_listbox = tk.Listbox(self.start_display_frame, height=10, width=30, selectmode=tk.SINGLE)
        self.start_display_listbox.grid(row=1, column=0, padx=5, pady=5, sticky=tk.NSEW)

        # Add a Scrollbar for the Listbox
        self.start_display_scrollbar = tk.Scrollbar(self.start_display_frame, orient=tk.VERTICAL)
        self.start_display_scrollbar.grid(row=1, column=1, sticky=tk.NS)
        self.start_display_listbox.config(yscrollcommand=self.start_display_scrollbar.set)
        self.start_display_scrollbar.config(command=self.start_display_listbox.yview)

        # Select Ending Entity
        end_entity_frame = tk.Frame(entity_frame)
        end_entity_frame.grid(row=0, column=1, padx=5, pady=5, sticky=tk.NSEW)
        end_entity_label = tk.Label(end_entity_frame, text="Select Ending Entity:")
        end_entity_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.end_entity_entry = tk.Entry(end_entity_frame, textvariable=self.end_entity)
        self.end_entity_entry.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.end_entity_listbox_frame = tk.Frame(end_entity_frame)
        self.end_entity_listbox_frame.grid(row=2, column=0, sticky=tk.NSEW)
        self.end_entity_listbox = tk.Listbox(self.end_entity_listbox_frame, selectmode=tk.SINGLE, height=10)
        self.end_entity_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.end_entity_scrollbar = tk.Scrollbar(self.end_entity_listbox_frame, orient=tk.VERTICAL)
        self.end_entity_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.end_entity_listbox.config(yscrollcommand=self.end_entity_scrollbar.set)
        self.end_entity_scrollbar.config(command=self.end_entity_listbox.yview)
        self.end_entity_listbox.bind('<Double-Button-1>', self.select_entity)

        # Display Listbox for Ending Entity
        self.end_display_frame = tk.Frame(end_entity_frame)
        self.end_display_frame.grid(row=0, column=1, rowspan=3, padx=5, pady=5, sticky=tk.NSEW)
        self.end_display_label = tk.Label(self.end_display_frame, text="Display Ending Entity:")
        self.end_display_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

        # Use Listbox instead of Text
        self.end_display_listbox = tk.Listbox(self.end_display_frame, height=10, width=30, selectmode=tk.SINGLE)
        self.end_display_listbox.grid(row=1, column=0, padx=5, pady=5, sticky=tk.NSEW)

        # Add a Scrollbar for the Listbox
        self.end_display_scrollbar = tk.Scrollbar(self.end_display_frame, orient=tk.VERTICAL)
        self.end_display_scrollbar.grid(row=1, column=1, sticky=tk.NS)
        self.end_display_listbox.config(yscrollcommand=self.end_display_scrollbar.set)
        self.end_display_scrollbar.config(command=self.end_display_listbox.yview)

        # Result Display
        self.result_textbox = tk.Text(root, height=5, width=60,state=tk.DISABLED)
        self.result_textbox.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky=tk.NSEW)

       # Submit Button
        ttk.Button(root, text="Find Shortest Path", command=self.find_shortest_path).grid(row=3, column=0, columnspan=2, pady=10)
        # Copy XPath Button
        copy_button = ttk.Button(root, text="📋 Copy Xpath", command=self.copy_xpath_to_clipboard)
        copy_button.grid(row=3, column=2, pady=0)

        # Bind the KeyRelease event for dynamic updates
        self.start_entity_entry.bind('<KeyRelease>', self.update_entity_listbox)
        self.end_entity_entry.bind('<KeyRelease>', self.update_entity_listbox)

        # Bind the Double-Button-1 event for selecting entities
        self.start_entity_listbox.bind('<Double-Button-1>', self.select_entity)
        self.end_entity_listbox.bind('<Double-Button-1>', self.select_entity)

        # Bind the Double-Button-1 event for selecting entities in display listboxes
        self.start_display_listbox.bind('<Double-Button-1>', self.select_entity)
        self.end_display_listbox.bind('<Double-Button-1>', self.select_entity)

        # Bind the Double-Button-1 event for selecting entities in display listboxes
        self.start_display_listbox.bind('<Double-Button-1>', self.select_entity)
        self.end_display_listbox.bind('<Double-Button-1>', self.select_entity)

        # Configure rows and columns to expand with the window
        for i in range(4):  # Number of rows
            root.grid_rowconfigure(i, weight=1)
        for i in range(3):  # Number of columns
            root.grid_columnconfigure(i, weight=1)
    
    def copy_xpath_to_clipboard(self):
        xpath = self.result_textbox.get(1.0, tk.END).strip()
        xpath_match = re.search(r'XPath: (.+)$', str(xpath), re.MULTILINE)
        xpath = xpath_match.group(1) if xpath_match else ""
        pyperclip.copy(xpath)


    def reset_selected_property(self):
        self.selected_property = ""

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
        self.xml_file_path.set(file_path)

        # Update the entity listbox as soon as the file is uploaded
        self.update_entity_listbox(None)

    def update_entity_listbox(self, event):
        xml_file_path = self.xml_file_path.get()
        if xml_file_path:
            entity_list = get_entity_list(xml_file_path)
            self.update_listbox(self.start_entity_listbox, entity_list, self.start_entity_entry)
            self.update_listbox(self.end_entity_listbox, entity_list, self.end_entity_entry)
            self.result_textbox.delete(1.0, tk.END)  # Clear result textbox
            self.result_textbox.insert(tk.END, "Entity list updated.")
        else:
            self.result_textbox.delete(1.0, tk.END)
            self.result_textbox.insert(tk.END, "Please select an XML file.")

    def find_shortest_path(self):
        selected_property = self.selected_property
        xml_file_path = self.xml_file_path.get()
        start_entity = self.start_entity.get()
        end_entity = self.end_entity.get()
        skip_entities = self.skip_entities.get()
        include_entity = self.include_entity.get()
        result_text = ""
        list_of_valid_navigations = get_entity_list(xml_file_path) + get_navigation_list(xml_file_path)

        if xml_file_path and start_entity and end_entity:
            if include_entity:
                # Use navigation through the specified entity
                entities_to_include = [entity.strip() for entity in include_entity.split(',')]
                shortest_distance, shortest_path = entity_types_parse_xml(xml_file_path, start_entity, entities_to_include[0], skip_entities)

                for i in range(1, len(entities_to_include)):
                    additional_distance, additional_path = entity_types_parse_xml(xml_file_path, entities_to_include[i - 1], entities_to_include[i], skip_entities)

                    if additional_distance != float("infinity") and shortest_distance != float("infinity"):
                        shortest_distance += additional_distance
                        shortest_path.extend(additional_path[1:])  # Exclude the repeated entity in the middle

                additional_distance, additional_path = entity_types_parse_xml(xml_file_path, entities_to_include[-1], end_entity, skip_entities)

                if additional_distance != float("infinity") and shortest_distance != float("infinity"):
                    shortest_distance += additional_distance
                    shortest_path.extend(additional_path[1:])  # Exclude the repeated entity in the middle

                count = sum(1 for item in shortest_path if item in list_of_valid_navigations)

                # Concatenate the selected property to the end of the XPath
                if selected_property:
                    shortest_path.append(str(selected_property))
                    list_of_valid_navigations.append(str(selected_property))
                    result_text = f"Destination property is: {str(selected_property)}\n"

                result_text += f"Shortest distance from {start_entity} to {end_entity} via {include_entity}: {count}\n"
                result_text += f"XPath: {'/'.join(filter(lambda item: item in list_of_valid_navigations, shortest_path))}"
            else:
                # Use normal navigation from start to ending entity
                shortest_distance, shortest_path = entity_types_parse_xml(xml_file_path, start_entity, end_entity, skip_entities)
                if shortest_distance != float("infinity"):
                    count = sum(1 for item in shortest_path if item in list_of_valid_navigations)

                    # Concatenate the selected property to the end of the XPath
                    if selected_property:
                        shortest_path.append(str(selected_property))
                        list_of_valid_navigations.append(str(selected_property))
                        result_text = f"Destination property is :{str(selected_property)}\n"

                    result_text += f"Shortest distance from {start_entity} to {end_entity}: {count}\n"
                    result_text += f"XPath: {'/'.join(filter(lambda item: item in list_of_valid_navigations, shortest_path))}"
                else:
                    result_text = f"There is no path from {start_entity} to {end_entity}"

            self.result_textbox.config(state=tk.NORMAL)
            self.result_textbox.delete(1.0, tk.END)  # Clear result textbox
            self.result_textbox.insert(tk.END, result_text)
            self.result_textbox.config(state=tk.DISABLED)
        else:
            self.result_textbox.config(state=tk.NORMAL)
            self.result_textbox.delete(1.0, tk.END)
            self.result_textbox.insert(tk.END, "Please provide all required inputs.")
            self.result_textbox.config(state=tk.DISABLED)


    def update_listbox(self, listbox, data, entry_widget):
        listbox.delete(0, tk.END)
        if (type(entry_widget) == str):
            value = entry_widget
        else:
            value = entry_widget.get()
        if value:
            pattern = re.compile(re.escape(value), re.IGNORECASE)
            filtered_data = [item for item in data if pattern.search(item)]
        else:
            filtered_data = data

        for item in filtered_data:
            listbox.insert(tk.END, item)

    def select_entity(self, event):
        widget = event.widget
        selected_index = widget.curselection()
        if selected_index:
            selected_entity = widget.get(selected_index)

            if widget == self.start_entity_listbox:
                self.start_entity.set(selected_entity)
                self.display_entity_info(selected_entity, self.start_display_listbox, self.start_entity_entry)
            elif widget == self.end_entity_listbox:
                self.end_entity.set(selected_entity)
                self.display_entity_info(selected_entity, self.end_display_listbox, self.end_entity_entry)
                self.reset_selected_property()  # Reset selected_property when a new ending entity is selected
            elif widget == self.start_display_listbox or widget == self.end_display_listbox:
                extracted_entity = re.search(r'\(Entity=([^,]+),', str(selected_entity)).group(1) if re.search(
                    r'\(Entity=([^,]+),', str(selected_entity)) else None
                if extracted_entity is not None:
                    entity_list = get_entity_list(self.xml_file_path.get())
                    if widget == self.start_display_listbox:
                        self.start_entity.set(extracted_entity)
                        self.display_entity_info(extracted_entity, self.start_display_listbox, self.start_entity_entry)
                        self.update_listbox(self.start_entity_listbox, entity_list, extracted_entity)
                    else:
                        self.end_entity.set(extracted_entity)
                        self.display_entity_info(extracted_entity, self.end_display_listbox, self.end_entity_entry)
                        self.update_listbox(self.end_entity_listbox, entity_list, extracted_entity)
                        self.reset_selected_property()  # Reset selected_property when a new ending entity is selected
                elif widget == self.end_display_listbox:
                    property_info = re.sub(r'\([^)]*\)', '', str(selected_entity)).replace('*', '')
                    self.selected_property = property_info
                    property_info = "Selected destination property :" + property_info
                    self.result_textbox.config(state=tk.NORMAL)
                    self.result_textbox.delete(1.0, tk.END)
                    self.result_textbox.insert(tk.END, property_info)
                    self.result_textbox.config(state=tk.DISABLED)


    def display_entity_info(self, entity_name, listbox, entry_widget):
        # Placeholder function to display entity information
        # You can replace this with actual code to fetch and display information about the entity
        xml_file_path = self.xml_file_path.get()
        entity_info = get_property_list(xml_file_path, entity_name)

        # Clear the Listbox
        listbox.delete(0, tk.END)

        # Split the entity_info into lines
        lines = entity_info.split("\n")

        # Separate properties, keys, and navigation properties
        properties = [line for line in lines if "(Property)" in line]
        keys = [line for line in lines if "(Key)" in line]
        navigation_properties = [line for line in lines if "(NavigationProperty)" in line]

        # Display keys
        keys.sort()
        for line in keys:
            listbox.insert(tk.END, "" + line.replace("(Key)", "").replace("abcd", "\n\t"))

        # Display properties
        properties.sort()
        for line in properties:
            listbox.insert(tk.END, "*" + line.replace("(Property)", "").replace("abcd", "\n\t"))

        # Display navigation properties
        navigation_properties.sort()
        for line in navigation_properties:
            listbox.insert(tk.END, "**" + line.replace("(NavigationProperty)", "").replace("abcd", ","))

        # Update the entry widget with the selected entity
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, entity_name)