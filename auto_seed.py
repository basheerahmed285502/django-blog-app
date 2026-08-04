import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog.settings')
django.setup()


def run_production_setup():
    from posts.models import Post, Tag, Comment
    from accounts.models import UserProfile
    from django.contrib.auth.models import User

    print("🤖 Checking Production Database Requirements...")

    # AUTO-CREATE ADMIN ACCOUNT IF MISSING
    if not User.objects.filter(is_superuser=True).exists():
        print("Creating production Admin Superuser...")

        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='AdminPass99!'
        )
        UserProfile.objects.get_or_create(
            user=admin_user,
            defaults={"phone_number": "+0000000000",
                      "city": "HQ", "address": "Admin System Office"}
        )
        print("Admin created. Username: admin | Password: AdminPass99!")
    else:
        print("Admin already exists. Skipping...")

    # AUTO-CREATE DUMMY USERS & PROFILES IF DATA IS BLANK
    if User.objects.count() <= 1:  # Only contains the admin we just created
        print("Database is blank. Starting 5 Muslim user seeding loop...")
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
            user, created = User.objects.get_or_create(
                username=data["username"],
                defaults={
                    "first_name": data["first"], "last_name": data["last"], "email": data["email"]}
            )
            if created:
                user.set_password("SecureUserPassword123!")
                user.save()
                UserProfile.objects.get_or_create(
                    user=user,
                    defaults={
                        "phone_number": f"+9198765{random.randint(10000, 99999)}",
                        "city": random.choice(["Mumbai", "Delhi", "Hyderabad", "Bengaluru"]),
                        "address": f"Flat No. {random.randint(101, 505)}, Crescent Heights"
                    }
                )
            users.append(user)

        # AUTO-CREATE TAGS
        print("🏷️ Seeding post tags...")
        tag_names = ["Python", "Django", "Bootstrap 5",
                     "Web Development", "Database Tuning"]
        tags = [Tag.objects.get_or_create(name=name)[0] for name in tag_names]

        # AUTO-CREATE POSTS
        print("📝 Writing dummy blog posts...")
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
                    "content": f"This is live production dummy content for '{title}'. It verifies that the grid loops, styling sheets, and pagination components render correctly for internet traffic.",
                    "user": random.choice(users),
                }
            )
            if created:
                post.tags.set(random.sample(tags, k=random.randint(1, 3)))
                post.save()
            posts.append(post)

        # AUTO-CREATE COMMENTS
        print("Adding dummy comments...")
        comment_samples = ["Wow, great layout!",
                           "Simple and incredibly clear.", "Fixed my columns instantly."]
        for post in posts:
            for _ in range(random.randint(1, 2)):
                Comment.objects.create(
                    post=post,
                    user=random.choice(users),
                    comment=random.choice(comment_samples)
                )
        print("Production tables seeded completely!")
    else:
        print("Blog data already present. Skipping data seed loop...")


if __name__ == "__main__":
    run_production_setup()
