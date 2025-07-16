#!/usr/bin/env python3
"""
Integration Example - How to use the FeatureInputManager in your main application
"""

import sys
from pathlib import Path

# Add src to path so we can import from ui
sys.path.append(str(Path(__file__).parent.parent))

from ui.input import FeatureInputManager


def simulate_operations(selected_features: list[str]) -> dict[str, bool]:
    """Simulate running the selected operations."""
    import random
    import time

    results = {}

    print("\n🚀 Executing selected operations...")
    print("=" * 50)

    for feature in selected_features:
        print(f"🔄 Processing {feature}...")

        # Simulate work
        time.sleep(0.5)

        # Random success/failure for demo (90% success rate)
        success = random.choice([True] * 9 + [False])
        results[feature] = success

        status = "✅ Success" if success else "❌ Failed"
        print(f"   {status}")

    return results


def main():
    """Example of how to integrate FeatureInputManager into your main app."""
    print("🔒 VSCode Spoofer - Integration Example")
    print("=" * 60)
    print("This shows how to integrate the FeatureInputManager into your main app")
    print()

    try:
        # Step 1: Create the input manager
        manager = FeatureInputManager()

        # Step 2: Collect user input for all features (defaults to 'n')
        print("Step 1: Collecting user input...")
        selections = manager.collect_feature_inputs()

        # Step 3: Get the list of selected features
        selected_features = manager.get_selected_features()

        # Step 4: Confirm before proceeding
        if not manager.confirm_proceed():
            print("\n❌ Operations cancelled by user")
            return

        # Step 5: Execute the selected operations
        if selected_features:
            results = simulate_operations(selected_features)

            # Step 6: Show final results
            print("\n📊 Final Results:")
            print("=" * 30)

            success_count = sum(results.values())
            total_count = len(results)

            for feature, success in results.items():
                status = "✅ Success" if success else "❌ Failed"
                print(f"  {feature}: {status}")

            print(f"\nSummary: {success_count}/{total_count} operations successful")

            if success_count == total_count:
                print("🎉 All operations completed successfully!")
            elif success_count > 0:
                print("⚠️ Some operations failed")
            else:
                print("❌ All operations failed")
        else:
            print("\n⚠️ No operations to execute")

        print("\n✅ Application completed")

    except KeyboardInterrupt:
        print("\n\n❌ Application interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")


def show_usage_example():
    """Show code example of how to use the FeatureInputManager."""
    print("\n" + "=" * 60)
    print("💡 USAGE EXAMPLE:")
    print("=" * 60)
    print("""
# In your main application:

from ui.input import FeatureInputManager

def main():
    # Create input manager
    manager = FeatureInputManager()
    
    # Collect user input (all features default to 'n')
    selections = manager.collect_feature_inputs()
    
    # Get selected features
    selected_features = manager.get_selected_features()
    
    # Confirm before proceeding
    if manager.confirm_proceed():
        # Execute your operations
        for feature in selected_features:
            if feature == "MAC Address":
                spoof_mac_addr()
            elif feature == "Machine ID":
                spoof_machine_id()
            # ... etc
    
    # The selections dict contains:
    # {
    #     "MAC Address": True/False,
    #     "Machine ID": True/False,
    #     "Filesystem UUID": True/False,
    #     "Hostname": True/False,
    #     "VS Code Caches": True/False,
    #     "New User": True/False
    # }
""")


if __name__ == "__main__":
    show_usage_example()
    main()
