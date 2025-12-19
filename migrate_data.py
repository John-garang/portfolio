import requests
import json

# Backend API URL
API_BASE = 'https://portfolio-backend-1-53hz.onrender.com/api'

# Admin credentials
ADMIN_USERNAME = 'dengjohn200@gmail.com'
ADMIN_PASSWORD = 'John@Alustudent1'

def get_admin_token():
    """Get admin authentication token"""
    response = requests.post(f'{API_BASE}/login', json={
        'username': ADMIN_USERNAME,
        'password': ADMIN_PASSWORD
    })
    if response.status_code == 200:
        return response.json()['token']
    else:
        print(f"Login failed: {response.status_code}")
        return None

def migrate_articles(token):
    """Migrate articles to database"""
    articles = [
        {
            "title": "If Equality Means This, Burn the World Already",
            "category": "personal-writings",
            "excerpt": "When violence wears a skirt and puts on lipstick, it suddenly becomes excused. A critical look at the double standards in how society treats violence based on gender.",
            "content": """<p class="lead">When violence wears a skirt and puts on lipstick, it suddenly becomes excused.</p>

<p>Today in Aweil, Northern Bahr El Ghazal, South Sudan, a man—a man I do not know, became a victim of the growing social inequality. His wife cut off his private part while he was asleep, for unknown reasons. The man is currently at the hospital with medics trying to salvage whatever is left of his manhood, while the culprit sits comfortably with the authorities.</p>

<p>But you know what disgusts me? Go look at the comment section of major media houses in South Sudan. People are laughing about it. They are turning the man's agony into some cheap comedy, singing the same tired chorus: "He must have cheated."</p>

<p>No one has even heard the facts of the story. No empathy, just resorting to victim-blaming.</p>

<p>And this is not new in South Sudan. There are dozens of cases where women have stabbed their partners, poured boiling oil on them, or even mutilated them. The same excuses follow: he must have cheated, or what a weak man to let a woman do that.</p>

<p>But even more disgusting, the cheerleaders of this madness are our so-called feminists, the same people who carry equality cards around like house keys. They are jumping up with the comparison: "Why are people making this a big deal? It happens to women every day!" Like seriously? I've never heard of a woman undergoing that and people keeping quiet. Normally, if a man inflicts a severe injury on a woman, it is the same men who stand up, and sometimes, if the law is not there, the culprit is killed on the spot. But I've never seen a woman being killed on the spot for an assault on a man (except maybe if the assaulted man did it himself).</p>

<p>A few months ago, a man flogged his wife in Juba for infidelity, and the whole nation nearly tore itself apart with rage, shouting: "Gender-based violence," "Why didn't he just divorce her," and so on. But now, a man loses his genitals, and I don't hear anyone saying, "Why didn't she just leave him?" Why is everyone hell-bent on saying, "He has now learned his lesson and won't cheat"? Do we even know if he cheated? Is flogging worse than mutilation? Or does the gender of the victim dictate the level of outrage?</p>

<p>But no one talks about this hypocrisy on display. Men's pain doesn't trend. Their oppression doesn't spark campaigns. They don't get hashtags. No one marches for them. No NGO or government even cares about them. Instead, they get laughed at, mocked, and told he deserved it or he was weak.</p>

<p>Take this: violence is violence, no matter who is at the receiving end. Cutting someone's genitals is a severe crime and should even be punished on the same level as murder. Stabbing your partner or pouring hot oil on them isn't a joke, it's a barbaric crime and deserves a heavy penalty.</p>

<p>And to the South Sudanese feminists celebrating this, stop pretending. You're not fighting for equality. You want a world where you bend the laws to please you. You are fighting hard to become the oppressor while maintaining your victim title. And to the society (men and women) who blindly embrace these acts just because you want to look civilized; you're sick. If the roles were reversed, you'd demand life imprisonment. But when the victim is male, you clap. If that man was your father or brother, would you still laugh? Or the dancing of a mad man at the market square is only funny when he is not your family member.</p>

<p>Stop dehumanizing men because they don't wail at every scratch. Their pain counts, and their lives matter, even though they'll always prioritize your lives over theirs.</p>

<p>I'm tired of the hypocrisy. Tired of this cult of fake equality. Men, open your eyes.</p>""",
            "image": "Pictures/If Equality Means This, Burn the World Already.jpg"
        }
    ]
    
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    
    for article in articles:
        response = requests.post(f'{API_BASE}/articles', json=article, headers=headers)
        if response.status_code == 200:
            print(f"Migrated article: {article['title']}")
        else:
            print(f"Failed to migrate: {article['title']} - {response.status_code}")

def migrate_sample_data(token):
    """Add sample subscribers and messages"""
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    
    # Sample subscribers
    subscribers = [
        {"email": "john.doe@example.com", "firstName": "John", "lastName": "Doe"},
        {"email": "jane.smith@example.com", "firstName": "Jane", "lastName": "Smith"}
    ]
    
    for subscriber in subscribers:
        response = requests.post(f'{API_BASE}/subscribers', json=subscriber, headers=headers)
        if response.status_code == 200:
            print(f"Added subscriber: {subscriber['email']}")
        else:
            print(f"Failed to add subscriber: {subscriber['email']}")

def main():
    print("Starting data migration...")
    
    # Get authentication token
    token = get_admin_token()
    if not token:
        print("Failed to authenticate. Check credentials.")
        return
    
    print("Authentication successful")
    
    # Migrate data
    migrate_articles(token)
    migrate_sample_data(token)
    
    print("\nMigration complete!")

if __name__ == "__main__":
    main()