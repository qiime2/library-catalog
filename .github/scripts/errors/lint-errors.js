// TODO: If the parser is ever updated this will need to be updated as well
import yaml from "js-yaml"
import fs from "fs";
import path from "path";
import { get_parser } from "./parser.js";

const readBlobAsText = (blob) =>
  new Promise((resolve, reject) => {
    // eslint-disable-line no-unused-vars
    const reader = new FileReader();
    reader.onload = (event) => {
      // eslint-disable-line no-unused-vars
      resolve(reader.result);
    };
    reader.readAsText(blob, "utf8");
});

const PARSER = get_parser();
const ERROR_DIR = "./library-catalog/errors";
const ERROR_FILES = await fs.promises.readdir(ERROR_DIR);
const EXPECTED_KEYS = new Set("name", "query", "date", "description");

for (const file of ERROR_FILES) {
    let loaded_yaml;

    // Make sure the file loads as yaml
    try {
        loaded_yaml = yaml.safeLoad(path.join(ERROR_DIR, file));
    } catch (error) {
        throw new Error(`The file '${file}' failed to parse as yaml:\n\n${error.message}`);
    }

    for (error of loaded_yaml) {
        // Make sure all errors in the file have the correct keys
        if (new Set(Object.keys(error)).difference(EXPECTED_KEYS).size !== 0) {
            throw new Error(`The error:\n\n${error}\n\nFrom the file '${file}'
                does not contain the expected keys.\n\nExpected keys are:
                ${EXPECTED_KEYS}\nKeys found: ${new Set(Object.keys(error))}`);
        }

        // Make sure all queries in the file can be parsed
        try {
            PARSER.parse(error.query);
        } catch (error) {
            throw new Error(`The error:\n\n${error}\n\nFrom the file '${file}'
                failed to parse.\n\n${error.message}`);
        }
    }
}
