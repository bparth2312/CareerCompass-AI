from __future__ import annotations

import asyncio

from datetime import (
    datetime,
    timedelta,
    timezone
)

from html import unescape
from typing import Any
from urllib.parse import quote_plus

import httpx

from app.config import YOUTUBE_API_KEY


# =========================================================
# API URLS
# =========================================================

YOUTUBE_SEARCH_URL = (
    "https://www.googleapis.com/youtube/v3/search"
)

YOUTUBE_VIDEOS_URL = (
    "https://www.googleapis.com/youtube/v3/videos"
)


# =========================================================
# SETTINGS
# =========================================================

# Only suggest YouTube videos with at least 1 lakh views.
MINIMUM_YOUTUBE_VIEWS = 100_000

# Ignore videos shorter than 8 minutes.
MINIMUM_VIDEO_DURATION_SECONDS = 8 * 60

# Search videos uploaded during the last three years.
DEFAULT_MONTHS_BACK = 36

# Cache recommendations for one hour.
CACHE_DURATION_MINUTES = 60

# Change this value whenever filtering logic changes.
CACHE_VERSION = "popular-videos-v4"


COURSE_CACHE: dict[
    str,
    dict[str, Any]
] = {}


# =========================================================
# TRUSTED YOUTUBE CHANNELS
# =========================================================

TRUSTED_CHANNEL_NAMES = {
    "freecodecamp.org",
    "freecodecamp",
    "programming with mosh",
    "traversy media",
    "codewithharry",
    "code with harry",
    "chai aur code",
    "hitesh choudhary",
    "tech with tim",
    "corey schafer",
    "fireship",
    "dave gray",
    "the net ninja",
    "academind",
    "apna college",
    "campusx",
    "geeksforgeeks",
    "google for developers",
    "microsoft developer",
    "aws developers",
    "simplilearn",
    "great learning",
    "edureka",
    "bro code",
    "telusko",
    "thenewboston",
    "web dev simplified",
    "javascript mastery",
    "amigoscode",
    "patrick loeber",
    "sentdex",
    "statquest",
    "krish naik",
    "codebasics",
    "piyush garg",
    "thapa technical",
    "wscubetech",
    "ws cube tech",
    "take u forward",
    "striver",
    "jenny's lectures",
    "neso academy"
}


# =========================================================
# SEARCH QUERIES
# =========================================================

SKILL_SEARCH_QUERIES = {
    "Python": [
        "Python complete course",
        "Python full course Hindi"
    ],

    "SQL": [
        "SQL complete course",
        "SQL full course Hindi"
    ],

    "HTML": [
        "HTML complete course",
        "HTML full course Hindi"
    ],

    "CSS": [
        "CSS complete course",
        "CSS full course Hindi"
    ],

    "JavaScript": [
        "JavaScript complete course",
        "JavaScript full course Hindi"
    ],

    "React": [
        "React JS complete course",
        "React JS full course Hindi"
    ],

    "Node.js": [
        "Node.js complete course",
        "Node.js full course Hindi"
    ],

    "Express.js": [
        "Express.js complete course",
        "Express JS REST API Hindi"
    ],

    "FastAPI": [
        "FastAPI complete course",
        "FastAPI tutorial Hindi"
    ],

    "REST API": [
        "REST API complete tutorial",
        "REST API tutorial Hindi"
    ],

    "Git": [
        "Git and GitHub complete course",
        "Git GitHub tutorial Hindi"
    ],

    "Docker": [
        "Docker complete course",
        "Docker tutorial Hindi"
    ],

    "AWS": [
        "AWS complete course",
        "AWS cloud practitioner Hindi"
    ],

    "PostgreSQL": [
        "PostgreSQL complete course",
        "PostgreSQL tutorial Hindi"
    ],

    "MongoDB": [
        "MongoDB complete course",
        "MongoDB tutorial Hindi"
    ],

    "Pandas": [
        "Pandas complete course",
        "Pandas tutorial Hindi"
    ],

    "NumPy": [
        "NumPy complete course",
        "NumPy tutorial Hindi"
    ],

    "Statistics": [
        "Statistics for data science course",
        "Statistics data science Hindi"
    ],

    "Machine Learning": [
        "Machine Learning Python complete course",
        "Machine Learning complete course Hindi"
    ],

    "Scikit-learn": [
        "Scikit-learn complete tutorial",
        "Scikit-learn tutorial Hindi"
    ],

    "TensorFlow": [
        "TensorFlow complete course",
        "TensorFlow tutorial Hindi"
    ],

    "PyTorch": [
        "PyTorch complete course",
        "PyTorch tutorial Hindi"
    ],

    "Deep Learning": [
        "Deep Learning complete course",
        "Deep Learning course Hindi"
    ],

    "Power BI": [
        "Power BI complete course",
        "Power BI course Hindi"
    ],

    "Tableau": [
        "Tableau complete course",
        "Tableau tutorial Hindi"
    ],

    "Kubernetes": [
        "Kubernetes complete course",
        "Kubernetes tutorial Hindi"
    ],

    "CI/CD": [
        "CI CD complete course",
        "CI CD tutorial Hindi"
    ],

    "Terraform": [
        "Terraform complete course",
        "Terraform tutorial Hindi"
    ]
}


