from typing import Any


LEARNING_RESOURCES = {
    "Python": {
        "difficulty": "Beginner",
        "duration": "3-4 weeks",
        "resources": [
            {
                "title": "Python Official Tutorial",
                "provider": "Python",
                "type": "Documentation",
                "url": "https://docs.python.org/3/tutorial/"
            },
            {
                "title": "Python for Beginners",
                "provider": "freeCodeCamp",
                "type": "Video Course",
                "url": "https://www.youtube.com/watch?v=rfscVS0vtbw"
            }
        ],
        "mini_project": "Build a command-line expense tracker using Python.",
        "certification": "Python Institute PCEP"
    },

    "SQL": {
        "difficulty": "Beginner",
        "duration": "2-3 weeks",
        "resources": [
            {
                "title": "SQL Tutorial",
                "provider": "W3Schools",
                "type": "Tutorial",
                "url": "https://www.w3schools.com/sql/"
            },
            {
                "title": "SQLBolt",
                "provider": "SQLBolt",
                "type": "Interactive Practice",
                "url": "https://sqlbolt.com/"
            }
        ],
        "mini_project": "Create a student database and write analytical SQL queries.",
        "certification": "Oracle Database SQL Certified Associate"
    },

    "HTML": {
        "difficulty": "Beginner",
        "duration": "1 week",
        "resources": [
            {
                "title": "HTML Tutorial",
                "provider": "MDN",
                "type": "Documentation",
                "url": "https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Structuring_content"
            }
        ],
        "mini_project": "Build a responsive personal portfolio webpage.",
        "certification": None
    },

    "CSS": {
        "difficulty": "Beginner",
        "duration": "2 weeks",
        "resources": [
            {
                "title": "CSS Tutorial",
                "provider": "MDN",
                "type": "Documentation",
                "url": "https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics"
            },
            {
                "title": "Flexbox Froggy",
                "provider": "Codepip",
                "type": "Interactive Practice",
                "url": "https://flexboxfroggy.com/"
            }
        ],
        "mini_project": "Design a responsive landing page using Flexbox and Grid.",
        "certification": None
    },

    "JavaScript": {
        "difficulty": "Beginner",
        "duration": "4-6 weeks",
        "resources": [
            {
                "title": "JavaScript Guide",
                "provider": "MDN",
                "type": "Documentation",
                "url": "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide"
            },
            {
                "title": "JavaScript Algorithms and Data Structures",
                "provider": "freeCodeCamp",
                "type": "Course",
                "url": "https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures-v8/"
            }
        ],
        "mini_project": "Build a task manager with local storage.",
        "certification": "freeCodeCamp JavaScript Certification"
    },

    "React": {
        "difficulty": "Intermediate",
        "duration": "3-5 weeks",
        "resources": [
            {
                "title": "React Learn",
                "provider": "React",
                "type": "Documentation",
                "url": "https://react.dev/learn"
            },
            {
                "title": "React Course",
                "provider": "freeCodeCamp",
                "type": "Video Course",
                "url": "https://www.youtube.com/watch?v=bMknfKXIFA8"
            }
        ],
        "mini_project": "Build a job application tracker using React.",
        "certification": None
    },

    "Node.js": {
        "difficulty": "Intermediate",
        "duration": "3-4 weeks",
        "resources": [
            {
                "title": "Introduction to Node.js",
                "provider": "Node.js",
                "type": "Documentation",
                "url": "https://nodejs.org/en/learn/getting-started/introduction-to-nodejs"
            }
        ],
        "mini_project": "Build a REST API for a student management system.",
        "certification": "OpenJS Node.js Application Developer"
    },

    "Express.js": {
        "difficulty": "Intermediate",
        "duration": "2 weeks",
        "resources": [
            {
                "title": "Express Getting Started",
                "provider": "Express",
                "type": "Documentation",
                "url": "https://expressjs.com/en/starter/installing.html"
            }
        ],
        "mini_project": "Create an authentication API using Express and JWT.",
        "certification": None
    },

    "FastAPI": {
        "difficulty": "Intermediate",
        "duration": "2-3 weeks",
        "resources": [
            {
                "title": "FastAPI Tutorial",
                "provider": "FastAPI",
                "type": "Documentation",
                "url": "https://fastapi.tiangolo.com/tutorial/"
            }
        ],
        "mini_project": "Build a resume analysis API using FastAPI.",
        "certification": None
    },

    "REST API": {
        "difficulty": "Intermediate",
        "duration": "2 weeks",
        "resources": [
            {
                "title": "REST API Concepts",
                "provider": "MDN",
                "type": "Documentation",
                "url": "https://developer.mozilla.org/en-US/docs/Glossary/REST"
            }
        ],
        "mini_project": "Design and document a CRUD REST API.",
        "certification": None
    },

    "Git": {
        "difficulty": "Beginner",
        "duration": "1-2 weeks",
        "resources": [
            {
                "title": "Git Handbook",
                "provider": "GitHub",
                "type": "Documentation",
                "url": "https://guides.github.com/introduction/git-handbook/"
            },
            {
                "title": "Learn Git Branching",
                "provider": "Learn Git Branching",
                "type": "Interactive Practice",
                "url": "https://learngitbranching.js.org/"
            }
        ],
        "mini_project": "Maintain a Git repository using branches and pull requests.",
        "certification": "GitHub Foundations"
    },

    "Docker": {
        "difficulty": "Intermediate",
        "duration": "2-3 weeks",
        "resources": [
            {
                "title": "Docker Get Started",
                "provider": "Docker",
                "type": "Documentation",
                "url": "https://docs.docker.com/get-started/"
            },
            {
                "title": "Docker Tutorial for Beginners",
                "provider": "freeCodeCamp",
                "type": "Video Course",
                "url": "https://www.youtube.com/watch?v=fqMOX6JJhGo"
            }
        ],
        "mini_project": "Containerize your FastAPI backend and PostgreSQL database.",
        "certification": "Docker Certified Associate"
    },

    "AWS": {
        "difficulty": "Intermediate",
        "duration": "4-6 weeks",
        "resources": [
            {
                "title": "AWS Skill Builder",
                "provider": "AWS",
                "type": "Learning Platform",
                "url": "https://skillbuilder.aws/"
            },
            {
                "title": "AWS Cloud Practitioner Essentials",
                "provider": "AWS",
                "type": "Course",
                "url": "https://explore.skillbuilder.aws/"
            }
        ],
        "mini_project": "Deploy a FastAPI application on an AWS EC2 instance.",
        "certification": "AWS Certified Cloud Practitioner"
    },

    "PostgreSQL": {
        "difficulty": "Intermediate",
        "duration": "2-3 weeks",
        "resources": [
            {
                "title": "PostgreSQL Tutorial",
                "provider": "PostgreSQL",
                "type": "Documentation",
                "url": "https://www.postgresql.org/docs/current/tutorial.html"
            }
        ],
        "mini_project": "Design a normalized database for a job portal.",
        "certification": None
    },

    "MongoDB": {
        "difficulty": "Intermediate",
        "duration": "2-3 weeks",
        "resources": [
            {
                "title": "MongoDB University",
                "provider": "MongoDB",
                "type": "Course",
                "url": "https://learn.mongodb.com/"
            }
        ],
        "mini_project": "Build a hospital management database using MongoDB.",
        "certification": "MongoDB Associate Developer"
    },

    "Pandas": {
        "difficulty": "Intermediate",
        "duration": "2 weeks",
        "resources": [
            {
                "title": "Pandas Getting Started",
                "provider": "Pandas",
                "type": "Documentation",
                "url": "https://pandas.pydata.org/docs/getting_started/index.html"
            }
        ],
        "mini_project": "Clean and analyze a real-world CSV dataset.",
        "certification": None
    },

    "NumPy": {
        "difficulty": "Intermediate",
        "duration": "1-2 weeks",
        "resources": [
            {
                "title": "NumPy Learn",
                "provider": "NumPy",
                "type": "Documentation",
                "url": "https://numpy.org/learn/"
            }
        ],
        "mini_project": "Perform numerical analysis on student performance data.",
        "certification": None
    },

    "Statistics": {
        "difficulty": "Intermediate",
        "duration": "3-4 weeks",
        "resources": [
            {
                "title": "Statistics and Probability",
                "provider": "Khan Academy",
                "type": "Course",
                "url": "https://www.khanacademy.org/math/statistics-probability"
            }
        ],
        "mini_project": "Analyze survey data using descriptive statistics.",
        "certification": None
    },

    "Machine Learning": {
        "difficulty": "Advanced",
        "duration": "6-8 weeks",
        "resources": [
            {
                "title": "Machine Learning Crash Course",
                "provider": "Google",
                "type": "Course",
                "url": "https://developers.google.com/machine-learning/crash-course"
            },
            {
                "title": "Machine Learning with Python",
                "provider": "freeCodeCamp",
                "type": "Course",
                "url": "https://www.freecodecamp.org/learn/machine-learning-with-python/"
            }
        ],
        "mini_project": "Build a student placement prediction model.",
        "certification": "Google Professional Machine Learning Engineer"
    },

    "Scikit-learn": {
        "difficulty": "Intermediate",
        "duration": "2-3 weeks",
        "resources": [
            {
                "title": "Scikit-learn User Guide",
                "provider": "Scikit-learn",
                "type": "Documentation",
                "url": "https://scikit-learn.org/stable/user_guide.html"
            }
        ],
        "mini_project": "Create a classification model using Scikit-learn.",
        "certification": None
    },

    "TensorFlow": {
        "difficulty": "Advanced",
        "duration": "4-6 weeks",
        "resources": [
            {
                "title": "TensorFlow Tutorials",
                "provider": "TensorFlow",
                "type": "Documentation",
                "url": "https://www.tensorflow.org/tutorials"
            }
        ],
        "mini_project": "Build an image classification model using TensorFlow.",
        "certification": "TensorFlow Developer Certificate"
    },

    "PyTorch": {
        "difficulty": "Advanced",
        "duration": "4-6 weeks",
        "resources": [
            {
                "title": "PyTorch Tutorials",
                "provider": "PyTorch",
                "type": "Documentation",
                "url": "https://pytorch.org/tutorials/"
            }
        ],
        "mini_project": "Build a neural network classifier using PyTorch.",
        "certification": None
    },

    "Deep Learning": {
        "difficulty": "Advanced",
        "duration": "6-10 weeks",
        "resources": [
            {
                "title": "Deep Learning Specialization",
                "provider": "DeepLearning.AI",
                "type": "Course",
                "url": "https://www.coursera.org/specializations/deep-learning"
            }
        ],
        "mini_project": "Build a deep-learning model for image recognition.",
        "certification": "DeepLearning.AI Deep Learning Specialization"
    },

    "Power BI": {
        "difficulty": "Intermediate",
        "duration": "3-4 weeks",
        "resources": [
            {
                "title": "Power BI Learning",
                "provider": "Microsoft",
                "type": "Documentation",
                "url": "https://learn.microsoft.com/en-us/training/powerplatform/power-bi"
            }
        ],
        "mini_project": "Build an interactive sales analytics dashboard.",
        "certification": "Microsoft Power BI Data Analyst Associate"
    },

    "Tableau": {
        "difficulty": "Intermediate",
        "duration": "3-4 weeks",
        "resources": [
            {
                "title": "Tableau Training",
                "provider": "Tableau",
                "type": "Training",
                "url": "https://www.tableau.com/learn/training"
            }
        ],
        "mini_project": "Create a customer behavior dashboard.",
        "certification": "Tableau Desktop Specialist"
    },

    "Kubernetes": {
        "difficulty": "Advanced",
        "duration": "4-6 weeks",
        "resources": [
            {
                "title": "Kubernetes Basics",
                "provider": "Kubernetes",
                "type": "Documentation",
                "url": "https://kubernetes.io/docs/tutorials/kubernetes-basics/"
            }
        ],
        "mini_project": "Deploy a containerized application on Kubernetes.",
        "certification": "Certified Kubernetes Application Developer"
    },

    "CI/CD": {
        "difficulty": "Intermediate",
        "duration": "2-3 weeks",
        "resources": [
            {
                "title": "GitHub Actions Documentation",
                "provider": "GitHub",
                "type": "Documentation",
                "url": "https://docs.github.com/en/actions"
            }
        ],
        "mini_project": "Create a CI/CD pipeline for your CareerCompass project.",
        "certification": "GitHub Actions Certification"
    },

    "Terraform": {
        "difficulty": "Advanced",
        "duration": "3-4 weeks",
        "resources": [
            {
                "title": "Terraform Tutorials",
                "provider": "HashiCorp",
                "type": "Documentation",
                "url": "https://developer.hashicorp.com/terraform/tutorials"
            }
        ],
        "mini_project": "Provision an AWS EC2 instance using Terraform.",
        "certification": "HashiCorp Certified Terraform Associate"
    }
}


