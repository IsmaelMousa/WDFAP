## Modules

Here is a summary for the purpose of each major module or component in **WDFAP**:

|       Module       | Purpose                                                                                                                                                                                                                                    |
|:------------------:|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|      `tools`       | Provides utility functions and scripts for orchestrating the fetching, cleaning, labeling, and uploading of data from various sources. Initially includes a script for user interaction to fetch articles from Web Sources asynchronously. |
|     `sources`      | Provides modules for fetching articles asynchronously from different sources like Google News & Wikipedia.                                                                                                                                 |
|       `data`       | Storage Where fetched articles are stored in various formats such as `csv`, `json`, `xlsx` and `parquet`.                                                                                                                                  |
|      `errors`      | Prepares and customizes exceptions for handling specific issues.                                                                                                                                                                           |
|      `utils`       | Houses common utilities/logic utilized throughout the project.                                                                                                                                                                             |
|     `configs`      | Contains main configurations for both development and production stages.                                                                                                                                                                   |
|     `setup.py`     | Configures the project metadata and dependencies for streamlined installation.                                                                                                                                                             |
|     `main.py`      | Serves as the entry point, initiating the project.                                                                                                                                                                                         |
|     `Makefile`     | Provides commands for installing dependencies and running the application.                                                                                                                                                                 |
| `requierments.txt` | Lists all the required dependencies for running the application.                                                                                                                                                                           |

---

<div align="right">

**[Go Back ➡️](index.md)**

</div>