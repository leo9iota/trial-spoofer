#!/usr/bin/env python3
"""
Feature Input Demo - Show the input system with default 'n' for all features
"""

import sys
from pathlib import Path

# Add src to path so we can import from ui
sys.path.append(str(Path(__file__).parent.parent))

from ui.input import FeatureInputManager


def demo_with_defaults():
    """Demo showing all features defaulting to 'n'."""
    print("🎯 Demo: Feature Input with Default 'n'")
    print("=" * 50)
    print("This demo shows how all features default to 'n' (no)")
    print("You can press Enter to accept defaults or type 'y' to select features")
    print()

    manager = FeatureInputManager()

    # Collect inputs (all default to 'n')
    selections = manager.collect_feature_inputs()

    # Show final confirmation
    if manager.confirm_proceed():
        print("\n✅ User confirmed to proceed with selected operations")

        # Show what would be executed
        selected_features = manager.get_selected_features()
        if selected_features:
            print(f"\n🚀 Would execute {len(selected_features)} operations:")
            for feature in selected_features:
                print(f"  • {feature}")
        else:
            print("\n⚠️ No operations would be executed")
    else:
        print("\n❌ User cancelled operations")

    return selections


def show_feature_details():
    """Show details about each feature."""
    manager = FeatureInputManager()

    print("\n" + "=" * 60)
    print("📋 FEATURE DETAILS:")
    print("=" * 60)

    for i, feature in enumerate(manager.features, 1):
        print(f"{i}. {feature['name']} [{feature['risk_level']}]")
        print(f"   Description: {feature['description']}")
        print(f"   Prompt: {feature['prompt']}")
        print(f"   Default: No (n)")
        print()


def main():
    """Run the feature input demo."""
    try:
        # Show feature details first
        show_feature_details()

        # Run the demo
        selections = demo_with_defaults()

        # Show final results
        print("\n" + "=" * 60)
        print("📊 FINAL RESULTS:")
        print("=" * 60)

        selected_count = sum(selections.values())
        total_count = len(selections)

        print(f"Selected: {selected_count}/{total_count} features")
        print()

        for feature, selected in selections.items():
            status = "✅ SELECTED" if selected else "❌ SKIPPED"
            print(f"  {feature}: {status}")

        print("\n🎉 Demo completed!")

    except KeyboardInterrupt:
        print("\n\n❌ Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()
