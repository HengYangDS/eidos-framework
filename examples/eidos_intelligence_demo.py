import asyncio
from eidos.system.sidecar import Sidecar
from eidos.intelligence.driver import OpenAIDriver

async def main():
    print("=== Eidos Intelligence Demo ===")
    
    # 1. Initialize Intelligence Components
    driver = OpenAIDriver(api_key="mock-key")
    sidecar = Sidecar(driver=driver)
    
    # 2. Simulate an Error
    try:
        print("\n[System] Running pipeline...")
        # Simulate a runtime error
        raise ValueError("SchemaMismatch: Column 'price' expects float, got string '$100'")
    except Exception as e:
        # 3. Trigger Sidecar Healing
        print(f"\n[System] Caught error. Invoking Sidecar...")
        diagnosis = await sidecar.heal(e, context={"pipeline_id": "alpha-v1"})
        
        print(f"\n[System] Received diagnosis: {diagnosis}")
        
        # 4. Simulate Patching
        print("[System] Applying patch... (Simulated)")
        print("[System] Pipeline recovered.")

if __name__ == "__main__":
    asyncio.run(main())