# =========================================================
# OFFICIAL RESOURCES
# =========================================================

OFFICIAL_RESOURCES = {
    "Python": {
        "title": "Python Official Tutorial",
        "provider": "Python",
        "url": "https://docs.python.org/3/tutorial/"
    },

    "JavaScript": {
        "title": "MDN JavaScript Guide",
        "provider": "MDN",
        "url": (
            "https://developer.mozilla.org/"
            "en-US/docs/Web/JavaScript/Guide"
        )
    },

    "React": {
        "title": "React Official Learning Guide",
        "provider": "React",
        "url": "https://react.dev/learn"
    },

    "Node.js": {
        "title": "Node.js Learning Guide",
        "provider": "Node.js",
        "url": (
            "https://nodejs.org/en/learn/"
            "getting-started/introduction-to-nodejs"
        )
    },

    "Express.js": {
        "title": "Express Getting Started",
        "provider": "Express",
        "url": (
            "https://expressjs.com/en/starter/"
            "installing.html"
        )
    },

    "FastAPI": {
        "title": "FastAPI Official Tutorial",
        "provider": "FastAPI",
        "url": "https://fastapi.tiangolo.com/tutorial/"
    },

    "REST API": {
        "title": "MDN REST Guide",
        "provider": "MDN",
        "url": (
            "https://developer.mozilla.org/"
            "en-US/docs/Glossary/REST"
        )
    },

    "Git": {
        "title": "GitHub Git Guide",
        "provider": "GitHub",
        "url": (
            "https://docs.github.com/en/"
            "get-started/using-git/about-git"
        )
    },

    "Docker": {
        "title": "Docker Get Started",
        "provider": "Docker",
        "url": "https://docs.docker.com/get-started/"
    },

    "AWS": {
        "title": "AWS Skill Builder",
        "provider": "AWS",
        "url": "https://skillbuilder.aws/"
    },

    "PostgreSQL": {
        "title": "PostgreSQL Official Tutorial",
        "provider": "PostgreSQL",
        "url": (
            "https://www.postgresql.org/"
            "docs/current/tutorial.html"
        )
    },

    "MongoDB": {
        "title": "MongoDB University",
        "provider": "MongoDB",
        "url": "https://learn.mongodb.com/"
    },

    "Pandas": {
        "title": "Pandas Getting Started",
        "provider": "Pandas",
        "url": (
            "https://pandas.pydata.org/"
            "docs/getting_started/index.html"
        )
    },

    "NumPy": {
        "title": "NumPy Learning Resources",
        "provider": "NumPy",
        "url": "https://numpy.org/learn/"
    },

    "Machine Learning": {
        "title": "Google Machine Learning Crash Course",
        "provider": "Google",
        "url": (
            "https://developers.google.com/"
            "machine-learning/crash-course"
        )
    },

    "Scikit-learn": {
        "title": "Scikit-learn User Guide",
        "provider": "Scikit-learn",
        "url": (
            "https://scikit-learn.org/"
            "stable/user_guide.html"
        )
    },

    "TensorFlow": {
        "title": "TensorFlow Tutorials",
        "provider": "TensorFlow",
        "url": "https://www.tensorflow.org/tutorials"
    },

    "PyTorch": {
        "title": "PyTorch Tutorials",
        "provider": "PyTorch",
        "url": "https://pytorch.org/tutorials/"
    },

    "Kubernetes": {
        "title": "Kubernetes Basics",
        "provider": "Kubernetes",
        "url": (
            "https://kubernetes.io/docs/"
            "tutorials/kubernetes-basics/"
        )
    },

    "Terraform": {
        "title": "Terraform Tutorials",
        "provider": "HashiCorp",
        "url": (
            "https://developer.hashicorp.com/"
            "terraform/tutorials"
        )
    }
}


