import subprocess
import time
import sys

def run_script(script_name):
    try:
        start_time = time.time()
        print(f"Starting {script_name}...")
        result = subprocess.run([sys.executable, script_name], check=True)
        end_time = time.time()
        duration = end_time - start_time
        print('====================================')
        print(f"{script_name} completed in {duration:.2f} seconds.")
        print('====================================')
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running {script_name}: {e}")
        return False

def main():
    total_start_time = time.time()
    
    # Step 1: Call get_data.py
    if run_script('get_data.py'):
        print("get_data.py ran successfully.")
        
        # Step 2: Call process_data.py
        if run_script('clean_data.py'):
            print("clean_data.py ran successfully.")
            
            # Step 3: Call visualize_data.py
            if run_script('visualize_results.py'):
                print("visualize_results.py ran successfully.")
                print("====================================")
                print("All scripts ran successfully!")
            else:
                print("visualize_results.py failed.")
        else:
            print("clean_data.py failed.")
    else:
        print("get_data.py failed.")
    
    total_end_time = time.time()
    total_duration = total_end_time - total_start_time
    print(f"Total time taken for all scripts: {total_duration:.2f} seconds.")

if __name__ == "__main__":
    main()