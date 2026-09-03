import pandas as pd

events = [
    # Artificial Intelligence
    ("AI Workshop", "Artificial Intelligence",
     "Hands-on workshop introducing artificial intelligence concepts, applications, and intelligent systems."),
    ("Generative AI Seminar", "Artificial Intelligence",
     "Seminar covering generative artificial intelligence, large language models, and AI applications."),
    ("AI Project Expo", "Artificial Intelligence",
     "Students demonstrate artificial intelligence projects involving prediction, automation, and intelligent decision making."),
    ("Computer Vision Workshop", "Artificial Intelligence",
     "Practical session on computer vision, image classification, object detection, and visual recognition."),
    ("Natural Language Processing Talk", "Artificial Intelligence",
     "Talk about natural language processing, text analysis, language models, and conversational AI."),
    
    # Machine Learning
    ("Machine Learning Bootcamp", "Machine Learning",
     "Training session covering supervised learning, classification, regression, and machine learning workflows."),
    ("Deep Learning Workshop", "Machine Learning",
     "Workshop introducing neural networks, deep learning architectures, and model training."),
    ("ML Model Building Challenge", "Machine Learning",
     "Competition where students build machine learning models to solve prediction problems."),
    ("Predictive Analytics Seminar", "Machine Learning",
     "Seminar on predictive analytics, feature engineering, model evaluation, and forecasting."),
    ("Machine Learning Project Review", "Machine Learning",
     "Students present machine learning projects and discuss algorithms, datasets, and performance."),
    
    # Cybersecurity
    ("Cybersecurity Awareness Seminar", "Cybersecurity",
     "Seminar covering cybersecurity awareness, online safety, passwords, phishing, and digital threats."),
    ("Ethical Hacking Workshop", "Cybersecurity",
     "Practical workshop introducing ethical hacking, vulnerability assessment, and penetration testing concepts."),
    ("Network Security Talk", "Cybersecurity",
     "Expert discussion about network protection, firewalls, intrusion detection, and secure communication."),
    ("Cyber Defense Challenge", "Cybersecurity",
     "Student competition involving cybersecurity problems, digital security challenges, and threat analysis."),
    ("Information Security Conference", "Cybersecurity",
     "Conference discussing information security, cyber threats, privacy, risk management, and secure systems."),
    
    # Data Science
    ("Data Science Workshop", "Data Science",
     "Workshop covering data cleaning, exploratory analysis, visualization, and data science workflows."),
    ("Data Analytics Bootcamp", "Data Science",
     "Hands-on training in data analytics, statistical analysis, dashboards, and business insights."),
    ("Big Data Seminar", "Data Science",
     "Seminar introducing big data technologies, distributed processing, and large-scale data analytics."),
    ("Data Visualization Contest", "Data Science",
     "Competition where students create meaningful visualizations from real-world datasets."),
    ("Statistics for Data Science", "Data Science",
     "Session explaining statistical methods, probability, distributions, and their use in data science."),
    
    # Robotics
    ("Robotics Workshop", "Robotics",
     "Hands-on workshop covering robot design, sensors, motors, controllers, and robotic automation."),
    ("Robot Competition", "Robotics",
     "Competition where teams design and program robots to complete challenging tasks."),
    ("Autonomous Robotics Seminar", "Robotics",
     "Seminar discussing autonomous robots, navigation, sensing, and intelligent control."),
    ("Industrial Robotics Talk", "Robotics",
     "Expert talk about industrial robots, manufacturing automation, robotic arms, and smart factories."),
    ("Arduino Robotics Challenge", "Robotics",
     "Student challenge involving Arduino-based robots, sensors, motors, and embedded programming."),
    
    # Business
    ("Entrepreneurship Talk", "Business",
     "Successful entrepreneur discusses startup creation, business strategy, innovation, and leadership."),
    ("Startup Funding Seminar", "Business",
     "Session explaining startup funding, investors, venture capital, business plans, and financial strategy."),
    ("Business Leadership Workshop", "Business",
     "Workshop developing leadership, communication, decision-making, and management skills."),
    ("Marketing Strategy Seminar", "Business",
     "Seminar covering digital marketing, customer engagement, branding, and business growth."),
    ("Innovation and Startup Expo", "Business",
     "Students showcase innovative startup ideas, business models, products, and entrepreneurial projects."),
    
    # Culture
    ("Annual Cultural Fest", "Culture",
     "Campus cultural celebration featuring music, dance, drama, art, and student performances."),
    ("Classical Dance Evening", "Culture",
     "Cultural evening featuring classical dance performances by talented student artists."),
    ("Music Festival", "Culture",
     "Campus music festival featuring student bands, singers, instrumental performances, and live music."),
    ("Drama Competition", "Culture",
     "Inter-department drama competition featuring creative theatrical performances and storytelling."),
    ("Traditional Arts Exhibition", "Culture",
     "Exhibition showcasing traditional art, crafts, cultural heritage, and creative student work."),
    
    # Sports
    ("Football Tournament", "Sports",
     "Inter-department football tournament featuring student teams competing for the campus championship."),
    ("Cricket Championship", "Sports",
     "Campus cricket championship with teams from different departments competing in tournament matches."),
    ("Basketball Tournament", "Sports",
     "Basketball competition encouraging teamwork, athletic performance, and sportsmanship."),
    ("Badminton Championship", "Sports",
     "Campus badminton championship for students interested in competitive individual and doubles matches."),
    ("Athletics Meet", "Sports",
     "Annual athletics event featuring running, jumping, throwing, and other track and field competitions."),
]