# =========================================================
# BASIC HELPERS
# =========================================================

def normalize_text(
    value: str | None
) -> str:
    return (
        value or ""
    ).strip().lower()


def clean_youtube_text(
    value: str | None
) -> str:
    return unescape(
        value or ""
    ).strip()


def is_trusted_channel(
    channel_title: str
) -> bool:
    normalized_channel = normalize_text(
        channel_title
    )

    return any(
        trusted_name in normalized_channel
        for trusted_name in TRUSTED_CHANNEL_NAMES
    )


def get_skill_search_queries(
    skill: str
) -> list[str]:
    direct_queries = (
        SKILL_SEARCH_QUERIES.get(skill)
    )

    if direct_queries:
        return direct_queries

    normalized_skill = normalize_text(
        skill
    )

    for configured_skill, queries in (
        SKILL_SEARCH_QUERIES.items()
    ):
        if (
            normalize_text(configured_skill)
            == normalized_skill
        ):
            return queries

    return [
        f"{skill} complete course",
        f"{skill} tutorial Hindi"
    ]


# =========================================================
# DURATION HELPERS
# =========================================================

def parse_iso_8601_duration(
    duration: str | None
) -> int:
    """
    Convert YouTube duration such as PT1H20M10S
    into seconds.
    """

    if not duration:
        return 0

    duration_text = duration.replace(
        "PT",
        ""
    )

    hours = 0
    minutes = 0
    seconds = 0

    current_number = ""

    for character in duration_text:
        if character.isdigit():
            current_number += character
            continue

        if not current_number:
            continue

        value = int(current_number)

        if character == "H":
            hours = value

        elif character == "M":
            minutes = value

        elif character == "S":
            seconds = value

        current_number = ""

    return (
        hours * 3600
        + minutes * 60
        + seconds
    )


def format_duration(
    duration_seconds: int
) -> str | None:
    if duration_seconds <= 0:
        return None

    hours = duration_seconds // 3600

    minutes = (
        duration_seconds % 3600
    ) // 60

    if hours > 0:
        return f"{hours}h {minutes}m"

    return f"{minutes}m"


def format_view_count(
    view_count: int
) -> str:
    """
    Convert:
    201452 -> 2.0L
    12000000 -> 1.2Cr
    """

    if view_count >= 10_000_000:
        return (
            f"{view_count / 10_000_000:.1f}Cr"
        )

    if view_count >= 100_000:
        return (
            f"{view_count / 100_000:.1f}L"
        )

    if view_count >= 1_000:
        return (
            f"{view_count / 1_000:.1f}K"
        )

    return str(view_count)


# =========================================================
# VIDEO VALIDATION
# =========================================================

def is_valid_learning_video(
    *,
    title: str,
    description: str,
    duration_seconds: int,
    view_count: int
) -> bool:
    combined_text = normalize_text(
        f"{title} {description}"
    )

    blocked_terms = {
        "#shorts",
        "youtube shorts",
        "trailer",
        "teaser",
        "reaction video",
        "meme",
        "podcast clip",
        "motivational video",
        "status video",
        "edit video"
    }

    if any(
        term in combined_text
        for term in blocked_terms
    ):
        return False

    if (
        duration_seconds
        < MINIMUM_VIDEO_DURATION_SECONDS
    ):
        return False

    if (
        view_count
        < MINIMUM_YOUTUBE_VIEWS
    ):
        return False

    return True


