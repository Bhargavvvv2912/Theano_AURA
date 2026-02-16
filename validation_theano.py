import sys
import os

# Disable the noisy config scanning
os.environ["THEANO_FLAGS"] = "base_compiledir=/tmp/theano,device=cpu,config.ignore_config_files=True"

def test_theano_resurrection():
    try:
        # If the patch worked, this will now pass the version check
        import theano
        import theano.tensor as T
        
        # Fundamental scalar addition
        x = T.dscalar('x')
        y = T.dscalar('y')
        z = x + y
        
        print("✅ Validation Passed: Theano engine successfully initialized.")
        return True
        
    except AttributeError as e:
        # This is the "Attack" signature for NumPy 2.0 (Step 2)
        print(f"❌ Validation Failed: Internal Dependency Breakage (NumPy 2.0). {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Validation Failed: {type(e).__name__}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_theano_resurrection()