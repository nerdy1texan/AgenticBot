"""
History Manager for AgenticBot
Handles saving, loading, and managing chat session history
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
import uuid
import glob

class HistoryManager:
    """Manages chat history persistence and retrieval"""
    
    def __init__(self, history_dir: str = "history"):
        self.history_dir = history_dir
        self.ensure_history_dir()
    
    def ensure_history_dir(self):
        """Create history directory if it doesn't exist"""
        if not os.path.exists(self.history_dir):
            os.makedirs(self.history_dir)
    
    def generate_session_id(self) -> str:
        """Generate a unique session ID"""
        return str(uuid.uuid4())[:8]
    
    def generate_filename(self, session_id: str) -> str:
        """Generate filename for a session"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"chat_{timestamp}_{session_id}.json"
    
    def find_existing_session_file(self, session_id: str) -> Optional[str]:
        """Find existing session file by session_id"""
        if not session_id:
            return None
        
        pattern = os.path.join(self.history_dir, f"chat_*_{session_id}.json")
        files = glob.glob(pattern)
        return files[0] if files else None
    
    def generate_title(self, chat_history: List[Dict]) -> str:
        """Generate a title from the first user message"""
        for message in chat_history:
            if message.get('role') == 'user':
                content = message.get('content', '')
                # Take first 50 characters and clean up
                title = content[:50].strip()
                if len(content) > 50:
                    title += "..."
                return title if title else "New Chat"
        return "New Chat"
    
    def save_session(self, session_data: Dict) -> str:
        """Save a chat session to file"""
        try:
            session_id = session_data.get('session_id')
            
            # For existing sessions, find and update the existing file
            if session_id:
                existing_file = self.find_existing_session_file(session_id)
                if existing_file:
                    filepath = existing_file
                else:
                    # Session ID exists but no file found, create new file
                    filename = self.generate_filename(session_id)
                    filepath = os.path.join(self.history_dir, filename)
            else:
                # New session, generate new ID and file
                session_id = self.generate_session_id()
                filename = self.generate_filename(session_id)
                filepath = os.path.join(self.history_dir, filename)
            
            # Update metadata
            session_data.update({
                'session_id': session_id,
                'updated_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'metadata': {
                    'total_messages': len(session_data.get('chat_history', [])),
                    'tools_used': self.extract_tools_used(session_data.get('agentic_logs', [])),
                    'session_duration': self.calculate_duration(session_data)
                }
            })
            
            # Generate title if not provided
            if not session_data.get('title'):
                session_data['title'] = self.generate_title(session_data.get('chat_history', []))
            
            # Ensure created_at exists
            if not session_data.get('created_at'):
                session_data['created_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, indent=2, ensure_ascii=False)
            
            return filepath
            
        except Exception as e:
            print(f"Error saving session: {e}")
            return None
    
    def load_session(self, filepath: str) -> Optional[Dict]:
        """Load a chat session from file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading session {filepath}: {e}")
            return None
    
    def list_sessions(self) -> List[Dict]:
        """List all chat sessions with metadata"""
        sessions = []
        pattern = os.path.join(self.history_dir, "chat_*.json")
        
        # Use a dict to deduplicate by session_id
        session_dict = {}
        
        for filepath in glob.glob(pattern):
            session_data = self.load_session(filepath)
            if session_data:
                session_id = session_data.get('session_id', 'unknown')
                session_info = {
                    'filepath': filepath,
                    'filename': os.path.basename(filepath),
                    'session_id': session_id,
                    'title': session_data.get('title', 'Untitled Chat'),
                    'created_at': session_data.get('created_at', ''),
                    'updated_at': session_data.get('updated_at', ''),
                    'total_messages': session_data.get('metadata', {}).get('total_messages', 0),
                    'tools_used': session_data.get('metadata', {}).get('tools_used', [])
                }
                
                # Keep only the most recent version of each session_id
                if session_id not in session_dict or session_info['updated_at'] > session_dict[session_id]['updated_at']:
                    session_dict[session_id] = session_info
        
        # Convert back to list and sort by updated_at (most recent first)
        sessions = list(session_dict.values())
        sessions.sort(key=lambda x: x['updated_at'], reverse=True)
        return sessions
    
    def delete_session(self, filepath: str) -> bool:
        """Delete a chat session file"""
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                return True
            return False
        except Exception as e:
            print(f"Error deleting session {filepath}: {e}")
            return False
    
    def delete_all_session_files(self, session_id: str) -> int:
        """Delete all files for a given session_id (to clean up duplicates)"""
        deleted_count = 0
        pattern = os.path.join(self.history_dir, f"chat_*_{session_id}.json")
        
        for filepath in glob.glob(pattern):
            try:
                os.remove(filepath)
                deleted_count += 1
            except Exception as e:
                print(f"Error deleting {filepath}: {e}")
        
        return deleted_count
    
    def search_sessions(self, query: str) -> List[Dict]:
        """Search sessions by title or content"""
        query = query.lower()
        sessions = self.list_sessions()
        filtered_sessions = []
        
        for session_meta in sessions:
            # Check title
            if query in session_meta['title'].lower():
                filtered_sessions.append(session_meta)
                continue
            
            # Check content
            session_data = self.load_session(session_meta['filepath'])
            if session_data:
                for message in session_data.get('chat_history', []):
                    if query in message.get('content', '').lower():
                        filtered_sessions.append(session_meta)
                        break
        
        return filtered_sessions
    
    def extract_tools_used(self, agentic_logs: List[Dict]) -> List[str]:
        """Extract unique tools used from agentic logs"""
        tools = set()
        for log in agentic_logs:
            message = log.get('message', '').lower()
            if 'search agent' in message:
                tools.add('web_search')
            elif 'web extraction agent' in message:
                tools.add('web_scraping')
            elif 'research agent' in message:
                tools.add('deep_research')
            elif 'image generation agent' in message:
                tools.add('image_generation')
        return list(tools)
    
    def calculate_duration(self, session_data: Dict) -> str:
        """Calculate session duration"""
        try:
            created = session_data.get('created_at')
            updated = session_data.get('updated_at')
            if created and updated:
                start = datetime.strptime(created, "%Y-%m-%d %H:%M:%S")
                end = datetime.strptime(updated, "%Y-%m-%d %H:%M:%S")
                duration = end - start
                hours, remainder = divmod(duration.total_seconds(), 3600)
                minutes, seconds = divmod(remainder, 60)
                return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
        except:
            pass
        return "00:00:00"
    
    def export_session(self, filepath: str, export_format: str = 'json') -> Optional[str]:
        """Export session in different formats"""
        session_data = self.load_session(filepath)
        if not session_data:
            return None
        
        base_name = os.path.splitext(os.path.basename(filepath))[0]
        
        if export_format == 'json':
            export_path = os.path.join(self.history_dir, f"{base_name}_export.json")
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, indent=2, ensure_ascii=False)
            return export_path
        
        elif export_format == 'txt':
            export_path = os.path.join(self.history_dir, f"{base_name}_export.txt")
            with open(export_path, 'w', encoding='utf-8') as f:
                f.write(f"AgenticBot Chat Session: {session_data.get('title', 'Untitled')}\n")
                f.write(f"Created: {session_data.get('created_at', 'Unknown')}\n")
                f.write(f"Updated: {session_data.get('updated_at', 'Unknown')}\n")
                f.write("=" * 50 + "\n\n")
                
                for message in session_data.get('chat_history', []):
                    role = "You" if message['role'] == 'user' else "AgenticBot"
                    timestamp = message.get('timestamp', '')
                    f.write(f"[{timestamp}] {role}: {message['content']}\n\n")
                    
                    if message.get('image_data'):
                        f.write("[Image was generated in this response]\n\n")
            
            return export_path
        
        return None
    
    def cleanup_old_sessions(self, max_sessions: int = 50) -> int:
        """Remove old sessions if count exceeds maximum"""
        sessions = self.list_sessions()
        if len(sessions) <= max_sessions:
            return 0
        
        # Keep most recent sessions, delete oldest
        sessions_to_delete = sessions[max_sessions:]
        deleted_count = 0
        
        for session in sessions_to_delete:
            if self.delete_session(session['filepath']):
                deleted_count += 1
        
        return deleted_count
    
    def cleanup_duplicate_sessions(self) -> int:
        """Clean up duplicate session files (keep only the most recent for each session_id)"""
        pattern = os.path.join(self.history_dir, "chat_*.json")
        session_files = {}
        deleted_count = 0
        
        # Group files by session_id
        for filepath in glob.glob(pattern):
            session_data = self.load_session(filepath)
            if session_data:
                session_id = session_data.get('session_id', 'unknown')
                updated_at = session_data.get('updated_at', '')
                
                if session_id not in session_files:
                    session_files[session_id] = []
                
                session_files[session_id].append({
                    'filepath': filepath,
                    'updated_at': updated_at,
                    'session_data': session_data
                })
        
        # For each session_id, keep only the most recent file
        for session_id, files in session_files.items():
            if len(files) > 1:
                # Sort by updated_at, keep the most recent
                files.sort(key=lambda x: x['updated_at'], reverse=True)
                files_to_delete = files[1:]  # All except the most recent
                
                for file_info in files_to_delete:
                    try:
                        os.remove(file_info['filepath'])
                        deleted_count += 1
                        print(f"Removed duplicate: {file_info['filepath']}")
                    except Exception as e:
                        print(f"Error deleting duplicate {file_info['filepath']}: {e}")
        
        return deleted_count 