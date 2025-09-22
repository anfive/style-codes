import hashlib
import os
import json

def calculate_file_hash(file_path):
    """Calculate SHA256 hash of a file."""
    if not os.path.exists(file_path):
        return None
    
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def compare_json_dumps():
    """Compare JSON dump files from all three languages for each pen/sog combination."""
    languages = ['python', 'php', 'ts']
    pen_values = [0, 1, 10]
    sog_values = range(4)
    
    base_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'out')
    
    print("Comparing JSON dump files from Python, PHP, and TypeScript implementations...")
    print("=" * 80)
    
    all_match = True
    total_comparisons = 0
    successful_comparisons = 0
    
    for pen in pen_values:
        for sog in sog_values:
            print(f"\nChecking PEN={pen}, SOG={sog}:")
            
            # Get file paths for all three languages
            file_paths = {}
            hashes = {}
            
            for lang in languages:
                filename = f"style_codes_v2a_{lang}_pen={pen}_sog={sog}.json"
                file_path = os.path.join(base_dir, filename)
                file_paths[lang] = file_path
                
                # Calculate hash
                file_hash = calculate_file_hash(file_path)
                hashes[lang] = file_hash
                
                if file_hash is None:
                    print(f"  ❌ {lang.upper()}: File not found - {filename}")
                else:
                    print(f"  ✓ {lang.upper()}: {file_hash[:16]}... ({os.path.getsize(file_path)} bytes)")
            
            # Compare hashes
            total_comparisons += 1
            if all(h is not None for h in hashes.values()):
                unique_hashes = set(hashes.values())
                if len(unique_hashes) == 1:
                    print(f"  🎉 All three languages produce IDENTICAL output!")
                    successful_comparisons += 1
                else:
                    print(f"  ⚠️  MISMATCH detected!")
                    all_match = False
                    for lang, hash_val in hashes.items():
                        print(f"    {lang.upper()}: {hash_val}")
            else:
                print(f"  ❌ Cannot compare - missing files")
                all_match = False
    
    print("\n" + "=" * 80)
    print("SUMMARY:")
    print(f"Total combinations checked: {total_comparisons}")
    print(f"Successful comparisons: {successful_comparisons}")
    
    if all_match and successful_comparisons == total_comparisons:
        print("🎉 SUCCESS: All JSON dumps from all three languages are identical!")
    else:
        print("❌ FAILURE: Some files are missing or contain different data")
        
    return all_match and successful_comparisons == total_comparisons

def compare_file_contents_detailed(pen, sog):
    """Compare the actual JSON content of files for a specific pen/sog combination."""
    languages = ['python', 'php', 'ts']
    base_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'out')
    
    print(f"\nDetailed comparison for PEN={pen}, SOG={sog}:")
    
    contents = {}
    for lang in languages:
        filename = f"style_codes_v2a_{lang}_pen={pen}_sog={sog}.json"
        file_path = os.path.join(base_dir, filename)
        
        try:
            with open(file_path, 'r') as f:
                contents[lang] = json.load(f)
            print(f"  ✓ {lang.upper()}: Loaded {len(contents[lang])} entries")
        except FileNotFoundError:
            print(f"  ❌ {lang.upper()}: File not found")
            return False
        except json.JSONDecodeError as e:
            print(f"  ❌ {lang.upper()}: JSON decode error - {e}")
            return False
    
    # Compare keys
    all_keys = [set(content.keys()) for content in contents.values()]
    if not all(keys == all_keys[0] for keys in all_keys):
        print("  ❌ Different sets of keys found between languages")
        return False
    
    # Compare values for each key
    mismatches = 0
    for key in all_keys[0]:
        values = [contents[lang][key] for lang in languages]
        if not all(val == values[0] for val in values):
            mismatches += 1
            if mismatches <= 5:  # Show first 5 mismatches
                print(f"  ❌ Mismatch for key '{key}':")
                for lang, val in zip(languages, values):
                    print(f"    {lang.upper()}: {val}")
    
    if mismatches == 0:
        print("  🎉 All entries match perfectly!")
        return True
    else:
        print(f"  ❌ Found {mismatches} mismatched entries")
        return False

if __name__ == '__main__':
    success = compare_json_dumps()
    
    # If there are any issues, you can uncomment the line below to do detailed comparison
    # for a specific pen/sog combination:
    # compare_file_contents_detailed(0, 0)
    
    if success:
        print("\n✅ All tests passed! The three language implementations produce identical results.")
    else:
        print("\n❌ Some tests failed. Check the output above for details.")