# =========================================================
# CACHE HELPERS
# =========================================================

def get_cache_key(
    skill: str,
    max_results: int,
    months_back: int
) -> str:
    return (
        f"{CACHE_VERSION}:"
        f"{normalize_text(skill)}:"
        f"{max_results}:"
        f"{months_back}:"
        f"{MINIMUM_YOUTUBE_VIEWS}"
    )


def get_cached_results(
    cache_key: str
) -> list[dict[str, Any]] | None:
    cache_entry = COURSE_CACHE.get(
        cache_key
    )

    if not cache_entry:
        return None

    created_at = cache_entry.get(
        "created_at"
    )

    resources = cache_entry.get(
        "resources"
    )

    if not isinstance(
        created_at,
        datetime
    ):
        COURSE_CACHE.pop(
            cache_key,
            None
        )

        return None

    if not isinstance(
        resources,
        list
    ):
        COURSE_CACHE.pop(
            cache_key,
            None
        )

        return None

    expires_at = (
        created_at
        + timedelta(
            minutes=CACHE_DURATION_MINUTES
        )
    )

    if (
        datetime.now(timezone.utc)
        >= expires_at
    ):
        COURSE_CACHE.pop(
            cache_key,
            None
        )

        return None

    valid_cached_videos = [
        resource
        for resource in resources
        if (
            resource.get("platform")
            != "YouTube"
            or int(
                resource.get(
                    "view_count",
                    0
                )
                or 0
            ) >= MINIMUM_YOUTUBE_VIEWS
        )
    ]

    return valid_cached_videos


def save_cached_results(
    cache_key: str,
    resources: list[dict[str, Any]]
) -> None:
    valid_resources = [
        resource
        for resource in resources
        if (
            resource.get("platform")
            != "YouTube"
            or int(
                resource.get(
                    "view_count",
                    0
                )
                or 0
            ) >= MINIMUM_YOUTUBE_VIEWS
        )
    ]

    COURSE_CACHE[cache_key] = {
        "created_at":
            datetime.now(timezone.utc),

        "resources":
            valid_resources
    }


def clear_course_cache() -> None:
    """
    Clear all cached course recommendations.
    """

    COURSE_CACHE.clear()


# =========================================================
# PLATFORM LINKS
# =========================================================

def create_platform_search_links(
    skill: str
) -> list[dict[str, Any]]:
    encoded_skill = quote_plus(
        skill
    )

    resources: list[
        dict[str, Any]
    ] = []

    official_resource = (
        OFFICIAL_RESOURCES.get(skill)
    )

    if official_resource:
        resources.append({
            "title":
                official_resource["title"],

            "provider":
                official_resource["provider"],

            "platform":
                "Official Documentation",

            "resource_type":
                "Official learning guide",

            "url":
                official_resource["url"],

            "thumbnail": None,
            "published_at": None,

            "description": (
                f"Learn {skill} using the official "
                "documentation and learning guide."
            ),

            "free": True,
            "is_recent": False,
            "is_trusted_channel": True,

            "duration": None,
            "duration_seconds": 0,

            "view_count": None,
            "formatted_views": None
        })

    resources.extend([
        {
            "title": (
                f"Search {skill} courses "
                "on Coursera"
            ),

            "provider": "Coursera",
            "platform": "Coursera",
            "resource_type": "Course search",

            "url": (
                "https://www.coursera.org/"
                f"search?query={encoded_skill}"
            ),

            "thumbnail": None,
            "published_at": None,

            "description": (
                f"Browse Coursera courses "
                f"related to {skill}."
            ),

            "free": False,
            "is_recent": False,
            "is_trusted_channel": False,

            "duration": None,
            "duration_seconds": 0,

            "view_count": None,
            "formatted_views": None
        },

        {
            "title": (
                f"Learn {skill} with "
                "freeCodeCamp"
            ),

            "provider": "freeCodeCamp",
            "platform": "freeCodeCamp",
            "resource_type": "Free tutorials",

            "url": (
                "https://www.freecodecamp.org/"
                f"news/search/?query={encoded_skill}"
            ),

            "thumbnail": None,
            "published_at": None,

            "description": (
                f"Find freeCodeCamp tutorials and "
                f"learning material for {skill}."
            ),

            "free": True,
            "is_recent": False,
            "is_trusted_channel": True,

            "duration": None,
            "duration_seconds": 0,

            "view_count": None,
            "formatted_views": None
        },

        {
            "title": (
                f"Search {skill} resources "
                "on Kaggle"
            ),

            "provider": "Kaggle",
            "platform": "Kaggle",

            "resource_type":
                "Free practice resources",

            "url": (
                "https://www.kaggle.com/search"
                f"?q={encoded_skill}"
            ),

            "thumbnail": None,
            "published_at": None,

            "description": (
                f"Explore notebooks, datasets "
                f"and practice material for {skill}."
            ),

            "free": True,
            "is_recent": False,
            "is_trusted_channel": False,

            "duration": None,
            "duration_seconds": 0,

            "view_count": None,
            "formatted_views": None
        }
    ])

    return resources


