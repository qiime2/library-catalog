// TODO: If the parser is ever updated this will need to be updated as well
import yaml from "js-yaml"
import fs from "fs";
import path from "path";
import { get_parser } from "./parser.js";

const PARSER = get_parser();
const ERROR_DIR = "./library-catalog/errors";
const ERROR_FILES = fs.readdirSync(ERROR_DIR);
const EXPECTED_KEYS = new Set(["name", "query", "date", "description"]);

function setsEqual(setA, setB) {
    return setA.size === setB.size &&
                [...setA].every(value => setB.has(value));
}

for (const file of ERROR_FILES) {
    let loaded_yaml;

    // Make sure the file loads as yaml
    try {
        loaded_yaml = yaml.load(fs.readFileSync(path.join(ERROR_DIR, file), 'utf8'));
    } catch (error) {
        throw new Error(`The file '${file}' failed to parse as yaml:\n\n${error.message}`);
    }

    for (const loaded_error of loaded_yaml) {
        // Make sure all errors in the file have the correct keys
        const found_keys = new Set(Object.keys(loaded_error));

        if (!setsEqual(EXPECTED_KEYS, found_keys)) {
            throw new Error(`The error:\n\n${loaded_error}\n\nFrom the file '${file}'
                does not contain the expected keys.\n\nExpected keys are:
                ${EXPECTED_KEYS}\nKeys found: ${found_keys}`);
        }

        // Make sure all queries in the file can be parsed
        try {
            PARSER.parse(loaded_error.query);
        } catch (error) {
            throw new Error(`The query '${loaded_error.query}' for the error '${loaded_error.name}' from the file: '${file}'
                failed to parse.\n\n${error.message}`);
        }
    }
}
