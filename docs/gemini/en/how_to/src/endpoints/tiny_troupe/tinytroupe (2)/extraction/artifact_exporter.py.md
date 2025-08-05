**Instructions for Generating Code Documentation**

1. **Analyze the Code**: Understand the logic and actions performed by the code snippet.

2. **Create a Step-by-Step Guide**:
    - **Description**: Explain what the code block does.
    - **Execution Steps**: Describe the sequence of actions in the code.
    - **Usage Example**: Provide a code example of how to use the snippet in the project.

3. **Example**:

How to Use the `ArtifactExporter` Class
=========================================================================================

Description
-------------------------
The `ArtifactExporter` class is responsible for exporting artifacts from TinyTroupe elements, such as simulation results, to various file formats. It handles different content types and formats, including JSON, text, and DOCX.

Execution Steps
-------------------------
1. **Initialization:** Create an instance of the `ArtifactExporter` class with a base output folder path.
2. **Export Artifact:** Call the `export` method to save artifact data to a file. The method takes the artifact name, data, content type, optional content format, target format, and a flag for verbose output.
3. **Data Handling:** The `export` method prepares the artifact data by dedenting it, cleaning the artifact name, and choosing the appropriate export function based on the target format.
4. **Export Functions:**  The `_export_as_txt`, `_export_as_json`, and `_export_as_docx` methods handle the specific file format conversions.
5. **File Path Composition:** The `_compose_filepath` method constructs the file path for the exported artifact based on the base output folder, content type, and artifact name.

Usage Example
-------------------------

```python
from tinytroupe.extraction import ArtifactExporter

# Initialize the Artifact Exporter with a base output folder
exporter = ArtifactExporter("path/to/output/folder")

# Example artifact data
artifact_name = "simulation_results"
artifact_data = {
    "content": "This is the simulation output.\nIt contains important data.",
    "metadata": {"model": "SimulationModel", "version": "1.0"}
}

# Export the artifact as a JSON file
exporter.export(
    artifact_name=artifact_name,
    artifact_data=artifact_data,
    content_type="simulation",
    target_format="json",
    verbose=True
)

# Export the artifact as a DOCX file
exporter.export(
    artifact_name="documentation",
    artifact_data="This is the documentation for the simulation.\nIt is written in Markdown.",
    content_type="documentation",
    content_format="markdown",
    target_format="docx"
)
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".