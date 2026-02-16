import sys
import os

# TRICK: Disable Theano's broken config-scanning to avoid the IndexError
os.environ["THEANO_FLAGS"] = "base_compiledir=/tmp/theano,device=cpu"

def test_theano_resurrection():
    try:
        # THE TRIPWIRE: 
        # In the 2026 Attack (NumPy 2.0), this import will crash 
        # because Theano calls np.complex, np.bool, etc.
        import theano
        import theano.tensor as T
        
        # Simple symbolic test
        x = T.dscalar('x')
        y = T.dscalar('y')
        z = x + y
        
        print("✅ Validation Passed: Theano initialized.")
        return True
        
    except IndexError:
        # If we still hit the path error, we can't test NumPy yet.
        # But this usually only happens if the environment is totally mangled.
        print("❌ Validation Failed: Legacy Path/Config Error (IndexError).")
        sys.exit(1)
    except AttributeError as e:
        # This is the "Attack" signature we want for the paper!
        print(f"❌ Validation Failed: Internal Dependency Breakage (NumPy 2.0). {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Validation Failed: {type(e).__name__}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_theano_resurrection()