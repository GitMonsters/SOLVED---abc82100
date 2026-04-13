import subprocess
import sys
import os

def run_verification(script_name):
    print(f"--- Running {script_name} ---")
    try:
        result = subprocess.run([sys.executable, script_name], capture_output=True, text=True)
        print(result.stdout)
        if result.returncode == 0:
            return True
        else:
            print(f"Error in {script_name}: {result.stderr}")
            return False
    except Exception as e:
        print(f"Failed to execute {script_name}: {e}")
        return False

def main():
    print("=========================================")
    print("   TranscendPlexity Reproducer Tool      ")
    print("=========================================")
    
    # 1. Verify Flagship Task
    success_flagship = run_verification("verify.py")
    
    # 2. Add placeholders for other batch verifiers if you have them
    # success_all = run_verification("verify_all.py") 

    print("\nVerification Summary:")
    print(f"Flagship (abc82100): {'✅ PASSED' if success_flagship else '❌ FAILED'}")
    
    if success_flagship:
        print("\nConclusion: Evidence is verified against ground truth task.json.")
    else:
        print("\nConclusion: Verification failed. Check local environment.")

if __name__ == "__main__":
    main()