# =========================================================
# YOUTUBE SEARCH
# =========================================================

async def fetch_youtube_search_results(
    client: httpx.AsyncClient,
    query: str,
    published_after: str
) -> list[dict[str, Any]]:
    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": 50,

        # Established and popular videos are more likely
        # to appear when relevance is used.
        "order": "relevance",

        "publishedAfter": published_after,

        "regionCode": "IN",
        "safeSearch": "strict",

        "videoEmbeddable": "true",
        "videoSyndicated": "true",

        "key": YOUTUBE_API_KEY
    }

    response = await client.get(
        YOUTUBE_SEARCH_URL,
        params=params
    )

    response.raise_for_status()

    payload = response.json()

    return payload.get(
        "items",
        []
    )


# =========================================================
# VIDEO DETAILS
# =========================================================

def chunk_list(
    values: list[str],
    chunk_size: int
) -> list[list[str]]:
    return [
        values[index:index + chunk_size]
        for index in range(
            0,
            len(values),
            chunk_size
        )
    ]


async def fetch_video_details_batch(
    client: httpx.AsyncClient,
    video_ids: list[str]
) -> dict[str, dict[str, Any]]:
    if not video_ids:
        return {}

    params = {
        "part": (
            "snippet,"
            "contentDetails,"
            "statistics,"
            "status"
        ),

        "id": ",".join(
            video_ids
        ),

        "key": YOUTUBE_API_KEY
    }

    response = await client.get(
        YOUTUBE_VIDEOS_URL,
        params=params
    )

    response.raise_for_status()

    payload = response.json()

    details: dict[
        str,
        dict[str, Any]
    ] = {}

    for item in payload.get(
        "items",
        []
    ):
        video_id = item.get("id")

        if video_id:
            details[video_id] = item

    return details


async def fetch_all_video_details(
    client: httpx.AsyncClient,
    video_ids: list[str]
) -> dict[str, dict[str, Any]]:
    unique_ids = list(
        dict.fromkeys(video_ids)
    )

    batches = chunk_list(
        unique_ids,
        50
    )

    tasks = [
        fetch_video_details_batch(
            client,
            batch
        )
        for batch in batches
    ]

    if not tasks:
        return {}

    results = await asyncio.gather(
        *tasks
    )

    combined: dict[
        str,
        dict[str, Any]
    ] = {}

    for result in results:
        combined.update(
            result
        )

    return combined


# =========================================================
# MAIN YOUTUBE COURSE SEARCH
# =========================================================

