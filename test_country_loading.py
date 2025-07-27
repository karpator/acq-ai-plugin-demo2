#!/usr/bin/env python3
"""
Test script to demonstrate country-specific plugin loading.
"""

import os
import subprocess
import sys


def run_test(test_name: str, country_code: str, expected_greeting: str):
    """Run a test case for a specific country."""
    print(f"\n{'=' * 60}")
    print(f"TEST: {test_name}")
    print(f"Country: {country_code}")
    print(f"Expected greeting pattern: {expected_greeting}")
    print("=" * 60)

    # Run the main script with the country code
    try:
        result = subprocess.run(
            [sys.executable, "main.py", country_code],
            capture_output=True,
            text=True,
            timeout=30,
        )

        print("STDOUT:")
        print(result.stdout)

        if result.stderr:
            print("STDERR:")
            print(result.stderr)

        print(f"Return code: {result.returncode}")

        # Check if expected greeting is in output
        if expected_greeting.lower() in result.stdout.lower():
            print(f"✅ SUCCESS: Found expected greeting pattern '{expected_greeting}'")
        else:
            print(
                f"❌ FAILURE: Expected greeting pattern '{expected_greeting}' not found"
            )

        return result.returncode == 0

    except subprocess.TimeoutExpired:
        print("❌ FAILURE: Test timed out")
        return False
    except Exception as e:
        print(f"❌ FAILURE: {e}")
        return False


def test_environment_variable():
    """Test loading country from environment variable."""
    print(f"\n{'=' * 60}")
    print("TEST: Environment Variable Country Selection")
    print("=" * 60)

    # Set environment variable
    env = os.environ.copy()
    env["PLUGIN2_COUNTRY"] = "hu"

    try:
        result = subprocess.run(
            [sys.executable, "main.py"],
            capture_output=True,
            text=True,
            timeout=30,
            env=env,
        )

        print("STDOUT:")
        print(result.stdout)

        if result.stderr:
            print("STDERR:")
            print(result.stderr)

        print(f"Return code: {result.returncode}")

        # Check if Hungarian greeting is used
        if "szia" in result.stdout.lower():
            print("✅ SUCCESS: Hungarian greeting loaded from environment variable")
            return True
        else:
            print("❌ FAILURE: Expected Hungarian greeting not found")
            return False

    except Exception as e:
        print(f"❌ FAILURE: {e}")
        return False


def test_config_file():
    """Test loading country from config file."""
    print(f"\n{'=' * 60}")
    print("TEST: Config File Country Selection")
    print("=" * 60)

    # Create temporary config file
    config_file = "country_config.txt"
    try:
        with open(config_file, "w") as f:
            f.write("cz")

        result = subprocess.run(
            [sys.executable, "main.py"], capture_output=True, text=True, timeout=30
        )

        print("STDOUT:")
        print(result.stdout)

        if result.stderr:
            print("STDERR:")
            print(result.stderr)

        print(f"Return code: {result.returncode}")

        # Check if Czech greeting is used
        if "ahoj" in result.stdout.lower():
            print("✅ SUCCESS: Czech greeting loaded from config file")
            return True
        else:
            print("❌ FAILURE: Expected Czech greeting not found")
            return False

    except Exception as e:
        print(f"❌ FAILURE: {e}")
        return False
    finally:
        # Clean up config file
        if os.path.exists(config_file):
            os.remove(config_file)


def main():
    """Run all tests."""
    print("Starting Plugin2 Country-Specific Loading Tests")
    print(f"Python: {sys.executable}")
    print(f"Working directory: {os.getcwd()}")

    tests_passed = 0
    total_tests = 0

    # Test 1: Czech Republic
    total_tests += 1
    if run_test("Czech Republic Plugin", "cz", "Ahoj"):
        tests_passed += 1

    # Test 2: Hungary
    total_tests += 1
    if run_test("Hungary Plugin", "hu", "Szia"):
        tests_passed += 1

    # Test 3: Invalid country
    total_tests += 1
    print(f"\n{'=' * 60}")
    print("TEST: Invalid Country Code")
    print("=" * 60)
    try:
        result = subprocess.run(
            [sys.executable, "main.py", "invalid"],
            capture_output=True,
            text=True,
            timeout=30,
        )

        print("STDOUT:")
        print(result.stdout)

        if result.stderr:
            print("STDERR:")
            print(result.stderr)

        print(f"Return code: {result.returncode}")

        if result.returncode != 0:
            print("✅ SUCCESS: Invalid country code properly rejected")
            tests_passed += 1
        else:
            print("❌ FAILURE: Invalid country code should have failed")

    except Exception as e:
        print(f"❌ FAILURE: {e}")

    # Test 4: Environment variable
    total_tests += 1
    if test_environment_variable():
        tests_passed += 1

    # Test 5: Config file
    total_tests += 1
    if test_config_file():
        tests_passed += 1

    # Summary
    print(f"\n{'=' * 60}")
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Tests passed: {tests_passed}/{total_tests}")

    if tests_passed == total_tests:
        print("🎉 All tests passed!")
        return 0
    else:
        print("❌ Some tests failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
