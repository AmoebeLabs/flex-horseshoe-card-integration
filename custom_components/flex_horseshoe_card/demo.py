"""Generate the Flex Horseshoe Card demo dashboard."""

from pathlib import Path
import shutil

from .const import (
    CONF_TEMPERATURE_ENTITY,
    CONF_HUMIDITY_ENTITY,
    CONF_ENERGY_ENTITY,
    CONF_BATTERY_ENTITY,
    CONF_SWITCH_ENTITY,
)


PLACEHOLDERS = {
    "__FHS_TEMPERATURE__": CONF_TEMPERATURE_ENTITY,
    "__FHS_HUMIDITY__": CONF_HUMIDITY_ENTITY,
    "__FHS_ENERGY__": CONF_ENERGY_ENTITY,
    "__FHS_BATTERY__": CONF_BATTERY_ENTITY,
    "__FHS_SWITCH__": CONF_SWITCH_ENTITY,
}


def generate_demo(
    source: Path,
    target: Path,
    options: dict,
) -> None:
    """Copy the demo dashboard and replace entity placeholders."""

    # The generated demo directory belongs to FHS.
    # Always recreate it so removed/renamed demo files don't remain behind.
    if target.exists():
        shutil.rmtree(target)

    # Copy the complete demo dashboard:
    # dashboard.yaml + all views + any other files.
    shutil.copytree(source, target)

    # Walk through every YAML file recursively.
    # This includes dashboard.yaml and every view in subdirectories.
    for file in target.rglob("*"):
        if not file.is_file():
            continue

        if file.suffix.lower() not in (".yaml", ".yml"):
            continue

        text = file.read_text(encoding="utf-8")

        # Replace every occurrence of every configured entity placeholder.
        for placeholder, option_name in PLACEHOLDERS.items():
            entity_id = options.get(option_name)

            if entity_id:
                text = text.replace(
                    placeholder,
                    entity_id,
                )

        file.write_text(
            text,
            encoding="utf-8",
        )
