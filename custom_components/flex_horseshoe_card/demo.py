for file in target.rglob("*"):
    if file.suffix not in (".yaml", ".yml"):
        continue

    text = file.read_text(encoding="utf-8")

    for placeholder, option in PLACEHOLDERS.items():
        entity_id = options.get(option)

        if entity_id:
            text = text.replace(placeholder, entity_id)

    file.write_text(text, encoding="utf-8")
