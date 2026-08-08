def build_memory_context(posts, topics):

    memory = []

    for post in posts:

        memory.append({
            "type": "published_post",
            "text": post.get("text", ""),
            "createdAt": str(post.get("createdAt", ""))
        })

    for topic in topics:

        memory.append({
            "type": "evaluated_topic",
            "title": topic.get("title", ""),
            "decision": topic.get("decision", ""),
            "reason": topic.get("reason", "")
        })

    return memory