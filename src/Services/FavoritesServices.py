import json
import os
from src.Models.job_model import Job 
import Data

FAVORITES_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../Data/favorites.json"))

class FavoritesService:
    def __init__(self):
        self.favorite_jobs = []
        self.load_favorites()

    def add_favorite_job(self, job):
        if job not in self.favorite_jobs:
            self.favorite_jobs.append(job)
            self.save_favorites()
            print(f"Added to favorites: {job.title}")
            return True
        print(f"Already in favorites: {job.title}")
        return False

    def remove_favorite_job(self, job_to_remove):
        if job_to_remove in self.favorite_jobs:
            self.favorite_jobs.remove(job_to_remove)
            self.save_favorites()
            print(f"Removed from favorites: {job_to_remove.title}")
            return True
        print(f"Not found in favorites: {job_to_remove.title}")
        return False

    def get_all_favorites(self):
        return self.favorite_jobs

    def save_favorites(self):
        serializable_favorites = [vars(job) for job in self.favorite_jobs]
        try:
            with open(FAVORITES_FILE, 'w') as f:
                json.dump(serializable_favorites, f, indent=4)
        except IOError as e:
            print(f"Error saving favorites: {e}")

    def load_favorites(self):
        if not os.path.exists(FAVORITES_FILE):
            self.favorite_jobs = []
            return

        try:
            with open(FAVORITES_FILE, 'r') as f:
                data = json.load(f)
                self.favorite_jobs = [Job(**job_data) for job_data in data]
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error loading favorites: {e}")
            self.favorite_jobs = []