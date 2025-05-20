import pymongo


def connect_to_mongodb(host="mongodb://localhost:27017/", db_name="sample_mflix"):
    try:
        client = pymongo.MongoClient(host)
        db = client[db_name]
        print(f"Successfully connected to MongoDB at {host} and database '{db_name}'.")
        return client, db
    except Exception as e:
        print(f"An unexpected error occurred during connection: {e}")
        return None, None


def get_movies_from_year(year):
    client = None
    try:
        client, db = connect_to_mongodb()

        if client is None or db is None:
            print("Failed to establish MongoDB connection. Cannot query for movies.")
            return []

        movies_collection = db["movies"]

        print(f"Querying for movies from the year {year}...")

        query = {"year": year}
        projection = {"_id": 0, "title": 1, "year": 1}
        movies = list(movies_collection.find(query, projection))

        if movies:
            print(f"\nFound {len(movies)} movie(s) from the year {year}:")
            for movie in movies:
                print(
                    f"- Title: {movie.get('title', 'N/A')}, Year: {movie.get('year', 'N/A')}"
                )
        else:
            print(f"No movies found from the year {year}.")

        return movies

    except Exception as e:
        print(f"An unexpected error occurred during movie retrieval: {e}")
        return []
    finally:
        if client:
            client.close()
            print("MongoDB connection closed.")


if __name__ == "__main__":
    movies_2000 = get_movies_from_year(2000)
