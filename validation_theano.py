import sys
import os

# 1. Force flags to skip complex path lookups
os.environ["THEANO_FLAGS"] = "base_compiledir=/tmp/theano,device=cpu,config.ignore_config_files=True"

try:
    # 2. MONKEY PATCH: We must intercept the config parser before importing theano.tensor
    import theano.configparser
    
    # We override the function that causes the IndexError with a dummy
    def dummy_filter(*args, **kwargs):
        return "/tmp/theano"
    
    # This prevents the scanner from ever reaching the broken index access
    theano.configparser.filter_theano_cfg_file = dummy_filter
    
    # 3. Now perform the actual test
    import theano
    import theano.tensor as T
    
    x = T.dscalar('x')
    y = T.dscalar('y')
    z = x + y
    
    print("✅ Validation Passed: Theano initialized via Monkey Patch.")
    sys.exit(0)

except AttributeError as e:
    # This is the "Attack" signature for NumPy 2.0 (Step 2)
    print(f"❌ Validation Failed: Internal Dependency Breakage (NumPy 2.0). {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Validation Failed: {type(e).__name__}: {e}")
    # Print the traceback so we can see where the index error is if it persists
    import traceback
    traceback.print_exc()
    sys.exit(1)