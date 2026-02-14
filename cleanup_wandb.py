#!/usr/bin/env python3
"""Clean up old W&B runs - keep only latest meaningful runs"""
import wandb
import os
from dotenv import load_dotenv

load_dotenv()

api = wandb.Api()
entity = os.getenv('WANDB_ENTITY', 'kakarlagana18-iihmr')

print("Cleaning up W&B runs...")
print("=" * 60)

# Projects to clean
projects = [
    "burnout-prediction",
    "burnout-prediction-live",
    "burnout-test"
]

for project_name in projects:
    print(f"\nProject: {project_name}")
    print("-" * 60)
    
    try:
        runs = api.runs(f"{entity}/{project_name}")
        
        # Separate meaningful and random-named runs
        meaningful_runs = []
        random_runs = []
        
        for run in runs:
            # Check if run has meaningful name (contains underscore and numbers)
            if '_' in run.name and any(char.isdigit() for char in run.name):
                meaningful_runs.append(run)
            else:
                random_runs.append(run)
        
        print(f"Total runs: {len(runs)}")
        print(f"Meaningful runs: {len(meaningful_runs)}")
        print(f"Random-named runs: {len(random_runs)}")
        
        # Delete random-named runs
        if random_runs:
            print(f"\nDeleting {len(random_runs)} random-named runs:")
            for run in random_runs:
                print(f"  - {run.name} (ID: {run.id})")
                run.delete()
            print(f"[OK] Deleted {len(random_runs)} runs")
        else:
            print("[OK] No random-named runs to delete")
        
        # Keep only latest 3 meaningful runs
        if len(meaningful_runs) > 3:
            # Sort by created time (newest first)
            meaningful_runs.sort(key=lambda x: x.created_at, reverse=True)
            runs_to_delete = meaningful_runs[3:]
            
            print(f"\nKeeping latest 3 runs, deleting {len(runs_to_delete)} older runs:")
            for run in runs_to_delete:
                print(f"  - {run.name} (ID: {run.id})")
                run.delete()
            print(f"[OK] Deleted {len(runs_to_delete)} old runs")
        
        # Show remaining runs
        remaining = api.runs(f"{entity}/{project_name}")
        print(f"\nRemaining runs: {len(list(remaining))}")
        for run in api.runs(f"{entity}/{project_name}"):
            print(f"  [OK] {run.name}")
            
    except Exception as e:
        print(f"[ERROR] {e}")

print("\n" + "=" * 60)
print("[SUCCESS] Cleanup complete!")
print("\nYour dashboards now show only the latest, meaningful runs.")
