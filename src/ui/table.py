



    def features_table(self) -> Table:
        """Rich TUI table with available features"""
        table: Table = Table(
            title="🛡️ Available Security Features", show_header=True
        )
        table.add_column("Feature", style="cyan", no_wrap=True)
        table.add_column("Description", style="white")
        table.add_column("Risk Level", justify="center")

        features: list[tuple[str, str, str]] = [
            ("MAC Address", "Spoof network interface MAC", "🟢 Low"),
            ("Machine ID", "Regenerate system machine-id", "🟢 Low"),
            ("Filesystem UUID", "Randomize root filesystem UUID", "🟡 Medium"),
            ("Hostname", "Set random hostname", "🟢 Low"),
            ("VS Code Caches", "Purge editor caches", "🟢 Low"),
            ("New User", "Create sandbox user account", "🟢 Low"),
        ]

        for feature, desc, risk in features:
            table.add_row(feature, desc, risk)

        return table