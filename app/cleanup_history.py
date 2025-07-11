#!/usr/bin/env python3
"""
Cleanup script for AgenticBot history duplicates
Run this script to remove duplicate session files and organize the history directory
"""

import sys
import os

# Add the app directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

from history_manager import HistoryManager

def main():
    print("🧹 AgenticBot History Cleanup Tool")
    print("=" * 40)
    
    # Initialize history manager
    history_manager = HistoryManager()
    
    # List current sessions before cleanup
    sessions_before = history_manager.list_sessions()
    print(f"📊 Sessions found: {len(sessions_before)}")
    
    # Get all files count before cleanup
    import glob
    pattern = os.path.join(history_manager.history_dir, "chat_*.json")
    files_before = len(glob.glob(pattern))
    print(f"📁 Total files: {files_before}")
    
    if files_before == 0:
        print("✅ No history files found. Nothing to clean up.")
        return
    
    # Show some examples of duplicates
    print("\n🔍 Analyzing for duplicates...")
    session_counts = {}
    for session in sessions_before:
        session_id = session['session_id']
        if session_id not in session_counts:
            session_counts[session_id] = 0
        session_counts[session_id] += 1
    
    duplicates = {sid: count for sid, count in session_counts.items() if count > 1}
    
    if duplicates:
        print(f"⚠️  Found {len(duplicates)} sessions with multiple files:")
        for session_id, count in list(duplicates.items())[:5]:  # Show first 5
            print(f"   - Session {session_id}: {count} files")
        if len(duplicates) > 5:
            print(f"   ... and {len(duplicates) - 5} more")
    else:
        print("✅ No duplicates detected!")
        return
    
    # Ask for confirmation
    print(f"\n🗑️  This will delete {files_before - len(sessions_before)} duplicate files")
    response = input("Continue? (y/N): ").strip().lower()
    
    if response != 'y':
        print("❌ Cleanup cancelled.")
        return
    
    # Perform cleanup
    print("\n🧹 Cleaning up duplicates...")
    deleted_count = history_manager.cleanup_duplicate_sessions()
    
    # Get counts after cleanup
    sessions_after = history_manager.list_sessions()
    files_after = len(glob.glob(pattern))
    
    # Report results
    print("\n📊 Cleanup Results:")
    print(f"   Files before: {files_before}")
    print(f"   Files after: {files_after}")
    print(f"   Files deleted: {deleted_count}")
    print(f"   Unique sessions: {len(sessions_after)}")
    
    if deleted_count > 0:
        print(f"\n✅ Successfully cleaned up {deleted_count} duplicate files!")
        print("📚 Your chat history is now organized with one file per session.")
    else:
        print("\n✅ No duplicates found or removed.")
    
    print("\n🎉 Cleanup complete! You can now use AgenticBot without duplicate issues.")

if __name__ == "__main__":
    main() 