def get_default_recommendation(skill: str) -> dict[str, Any]:
    return {
        "difficulty": "Intermediate",
        "duration": "2-4 weeks",
        "resources": [
            {
                "title": f"Learn {skill}",
                "provider": "Official Documentation",
                "type": "Documentation",
                "url": ""
            }
        ],
        "mini_project": (
            f"Build a small practical project using {skill}."
        ),
        "certification": None
    }


def generate_learning_roadmap(
    missing_skills: list[str],
    priority_skills: list[str],
    target_career: str
) -> dict[str, Any]:
    if not missing_skills:
        return {
            "target_career": target_career,
            "total_recommendations": 0,
            "roadmap": [],
            "message": (
                "No major skill gaps were found. "
                "Focus on projects, interview preparation "
                "and advanced practice."
            )
        }

    roadmap = []

    ordered_skills = []

    for skill in priority_skills:
        if skill in missing_skills and skill not in ordered_skills:
            ordered_skills.append(skill)

    for skill in missing_skills:
        if skill not in ordered_skills:
            ordered_skills.append(skill)

    for position, skill in enumerate(ordered_skills, start=1):
        recommendation = LEARNING_RESOURCES.get(
            skill,
            get_default_recommendation(skill)
        )

        roadmap.append({
            "order": position,
            "skill": skill,
            "is_priority": skill in priority_skills,
            "difficulty": recommendation["difficulty"],
            "duration": recommendation["duration"],
            "resources": recommendation["resources"],
            "mini_project": recommendation["mini_project"],
            "certification": recommendation["certification"]
        })

    return {
        "target_career": target_career,
        "total_recommendations": len(roadmap),
        "roadmap": roadmap,
        "message": (
            f"Complete these learning steps to improve your "
            f"readiness for the {target_career} role."
        )
    }