import os
import re


def parse_tsv(file):
    entries = []
    splitter = r'\t'
    # The first line of the file is field headers
    headers = re.split(splitter, file.readline())
    for line in file:
        entry = {}
        values = re.split(splitter, line)
        # Each line contains values for each header
        for key in range(0, len(headers)):
            entry[headers[key]] = values[key]
        entries.append(entry)
    return entries


# Store a dictionary of functions to parse different file types
file_parsers = {
    ".tsv": parse_tsv
}


def make_skill_summaries(
        data_dir="../data", render_dir="../render", template_dir="../templates"
):
    database = {}
    # Load all the files in the data directory, creating a dictionary with a list per file (as if a database)
    for filename in os.listdir(data_dir):
        parts = os.path.splitext(os.path.basename(filename))
        table = parts[0]
        extension = parts[1]
        file = open(os.path.join(data_dir, filename), "r")
        database[table] = file_parsers[extension](file)
    # Create a folder, ignoring prior existence, to store the renders
    try:
        os.mkdir(os.path.join(render_dir))
    except FileExistsError:
        pass
    # Go around each sub-folder of the templates directory
    for table in os.listdir(template_dir):
        # Create a folder, ignoring prior existence, to store the renders of each table
        try:
            os.mkdir(os.path.join(render_dir, table))
        except FileExistsError:
            pass
        # Open each template file and each record
        for template_file in os.listdir(os.path.join(template_dir, table)):
            template = open(os.path.join(template_dir, table, template_file), "r").read()
            for record_number in range(0, len(database[table])):
                # Create a folder, ignoring prior existence, to store the renders of each record
                try:
                    os.mkdir(os.path.join(render_dir, table, str(record_number)))
                except FileExistsError:
                    pass
                # Clone the string so we don't mutate it for subsequent iterations
                render = template
                # Inject the values from the record in the render
                for field in database[table][record_number]:
                    render = render.replace("{{" + field.strip() + "}}", database[table][record_number][field])
                # Write the file
                render_file = open(os.path.join(render_dir, table, str(record_number), template_file), "w")
                render_file.write(render)


if __name__ == "__main__":
    make_skill_summaries()
