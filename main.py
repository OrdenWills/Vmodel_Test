import json
from scipy.spatial.distance import cosine

def get_recommendations(user_id, n, show_name=False):
    """Uses cousine similarity to create recommendations based on category and video tags"""
    # Load data from JSON file
    with open("data.json") as f:
        data = json.load(f)

    # Parse user and video data and get user unique watch history and also unique video tags on each video
    users = {user['user_id']: {'name': user['name'], 'watch_history': set(user['watch_history'])} for user in data['users']}
    videos = {video['video_id']: {'title': video['title'], 'category': video['category'], 'tags': set(video['tags'])} for video in data['videos']}

    # prepare categories and tags for similarity calculation
    all_categories = set(video['category'] for video in data['videos'])
    all_tags = set(tag for video in data['videos'] for tag in video['tags'])

    # One-hot encode 
    def create_video_vector(video_id):
        """Creates a vector [0,1] for cousine similarity"""
        vector = [0] * (len(all_categories) + len(all_tags)) # init the empty vector (0s)
        # loop through and populate (1s)
        for i, category in enumerate(all_categories):
            if videos[video_id]['category'] == category:
                vector[i] = 1
        for j, tag in enumerate(all_tags):
            if tag in videos[video_id]['tags']:
                vector[j + len(all_categories)] = 1
        return vector

    def convert_ids_2_string(ids:list):
        """Prints the recommended videos"""
        print([videos[id]['title'] for id in ids])
        
    # Pre-compute similarity matrix
    similarity_matrix = {}
    for video_id1 in videos:
        similarity_matrix[video_id1] = {}
        for video_id2 in videos:
            vector1 = create_video_vector(video_id1)
            vector2 = create_video_vector(video_id2)
            similarity_matrix[video_id1][video_id2] = 1 - cosine(vector1, vector2)

    # Find similar users (user-based)
    similar_users = []
    for other_user_id in users:
        if other_user_id != user_id:
            shared_videos = len(users[user_id]['watch_history'].intersection(users[other_user_id]['watch_history']))
            if shared_videos > 0:
                similarity = shared_videos / len(users[user_id]['watch_history'])
                similar_users.append((other_user_id, similarity))
    similar_users.sort(key=lambda x: x[1], reverse=True)

    # Combine user-based and content-based recommendations
    recommended_videos = {}
    for other_user_id, similarity in similar_users[:5]:  # Top 5 similar users
        for video_id in users[other_user_id]['watch_history']:
            if video_id not in users[user_id]['watch_history']:
                recommended_videos[video_id] = recommended_videos.get(video_id, 0) + similarity

    for video_id in users[user_id]['watch_history']:
        for other_video_id in videos:
            if other_video_id not in users[user_id]['watch_history']:
                similarity = similarity_matrix[video_id][other_video_id]
                recommended_videos[other_video_id] = recommended_videos.get(other_video_id, 0) + similarity

    # Get top N recommendations
    sorted_recommendations = sorted(recommended_videos.items(), key=lambda x: x[1], reverse=True)
    # print(sorted_recommendations)
    user_recommendations = [video_id for video_id, similarity in sorted_recommendations[:n]]

    # if set to true prints the recommended videos
    if show_name:
        convert_ids_2_string(user_recommendations)
    return user_recommendations
# Example usage
recommendations = get_recommendations(user_id=1, n=5)
print(recommendations)