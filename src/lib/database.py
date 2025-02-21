import os


class Database:
    def __init__(self, base_path: str = os.getcwd()):
        self.base_path = base_path
        self.db_path = f"{self.base_path}/db.ceg"
        self.__create_db_if_not_exists()
        self.__parse_tables()
        pass

    def __create_db_if_not_exists(self):
        exists = os.path.isfile(self.db_path)
        if not exists:
            with open(self.db_path, "w") as f:
                f.write("")
                f.close()

    def __read_db(self):
        data = ""
        with open(self.db_path, "r") as f:
            data = f.read()
            f.close()
        return data

    def __parse_tables(self):
        data = self.__read_db()
        lines = data.split("\n")

        tables = []
        last_table = None

        for line in lines:
            start_table = line.startswith("START TABLE")
            end_table = line.startswith("END TABLE")
            schema_table = line.startswith("TABLE SCHEMA")

            if start_table and not last_table:
                table_name = line.split(" ")[2]
                last_table = {
                    "name": table_name,
                    "schema": [],
                    "data": [],
                }
                continue

            if schema_table:
                table_schema_definition = line[13:]
                table_schema = table_schema_definition.split(",")
                last_table["schema"] = table_schema
                continue

            if not (start_table or end_table or schema_table) and last_table:
                if len(last_table["schema"]) == 0:
                    raise Exception(
                        f"Schema da tabela {last_table['name']} não encontrado."
                    )

                if "data" not in last_table:
                    last_table["data"] = []

                line_data = line.split(",")
                line_data_structured = {}
                for [i, field] in enumerate(last_table["schema"]):
                    line_data_structured[field] = line_data[i]

                last_table["data"].append(line_data_structured)

            if end_table:
                tables.append(last_table)
                last_table = None
                continue

        return tables

    def __write_table_lines(self, table_name: str, new_data: list[list[str]]):
        data = self.__read_db()
        lines = data.split("\n")

        start_index = None
        schema_index = None
        end_index = None

        for i, line in enumerate(lines):
            if line.startswith("START TABLE"):
                parts = line.split()
                if len(parts) >= 3 and parts[2] == table_name:
                    start_index = i
            if start_index is not None and line.startswith("TABLE SCHEMA"):
                schema_index = i
            if start_index is not None and line.startswith("END TABLE"):
                end_index = i
                break

        if start_index is None or schema_index is None or end_index is None:
            raise Exception(f"Tabela {table_name} não encontrada.")

        formatted_data_lines = []
        for row in new_data:
            formatted_row = ",".join([
                value if (value.startswith('"') and value.endswith('"'))
                else f'"{value}"'
                for value in row
            ])
            formatted_data_lines.append(formatted_row)

        updated_lines = lines[:schema_index+1] + \
            formatted_data_lines + lines[end_index:]

        with open(self.db_path, "w") as f:
            f.write("\n".join(updated_lines))

    def __strip_quotes(self, value: str) -> str:
        if value.startswith('"') and value.endswith('"'):
            return value[1:-1]

        return str(value)

    def get_table(self, table_name: str):
        tables = self.__parse_tables()
        for table in tables:
            if table["name"] == table_name:
                return table

        return None

    def create(self, table_name: str, data: dict):
        table = self.get_table(table_name)
        if not table:
            raise Exception(f"Tabela {table_name} não encontrada.")

        table_schema = table["schema"]
        table_data = table["data"]

        rows = []
        for row in table_data:
            rows.append([row[field] for field in table_schema])

        new_row = []
        for field in table_schema:
            if field not in data:
                raise Exception(
                    f"Campo {field} não encontrado para a tabela {table_name}."
                )
            new_row.append(data[field])

        rows.append(new_row)
        self.__write_table_lines(table_name, rows)

    def update(self, table_name: str, key_field: str, key_value: str, new_data: dict):
        table = self.get_table(table_name)
        if not table:
            raise Exception(f"Tabela {table_name} não encontrada.")
        if key_field not in table["schema"]:
            raise Exception(
                f"Campo {key_field} não existe na tabela {table_name}."
            )

        found = False
        for row in table["data"]:
            stored_val = self.__strip_quotes(row[key_field])

            if stored_val == key_value:
                for k, v in new_data.items():
                    if k in table["schema"]:
                        row[k] = str(v)

                found = True
                break

        if not found:
            raise Exception("Registro não encontrado para atualização.")

        rows = []
        for row in table["data"]:
            rows.append([row[field] for field in table["schema"]])

        self.__write_table_lines(table_name, rows)

    def delete(self, table_name: str, key_field: str, key_value: str):
        table = self.get_table(table_name)
        if not table:
            raise Exception(f"Tabela {table_name} não encontrada.")
        if key_field not in table["schema"]:
            raise Exception(
                f"Campo {key_field} não existe na tabela {table_name}."
            )

        initial_length = len(table["data"])
        table["data"] = [
            row for row in table["data"]
            if self.__strip_quotes(row[key_field]) != key_value
        ]

        if len(table["data"]) == initial_length:
            raise Exception("Registro não encontrado para deleção.")

        rows = []
        for row in table["data"]:
            rows.append([row[field] for field in table["schema"]])

        self.__write_table_lines(table_name, rows)

    def read(self, table_name: str, key_field: str, key_value: str) -> (dict | None):
        table = self.get_table(table_name)
        if not table:
            raise Exception(f"Tabela {table_name} não encontrada.")
        if key_field not in table["schema"]:
            raise Exception(
                f"Campo {key_field} não existe na tabela {table_name}."
            )

        for row in table["data"]:
            stored_val = self.__strip_quotes(row[key_field])

            if stored_val == key_value:
                return {field: self.__strip_quotes(row[field]) for field in table["schema"]}

        return None

    def read_all(self, table_name: str) -> list[dict]:
        table = self.get_table(table_name)
        if not table:
            raise Exception(f"Tabela {table_name} não encontrada.")

        rows = []
        for row in table["data"]:
            new_row = {
                field: self.__strip_quotes(row[field])
                for field in table["schema"]
            }
            rows.append(new_row)

        return rows
