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
    """Generate the demo dashboard."""

    # Remove the previously generated demo completely.
    # This also removes views that no longer exist in a newer release.
    if target.exists():
        shutil.rmtree(target)

    # Copy the complete demo directory from the integration package.
    shutil.copytree(source, target)

    # Process every YAML file recursively.
    #
    # This includes:
    #   dashboard.yaml
    #   views/view-horseshoes.yml
    #   views/view-electricity.yml
    #   views/anything-else.yml
    #
    # Subdirectories do not matter.
    for file in target.rglob("*"):
        if not file.is_file():
            continue

        if file.suffix.lower() not in (".yaml", ".yml"):
            continue

        text = file.read_text(encoding="utf-8")

        # Replace all entity placeholders with the entities selected
        # by the user in the Home Assistant config/options flow.
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


def remove_demo(target: Path) -> None:
    """Remove the generated demo dashboard."""

    if target.exists():
        shutil.rmtree(target)
