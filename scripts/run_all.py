import subprocess
import sys
import os

def run_script(script_name):
    script_path = os.path.join(os.path.dirname(__file__), script_name)
    print(f"--- Running {script_name} ---")
    try:
        result = subprocess.run([sys.executable, script_path], check=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("Errors/Warnings:", result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_name}:")
        print(e.stdout)
        print(e.stderr)
        sys.exit(1)

def main():
    print("Starting End-to-End Workflow...")
    
    # 1. Inspection (Optional, but good for logging)
    run_script('inspection.py')
    
    # 2. Load Data (Raw -> SQLite)
    run_script('load_data.py')
    
    # 3. Clean Data (Raw -> Processed CSV)
    run_script('clean_data.py')
    
    # 4. Analysis (Processed CSV -> Results)
    run_script('analysis.py')
    
    print("--- Workflow Completed Successfully ---")

if __name__ == "__main__":
    main()
