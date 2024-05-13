import os
from dataclasses import dataclass
from functools import lru_cache

from yaml import safe_load, YAMLError

from errors import UnhandledError


@dataclass(frozen=True)
class SourcesConfig:
    """
    Represents the interface of the sources' configuration.
    """

    wiki: str
    google_news: str


@dataclass(frozen=True)
class Config:
    """
    Represents the interface of the base configurations.

    - sources: sources' configuration.
    """

    sources: SourcesConfig


@lru_cache(maxsize=1)
def get_config() -> Config:
    """
    Getting the base configurations.

    :return: instance of Config
    """

    base_path = os.path.dirname(os.path.abspath(__file__))

    environment = os.getenv("ENVIRONMENT")
    match environment:
        case "production":
            path = os.path.join(base_path, "../configs/config.prd.yml")
        case _:
            path = os.path.join(base_path, "../configs/config.dev.yml")

    try:
        with open(path, "r") as file:
            configurations: dict = safe_load(file)

            sources_cfg: dict = configurations.get("sources", {})

            sources = SourcesConfig(wiki=sources_cfg.get("wiki"),
                                    google_news=sources_cfg.get("google_news"))

            config = Config(sources=sources)

        return config

    except IOError:
        raise IOError(f"Unable to open the config file with path {path}")

    except YAMLError:
        raise YAMLError("Unable to parse the config file")

    except Exception as exc:
        raise UnhandledError(exc) from None