async def search_youtube_courses(
    skill: str,
    max_results: int = 5,
    months_back: int = DEFAULT_MONTHS_BACK
) -> list[dict[str, Any]]:
    if not YOUTUBE_API_KEY:
        print(
            "YOUTUBE_API_KEY is missing."
        )

        return []

    safe_max_results = max(
        1,
        min(max_results, 10)
    )

    cache_key = get_cache_key(
        skill,
        safe_max_results,
        months_back
    )

    cached_results = get_cached_results(
        cache_key
    )

    if cached_results is not None:
        return cached_results

    published_after = (
        datetime.now(timezone.utc)
        - timedelta(
            days=months_back * 30
        )
    ).isoformat().replace(
        "+00:00",
        "Z"
    )

    queries = get_skill_search_queries(
        skill
    )

    try:
        async with httpx.AsyncClient(
            timeout=25.0
        ) as client:

            search_tasks = [
                fetch_youtube_search_results(
                    client,
                    query,
                    published_after
                )
                for query in queries
            ]

            search_results = (
                await asyncio.gather(
                    *search_tasks
                )
            )

            unique_items: dict[
                str,
                dict[str, Any]
            ] = {}

            for group in search_results:
                for item in group:
                    video_id = (
                        item.get("id", {})
                        .get("videoId")
                    )

                    if not video_id:
                        continue

                    if video_id in unique_items:
                        continue

                    unique_items[
                        video_id
                    ] = item

            video_ids = list(
                unique_items.keys()
            )

            video_details = (
                await fetch_all_video_details(
                    client,
                    video_ids
                )
            )

    except httpx.HTTPStatusError as error:
        print(
            "YouTube API HTTP error:",
            error.response.status_code,
            error.response.text
        )

        return []

    except (
        httpx.RequestError,
        ValueError
    ) as error:
        print(
            "YouTube API request failed:",
            error
        )

        return []

    resources: list[
        dict[str, Any]
    ] = []

    for video_id, search_item in (
        unique_items.items()
    ):
        detail = video_details.get(
            video_id
        )

        # Skip videos without proper details.
        if not detail:
            continue

        statistics = detail.get(
            "statistics"
        )

        content_details = detail.get(
            "contentDetails"
        )

        status_data = detail.get(
            "status",
            {}
        )

        detail_snippet = detail.get(
            "snippet",
            {}
        )

        if not isinstance(
            statistics,
            dict
        ):
            continue

        if not isinstance(
            content_details,
            dict
        ):
            continue

        raw_view_count = (
            statistics.get(
                "viewCount"
            )
        )

        # Skip the video when YouTube does not return views.
        if raw_view_count is None:
            continue

        try:
            view_count = int(
                raw_view_count
            )

        except (
            TypeError,
            ValueError
        ):
            continue

        # Strict 1 lakh view check.
        if (
            view_count
            < MINIMUM_YOUTUBE_VIEWS
        ):
            continue

        duration_seconds = (
            parse_iso_8601_duration(
                content_details.get(
                    "duration"
                )
            )
        )

        search_snippet = (
            search_item.get(
                "snippet",
                {}
            )
        )

        title = clean_youtube_text(
            detail_snippet.get(
                "title"
            )
            or search_snippet.get(
                "title"
            )
        )

        description = (
            clean_youtube_text(
                detail_snippet.get(
                    "description"
                )
                or search_snippet.get(
                    "description"
                )
            )
        )

        channel_title = (
            clean_youtube_text(
                detail_snippet.get(
                    "channelTitle"
                )
                or search_snippet.get(
                    "channelTitle"
                )
            )
            or "YouTube"
        )

        if not is_valid_learning_video(
            title=title,
            description=description,
            duration_seconds=
                duration_seconds,
            view_count=view_count
        ):
            continue

        privacy_status = (
            status_data.get(
                "privacyStatus"
            )
        )

        if (
            privacy_status
            not in {
                None,
                "public"
            }
        ):
            continue

        thumbnails = (
            detail_snippet.get(
                "thumbnails"
            )
            or search_snippet.get(
                "thumbnails"
            )
            or {}
        )

        thumbnail = (
            thumbnails.get(
                "maxres",
                {}
            ).get("url")

            or thumbnails.get(
                "standard",
                {}
            ).get("url")

            or thumbnails.get(
                "high",
                {}
            ).get("url")

            or thumbnails.get(
                "medium",
                {}
            ).get("url")

            or thumbnails.get(
                "default",
                {}
            ).get("url")
        )

        published_at = (
            detail_snippet.get(
                "publishedAt"
            )
            or search_snippet.get(
                "publishedAt"
            )
        )

        resources.append({
            "title": title,

            "provider":
                channel_title,

            "channel_title":
                channel_title,

            "platform":
                "YouTube",

            "resource_type":
                "Popular video course",

            "url": (
                "https://www.youtube.com/"
                f"watch?v={video_id}"
            ),

            "thumbnail":
                thumbnail,

            "published_at":
                published_at,

            "description":
                description,

            "free": True,
            "is_recent": True,

            "is_trusted_channel":
                is_trusted_channel(
                    channel_title
                ),

            "duration":
                format_duration(
                    duration_seconds
                ),

            "duration_seconds":
                duration_seconds,

            "view_count":
                view_count,

            "formatted_views":
                format_view_count(
                    view_count
                )
        })

    # Final strict filter.
    resources = [
        resource
        for resource in resources
        if int(
            resource.get(
                "view_count",
                0
            )
            or 0
        ) >= MINIMUM_YOUTUBE_VIEWS
    ]

    def ranking_key(
        resource: dict[str, Any]
    ) -> tuple[
        int,
        int,
        str,
        int
    ]:
        trusted_score = (
            1
            if resource.get(
                "is_trusted_channel"
            )
            else 0
        )

        views = int(
            resource.get(
                "view_count",
                0
            )
            or 0
        )

        published_at = (
            resource.get(
                "published_at"
            )
            or ""
        )

        duration = int(
            resource.get(
                "duration_seconds",
                0
            )
            or 0
        )

        return (
            trusted_score,
            views,
            published_at,
            duration
        )

    resources.sort(
        key=ranking_key,
        reverse=True
    )

    trusted_resources = [
        resource
        for resource in resources
        if resource.get(
            "is_trusted_channel"
        )
    ]

    other_resources = [
        resource
        for resource in resources
        if not resource.get(
            "is_trusted_channel"
        )
    ]

    selected_resources = (
        trusted_resources[
            :safe_max_results
        ]
    )

    remaining_slots = (
        safe_max_results
        - len(selected_resources)
    )

    if remaining_slots > 0:
        selected_resources.extend(
            other_resources[
                :remaining_slots
            ]
        )

    # Final safety check before saving.
    selected_resources = [
        resource
        for resource in selected_resources
        if resource.get(
            "view_count",
            0
        ) >= MINIMUM_YOUTUBE_VIEWS
    ]

    save_cached_results(
        cache_key,
        selected_resources
    )

    return selected_resources


