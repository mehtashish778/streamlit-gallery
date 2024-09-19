import pandas as pd
from datetime import datetime, timedelta
import pytz  # Import pytz for timezone handling
import os
import csv
# from API.ig_comment import create_csv_if_not_exists  # Import the function

class Instagram_Comment_Analytics:
    def __init__(self):
        self.instagram_posts_df = None
        self.instagram_comments_df = None
        self.instagram_replies_comments_df = None
        self.comment_analysis_df = None
        self.load_data()
        

    def load_data(self):
        """Load the necessary CSV files."""
        # create_csv_if_not_exists()  # Ensure CSV files are created

        # Update paths to load CSV files from the data folder
        self.instagram_posts_df = pd.read_csv(os.path.join('data', 'instagram_posts.csv'))
        self.instagram_comments_df = pd.read_csv(os.path.join('data', 'instagram_comments.csv'))
        self.instagram_replies_comments_df = pd.read_csv(os.path.join('data', 'instagram_replies_comments.csv'))
        self.comment_analysis_df = pd.read_csv(os.path.join('data', 'comment_analysis.csv'))
        
        # Convert timestamps to datetime with UTC timezone
        self.instagram_posts_df['Post Timestamp'] = pd.to_datetime(self.instagram_posts_df['Post Timestamp']).dt.tz_convert('UTC')
        self.instagram_comments_df['Comment Timestamp'] = pd.to_datetime(self.instagram_comments_df['Comment Timestamp']).dt.tz_convert('UTC')
        # self.instagram_replies_comments_df['Reply Timestamp'] = pd.to_datetime(self.instagram_replies_comments_df['Reply Timestamp']).dt.tz_convert('UTC')
        self.instagram_replies_comments_df['Reply Comment Timestamp'] = pd.to_datetime(self.instagram_replies_comments_df['Reply Comment Timestamp']).dt.tz_convert('UTC')

    def get_time_frames(self):
        """Define time frames for counting."""
        now = datetime.now(pytz.UTC)  # Make current time timezone-aware
        return {
            'last_24_hours': now - timedelta(hours=24),
            'last_72_hours': now - timedelta(hours=72),
            'last_week': now - timedelta(weeks=1),
            'last_month': now - timedelta(days=30)
        }

    def count_total_posts(self, time_frame):
        """Count total posts in a given time frame."""
        return self.instagram_posts_df[self.instagram_posts_df['Post Timestamp'] >= time_frame].shape[0]

    def count_total_comments(self, time_frame):
        """Count total comments in a given time frame."""
        return self.instagram_comments_df[self.instagram_comments_df['Comment Timestamp'] >= time_frame].shape[0]

    def count_total_replies(self, time_frame):
        """Count total replies in a given time frame."""
        return self.instagram_replies_comments_df[self.instagram_replies_comments_df['Reply Comment Timestamp'] >= time_frame].shape[0]

    def get_timewise_totals(self):
        """Get total posts, comments, and replies in specified time frames."""
        time_frames = self.get_time_frames()

        timewise_totals = {
            time_frame: {
                'total_posts': self.count_total_posts(time_limit),
                'total_comments': self.count_total_comments(time_limit),
                'total_replies': self.count_total_replies(time_limit)
            }
            for time_frame, time_limit in time_frames.items()
        }

        return timewise_totals

    def get_sentiment(self):
        """Get sentiment from the comment analysis DataFrame."""
        return self.comment_analysis_df['sentiment'].tolist()

    def get_engagement_intensity(self):
        """Get engagement intensity from the comment analysis DataFrame."""
        return self.comment_analysis_df['engagement_intensity'].tolist()

    def get_engagement_intent(self):
        """Get engagement intent from the comment analysis DataFrame."""
        intents = self.comment_analysis_df['engagement_intent'].apply(lambda x: eval(x) if isinstance(x, str) else x).tolist()
        return [intent if isinstance(intent, list) else [intent] for intent in intents]  # Ensure all intents are lists

# if __name__ == "__main__":
#     analytics = InstagramAnalytics()

#     # Run the test for timewise totals
#     totals = analytics.get_timewise_totals()
#     print("Timewise Totals:")
#     for time_frame, counts in totals.items():
#         print(f"{time_frame}: {counts}")

#     # Test the new functions
#     sentiments = analytics.get_sentiment()
#     intensities = analytics.get_engagement_intensity()
#     intents = analytics.get_engagement_intent()

#     print("\nSentiments:", sentiments)
#     print("Engagement Intensities:", intensities)
#     print("Engagement Intents:", intents)