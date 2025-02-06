from CLI import banner
from WalletWave.plugins.utils import plugin_manager


def menu(config_manager):
    pm = plugin_manager.PluginManager(config_manager=config_manager)
    pm.load_plugins()

    banner.print_wave_banner()

    while True:
        print("\n1. List Plugins")
        print("2. Run Plugin")
        print("0. Exit")

        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if choice == 0:
            print("Goodbye!")
            return "exit"
        elif choice == 1:
            # List available plugins
            print("\nAvailable Plugins:")
            if not pm.plugins:
                print("No plugins found.")
            else:
                pm.list_plugins()
        elif choice == 2:
            if not pm.plugins:
                print("\nNo plugins to run. Please add plugins to the directory.")
                continue

            print("\nAvailable Plugins:")
            pm.list_plugins()

            plugin_choice = input("Select a plugin by number: ")
            try:
                plugin_choice = int(plugin_choice)
                if plugin_choice < 1 or plugin_choice > len(pm.plugins):
                    print("Invalid plugin number.")
                    continue

                selected_plugin = pm.plugins[plugin_choice - 1]
                print(f"Selected Plugin: {selected_plugin.get_name()}")
                return "plugin", selected_plugin
            except ValueError:
                print("Invalid input. Please enter a number.")
        else:
            print("Invalid choice.")