# =========================================================
# ONE SKILL
# =========================================================

async def recommend_courses_for_skill(
    skill: str
) -> dict[str, Any]:
    youtube_resources = (
        await search_youtube_courses(
            skill=skill,
            max_results=5
        )
    )

    youtube_resources = [
        resource
        for resource in youtube_resources
        if resource.get(
            "view_count",
            0
        ) >= MINIMUM_YOUTUBE_VIEWS
    ]

    platform_resources = (
        create_platform_search_links(
            skill
        )
    )

    all_resources = (
        youtube_resources
        + platform_resources
    )

    return {
        "skill": skill,

        "minimum_youtube_views":
            MINIMUM_YOUTUBE_VIEWS,

        "latest_video_count":
            len(youtube_resources),

        "trusted_video_count": len([
            resource
            for resource
            in youtube_resources
            if resource.get(
                "is_trusted_channel"
            )
        ]),

        "free_resource_count": len([
            resource
            for resource
            in all_resources
            if resource.get("free")
        ]),

        "total_resources":
            len(all_resources),

        "resources":
            all_resources
    }


# =========================================================
# MULTIPLE SKILLS
# =========================================================

async def recommend_courses_for_skills(
    skills: list[str]
) -> list[dict[str, Any]]:
    cleaned_skills: list[str] = []

    seen_skills: set[str] = set()

    for skill in skills:
        clean_skill = str(
            skill
        ).strip()

        normalized_skill = (
            clean_skill.lower()
        )

        if not clean_skill:
            continue

        if normalized_skill in seen_skills:
            continue

        cleaned_skills.append(
            clean_skill
        )

        seen_skills.add(
            normalized_skill
        )

    # Limit requests to the first five missing skills.
    selected_skills = (
        cleaned_skills[:5]
    )

    if not selected_skills:
        return []

    tasks = [
        recommend_courses_for_skill(
            skill
        )
        for skill in selected_skills
    ]

    results = await asyncio.gather(
        *tasks
    )

    return list(results)