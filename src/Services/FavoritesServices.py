import os
import json
from typing import List
from datetime import datetime

from src.Models.job_model import Job

FAVORITES_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../Data/favorites.json"))

class FavoritesService:
    def __init__(self) -> None:
        self.favorite_jobs: List[Job] = []
        self.load_favorites()

    def add_favorite_job(self, job: Job) -> bool:
        if job not in self.favorite_jobs:
            self.favorite_jobs.append(job)
            self.save_favorites()
            print(f"Added to favorites: {job.title}")
            return True
        
        print(f"Already in favorites: {job.title}")
        return False

    def remove_favorite_job(self, job_to_remove: Job) -> bool:
        if job_to_remove in self.favorite_jobs:
            self.favorite_jobs.remove(job_to_remove)
            self.save_favorites()
            print(f"Removed from favorites: {job_to_remove.title}")
            return True
        
        print(f"Not found in favorites: {job_to_remove.title}")
        return False

    def get_all_favorites(self) -> List[Job]:
        return self.favorite_jobs

    def save_favorites(self) -> None:
        def _datetime_converter(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            raise TypeError(f"Type {type(obj)} not serializable")

        serializable_favorites = [vars(job) for job in self.favorite_jobs]

        try:
            with open(FAVORITES_FILE, 'w', encoding='utf-8') as file:
                json.dump(serializable_favorites, file, indent=4, default=_datetime_converter)
        except IOError as e:
            print(f"Error saving favorites: {e}")

    def load_favorites(self) -> None:
        if not os.path.exists(FAVORITES_FILE):
            self.favorite_jobs = []
            return

        try:
            with open(FAVORITES_FILE, 'r', encoding='utf-8') as file:
                data = json.load(file)

                jobs = []
                for job_data in data:
                    if 'data' in job_data and isinstance(job_data['data'], str):
                        job_data['data'] = datetime.fromisoformat(job_data['data'])
                    if 'fetch_date' in job_data and isinstance(job_data['fetch_date'], str):
                        job_data['fetch_date'] = datetime.fromisoformat(job_data['fetch_date'])

                    job = Job(**job_data)
                    jobs.append(job)

                self.favorite_jobs = jobs

        except (IOError, json.JSONDecodeError) as e:
            print(f"Error loading favorites: {e}")
            self.favorite_jobs = []