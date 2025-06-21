#!/usr/bin/env python3

# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

"""
Comprehensive example runner that discovers and executes all example scripts.
This script walks the examples directory and runs each main.py file in series.
"""

import os
import sys
import subprocess
import time
from pathlib import Path


def find_example_scripts():
    """Find all main.py files in the examples directory."""
    examples_dir = Path(__file__).parent
    example_scripts = []

    # Walk through all subdirectories to find main.py files
    for root, dirs, files in os.walk(examples_dir):
        if 'main.py' in files:
            script_path = Path(root) / 'main.py'
            # Skip the all.py script itself
            if script_path.name != 'all.py' and script_path != Path(__file__):
                relative_path = script_path.relative_to(examples_dir.parent)
                example_scripts.append(str(relative_path))

    # Sort for consistent execution order
    return sorted(example_scripts)


def should_skip_example(script_path):
    """Check if an example should be skipped (e.g., requires special setup)."""
    skip_patterns = [
        # Skip microphone examples that require audio input
        'microphone',
        # Skip callback examples that require running servers
        'callback',
        # Skip agent examples that might require special setup
        'agent',
        # Skip async examples for now to avoid complexity
        'async',
        # Skip examples that require special dependencies
        'hello_world_play',  # requires sounddevice
    ]

    return any(pattern in script_path.lower() for pattern in skip_patterns)


def run_example(script_path):
    """Run a single example script and return success/failure."""
    print(f"\n{'='*80}")
    print(f"🔸 Running: {script_path}")
    print(f"{'='*80}")

    try:
        # Run the script and capture output in real-time
        process = subprocess.Popen(
            [sys.executable, script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )

        # Stream output in real-time
        output_lines = []
        while True:
            line = process.stdout.readline()
            if line:
                print(line.rstrip())
                output_lines.append(line)
            elif process.poll() is not None:
                break

        # Wait for process to complete
        return_code = process.wait()

        if return_code == 0:
            print(f"✅ SUCCESS: {script_path}")
            return True, output_lines
        else:
            print(f"❌ FAILED: {script_path} (exit code: {return_code})")
            return False, output_lines

    except Exception as e:
        print(f"❌ ERROR running {script_path}: {e}")
        return False, [str(e)]


def main():
    """Main function to discover and run all examples."""
    print("🚀 Deepgram SDK - Example Runner")
    print("Discovering and executing all example scripts...")

    # Check for API key
    if not os.getenv("DG_API_KEY"):
        print("❌ DG_API_KEY environment variable not set")
        print("Please set your Deepgram API key in the .env file")
        return 1

    start_time = time.time()

    # Find all example scripts
    scripts = find_example_scripts()
    print(f"\n📋 Found {len(scripts)} example scripts")

    # Filter out scripts that should be skipped
    runnable_scripts = [s for s in scripts if not should_skip_example(s)]
    skipped_scripts = [s for s in scripts if should_skip_example(s)]

    if skipped_scripts:
        print(
            f"⏭️  Skipping {len(skipped_scripts)} scripts requiring special setup:")
        for script in skipped_scripts:
            print(f"   - {script}")

    print(f"\n🏃 Running {len(runnable_scripts)} example scripts:")
    for script in runnable_scripts:
        print(f"   - {script}")

    # Run each script
    success_count = 0
    failed_scripts = []

    for i, script in enumerate(runnable_scripts, 1):
        print(f"\n📍 [{i}/{len(runnable_scripts)}]")

        success, output = run_example(script)

        if success:
            success_count += 1
        else:
            failed_scripts.append((script, output))
            # Stop on first failure
            print(f"\n🛑 Stopping execution due to failure in: {script}")
            break

        # Small delay between examples
        time.sleep(1)

    # Summary
    elapsed = time.time() - start_time
    print(f"\n{'='*80}")
    print(f"📊 EXECUTION SUMMARY")
    print(f"{'='*80}")
    print(f"⏱️  Total time: {elapsed:.1f} seconds")
    print(f"✅ Successful: {success_count}/{len(runnable_scripts)}")
    print(f"❌ Failed: {len(failed_scripts)}")
    print(f"⏭️  Skipped: {len(skipped_scripts)}")

    if failed_scripts:
        print(f"\n❌ FAILED SCRIPTS:")
        for script, output in failed_scripts:
            print(f"   - {script}")
        return 1
    else:
        print(
            f"\n🎉 All {success_count} runnable examples executed successfully!")
        return 0


if __name__ == "__main__":
    sys.exit(main())
