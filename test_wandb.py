#!/usr/bin/env python3
"""Test W&B integration"""
import wandb
import os
from dotenv import load_dotenv

load_dotenv()

print("Testing W&B Integration...")
print(f"API Key present: {bool(os.getenv('WANDB_API_KEY'))}")
print(f"Entity: {os.getenv('WANDB_ENTITY', 'kakarlagana18-iihmr')}")

try:
    # Initialize W&B
    run = wandb.init(
        entity=os.getenv('WANDB_ENTITY', 'kakarlagana18-iihmr'),
        project="burnout-test",
        config={
            "test": True,
            "version": "2.0.0"
        },
        tags=["test", "integration"]
    )
    
    print("\n✓ W&B initialized successfully!")
    print(f"  Run ID: {run.id}")
    print(f"  Run URL: {run.url}")
    
    # Log test metrics
    for i in range(5):
        wandb.log({
            "test_metric": i * 10,
            "accuracy": 0.8 + i * 0.02,
            "loss": 0.5 - i * 0.05
        })
    
    print("\n✓ Logged 5 test metrics")
    
    # Finish run
    run.finish()
    print("\n✓ W&B test completed successfully!")
    print(f"\nView results at: https://wandb.ai/{os.getenv('WANDB_ENTITY', 'kakarlagana18-iihmr')}/burnout-test")
    
except Exception as e:
    print(f"\n✗ W&B test failed: {e}")
    print("\nTroubleshooting:")
    print("1. Check WANDB_API_KEY in .env")
    print("2. Run: wandb login")
    print("3. Verify internet connection")