# Repeat variations to create 240 records
records = []

for i in range(240):
    base_title, category, description = events[i % len(events)]

    number = i + 1

    title = f"{base_title} {number}"

    # Add variation so records are not identical
    description = (
        f"{description} "
        f"The event is organized for campus students and provides opportunities "
        f"for learning, participation, collaboration, and practical experience. "
        f"Event edition {number}."
    )

    records.append({
        "event_id": number,
        "title": title,
        "category": category,
        "description": description
    })

# Add special-case events
special_events = [
    {
        "event_id": 241,
        "title": "Technology Leadership Summit",
        "category": "Leadership",
        "description": (
            "Technology leadership summit featuring Dr. Ravi Kumar, "
            "a cybersecurity researcher and information security expert. "
            "The event focuses on leadership, innovation, and technology careers."
        )
    },
    {
        "event_id": 242,
        "title": "Innovation Leadership Forum",
        "category": "Leadership",
        "description": (
            "Leadership forum featuring Dr. Anitha Rao, an artificial intelligence "
            "researcher. The session discusses innovation, leadership, and future careers."
        )
    },
    {
        "event_id": 243,
        "title": "Healthcare Innovation Conference",
        "category": "Healthcare",
        "description": (
            "Conference featuring Dr. Meena Sharma, a data science researcher. "
            "The event discusses healthcare innovation and professional opportunities."
        )
    },
    {
        "event_id": 244,
        "title": "Future Technology Forum",
        "category": "Technology",
        "description": (
            "Technology forum featuring Prof. Arun Kumar, a robotics researcher. "
            "The event discusses technology trends, innovation, and engineering careers."
        )
    },
    {
        "event_id": 245,
        "title": "Digital Trust Conference",
        "category": "Technology",
        "description": (
            "Conference featuring Dr. Ravi Kumar, a cybersecurity researcher. "
            "The program discusses digital transformation, technology leadership, "
            "and professional development."
        )
    }
]

records.extend(special_events)

df = pd.DataFrame(records)

df.to_csv("events.csv", index=False)

print("=" * 60)
print("EVENT DATASET CREATED")
print("=" * 60)
print("Total records:", len(df))
print("Columns:", list(df.columns))
print()
print(df.head())
print()
print("Category counts:")
print(df["category"].value_counts())
print()
print("Dataset saved as: events.csv")