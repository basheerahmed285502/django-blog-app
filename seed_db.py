import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog.settings')
django.setup()


def seed_database():
    from posts.models import Post, Tag, Comment
    from accounts.models import UserProfile
    from django.contrib.auth.models import User

    print("Starting database seeding process...")

    print("Creating user accounts and profiles...")
    users = []
    user_data = [
        {"username": "imran_khan", "first": "Imran",
            "last": "Khan", "email": "imran@example.com"},
        {"username": "zayan_ahmed", "first": "Zayan",
            "last": "Ahmed", "email": "zayan@example.com"},
        {"username": "fathima_biwi", "first": "Fathima",
            "last": "Biwi", "email": "fathima@example.com"},
        {"username": "rayan_siddiqui", "first": "Rayan",
            "last": "Siddiqui", "email": "rayan@example.com"},
        {"username": "ayesha_malik", "first": "Ayesha",
            "last": "Malik", "email": "ayesha@example.com"},
    ]

    for data in user_data:
        # get_or_create checks for username first to prevent IntegrityErrors
        user, created = User.objects.get_or_create(
            username=data["username"],
            defaults={
                "first_name": data["first"],
                "last_name": data["last"],
                "email": data["email"]
            }
        )
        if created:
            user.set_password("SecurePassword123!")
            user.save()

            # Matched exactly to our custom UserProfile model fields
            UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    "phone_number": f"+9198765{random.randint(10000, 99999)}",
                    "city": random.choice(["Mumbai", "Delhi", "Hyderabad", "Bengaluru"]),
                    "address": f"Flat No. {random.randint(101, 505)}, Crescent Heights, Sector 4"
                }
            )
        users.append(user)

    print("🏷️ Creating post tags...")
    tag_names = ["Python", "Django", "Bootstrap 5",
                 "Web Development", "Database Tuning", "Coding Tips"]
    tags = []
    for name in tag_names:
        tag, created = Tag.objects.get_or_create(name=name)
        tags.append(tag)

    print("📝 Writing blog posts...")
    post_titles = [
        "Getting Started with Django Forms and Grid Rows",
        "Mastering Bootstrap 5 Column System Layouts",
        "Why Python is Perfect for Modern Web Engineering",
        "How to Handle Database Migration Architecture Safely",
        "Building Clean Authentication Views for Your Blog Site",
    ]

    posts = []
    for title in post_titles:
        post, created = Post.objects.get_or_create(
            title=title,
            defaults={
                "content": f"This is the extensive technical content for '{title}'. It covers styling parameters, form structures, and backend query configurations.",
                "user": random.choice(users),
                # post_image is skipped here; it defaults to blank/null safely
            }
        )
        if created:
            random_tags = random.sample(tags, k=random.randint(1, 3))
            post.tags.set(random_tags)
            post.save()
        posts.append(post)

    print("💬 Adding comment streams...")
    comment_samples = [
        "Wow, this article saved me hours of debugging layout issues!",
        "Can you write a follow-up guide explaining the `clean` validation data block?",
        "Simple, direct, and incredibly clear example code.",
        "I ran into an issue with my column grid system, but this fixed it instantly.",
        "Brilliant structural explanation, thanks for sharing."
    ]

    for post in posts:
        # Generates 2 to 3 random comments per blog post
        for _ in range(random.randint(2, 3)):
            Comment.objects.create(
                post=post,
                user=random.choice(users),
                # Matched to your model's field: comment (TextField)
                comment=random.choice(comment_samples)
            )

    print("Database successfully populated with all model parameters!")


if __name__ == "__main__":
    seed_database()
