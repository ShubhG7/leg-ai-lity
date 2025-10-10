"""
Temp directory utilities for serverless-safe file handling.
"""

import os
import os.path as _path
import tempfile
import secrets
import string
from typing import Optional
from fastapi import HTTPException
import threading

# Cache the resolved temp directory to avoid repeated lookups
_cached_temp_dir: Optional[str] = None
_cache_lock = threading.Lock()


def get_writable_temp_dir() -> str:
    """
    Get a writable temp directory across environments (local, Vercel, etc.).
    Checks candidates in order and returns the first writable one.
    Result is cached for performance.
    """
    global _cached_temp_dir
    
    # Return cached value if available
    if _cached_temp_dir is not None:
        return _cached_temp_dir
    
    with _cache_lock:
        # Double-check pattern - another thread might have set it
        if _cached_temp_dir is not None:
            return _cached_temp_dir
        
        # Priority order for temp directories:
        # 1. Explicit TEMP_DIR env var (highest priority for deployment configs)
        # 2. ./temp relative to working directory (local development)
        # 3. /tmp/lexsy (Vercel and serverless platforms)
        # 4. System temp + lexsy subdirectory (fallback)
        candidates = [
            os.getenv("TEMP_DIR"),
            _path.abspath("temp"),
            "/tmp/lexsy",
            _path.join(tempfile.gettempdir(), "lexsy"),
        ]
        
        errors = []
        for candidate in candidates:
            if not candidate:
                continue
            
            try:
                # Normalize path
                normalized = _path.abspath(candidate)
                
                # Create directory if it doesn't exist
                os.makedirs(normalized, exist_ok=True)
                
                # Test write permissions with a unique test file
                test_filename = f".write_test_{secrets.token_hex(8)}"
                test_path = _path.join(normalized, test_filename)
                
                # Write test
                with open(test_path, "w") as f:
                    f.write("test")
                
                # Read test (verify file was actually written)
                with open(test_path, "r") as f:
                    content = f.read()
                    if content != "test":
                        raise IOError("Write test failed: content mismatch")
                
                # Cleanup test file
                os.remove(test_path)
                
                # Success! Cache and return
                _cached_temp_dir = normalized
                print(f"✅ Using temp directory: {normalized}")
                return normalized
                
            except Exception as e:
                error_msg = f"Failed to use {candidate}: {str(e)}"
                errors.append(error_msg)
                print(f"⚠️  {error_msg}")
                continue
        
        # If we reach here, no writable directory is available
        error_detail = f"No writable temp directory available. Tried: {', '.join(errors)}"
        print(f"❌ {error_detail}")
        raise HTTPException(status_code=500, detail=error_detail)


def generate_random_id(length: int = 20) -> str:
    """
    Generate a secure random ID using lowercase alphanumeric characters.
    Serverless-safe alternative to uuid.uuid4().
    """
    alphabet = string.ascii_lowercase + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def cleanup_old_files(max_age_hours: int = 24) -> int:
    """
    Clean up old temporary files from the temp directory.
    Returns the number of files deleted.
    
    Args:
        max_age_hours: Delete files older than this many hours (default: 24)
    """
    try:
        temp_dir = get_writable_temp_dir()
        import time
        now = time.time()
        max_age_seconds = max_age_hours * 3600
        deleted_count = 0
        
        for filename in os.listdir(temp_dir):
            # Skip hidden files and directories
            if filename.startswith('.'):
                continue
            
            filepath = _path.join(temp_dir, filename)
            
            # Only process files, not directories
            if not _path.isfile(filepath):
                continue
            
            # Check file age
            file_age = now - _path.getmtime(filepath)
            if file_age > max_age_seconds:
                try:
                    os.remove(filepath)
                    deleted_count += 1
                    print(f"🗑️  Deleted old temp file: {filename}")
                except Exception as e:
                    print(f"⚠️  Failed to delete {filename}: {e}")
        
        if deleted_count > 0:
            print(f"✅ Cleaned up {deleted_count} old temp files")
        
        return deleted_count
        
    except Exception as e:
        print(f"⚠️  Temp file cleanup failed: {e}")
        return 0

