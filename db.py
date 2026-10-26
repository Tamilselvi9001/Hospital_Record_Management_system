import os
import json
import uuid
import datetime
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/medivault")
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
STORAGE_FILE = DATA_DIR / "medivault_db.json"

class JsonCollection:
    """A resilient MongoDB-compatible collection backed by JSON storage."""
    def __init__(self, db, name):
        self.db = db
        self.name = name

    def _get_items(self):
        return self.db.data.get(self.name, [])

    def _save(self):
        self.db.save()

    def find(self, query=None, sort=None):
        items = self._get_items()
        if not query:
            res = list(items)
        else:
            res = []
            for item in items:
                matches = True
                for k, v in query.items():
                    if k == "$or" and isinstance(v, list):
                        or_match = False
                        for sub_q in v:
                            sub_match = True
                            for sk, sv in sub_q.items():
                                if item.get(sk) != sv:
                                    sub_match = False
                                    break
                            if sub_match:
                                or_match = True
                                break
                        if not or_match:
                            matches = False
                            break
                    elif item.get(k) != v:
                        matches = False
                        break
                if matches:
                    res.append(item)
        if sort:
            for field, direction in reversed(sort):
                reverse = direction < 0
                res.sort(key=lambda x: str(x.get(field, "")), reverse=reverse)
        return res

    def find_one(self, query=None):
        results = self.find(query)
        return results[0] if results else None

    def insert_one(self, doc):
        doc = dict(doc)
        if "_id" not in doc:
            doc["_id"] = str(uuid.uuid4())
        if "created_at" not in doc:
            doc["created_at"] = datetime.datetime.utcnow().isoformat()
        if self.name not in self.db.data:
            self.db.data[self.name] = []
        self.db.data[self.name].append(doc)
        self._save()
        class InsertResult:
            def __init__(self, inserted_id):
                self.inserted_id = inserted_id
        return InsertResult(doc["_id"])

    def update_one(self, query, update, upsert=False):
        items = self.db.data.get(self.name, [])
        set_vals = update.get("$set", {})
        push_vals = update.get("$push", {})
        modified_count = 0
        
        for item in items:
            matches = True
            for k, v in query.items():
                if item.get(k) != v:
                    matches = False
                    break
            if matches:
                item.update(set_vals)
                for pk, pv in push_vals.items():
                    if pk not in item or not isinstance(item[pk], list):
                        item[pk] = []
                    item[pk].append(pv)
                modified_count += 1
                break
                
        if modified_count == 0 and upsert:
            new_doc = dict(query)
            new_doc.update(set_vals)
            if "_id" not in new_doc:
                new_doc["_id"] = str(uuid.uuid4())
            items.append(new_doc)
            modified_count = 1

        self.db.data[self.name] = items
        self._save()
        class UpdateResult:
            def __init__(self, count):
                self.modified_count = count
        return UpdateResult(modified_count)

    def delete_one(self, query):
        items = self.db.data.get(self.name, [])
        initial_len = len(items)
        for i, item in enumerate(items):
            matches = True
            for k, v in query.items():
                if item.get(k) != v:
                    matches = False
                    break
            if matches:
                del items[i]
                break
        self.db.data[self.name] = items
        self._save()
        deleted = initial_len - len(items)
        class DeleteResult:
            def __init__(self, count):
                self.deleted_count = count
        return DeleteResult(deleted)

    def count_documents(self, query=None):
        return len(self.find(query))


class FallbackDatabase:
    def __init__(self, filepath=STORAGE_FILE):
        self.filepath = filepath
        self.data = {}
        self.load()

    def load(self):
        if self.filepath.exists():
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
            except Exception:
                self.data = {}
        else:
            self.data = {}

    def save(self):
        try:
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving database file: {e}")

    def __getitem__(self, name):
        return JsonCollection(self, name)

    def __setitem__(self, name, value):
        pass


def get_db():
    use_fallback = False
    try:
        import pymongo
        client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=1000)
        client.admin.command('ping')
        db_name = MONGO_URI.split("/")[-1].split("?")[0] or "medivault"
        db = client[db_name]
        return db
    except Exception as e:
        use_fallback = True

    if use_fallback:
        return FallbackDatabase()

db = get_db()
