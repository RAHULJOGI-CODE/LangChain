import requests
import json
import re
from bs4 import BeautifulSoup

base_url = "https://brainlox.com"
category_url = f"{base_url}/courses/category/technical"

response = requests.get(category_url)
soup = BeautifulSoup(response.text, "html.parser")

# Course details
courses = []
course_cards = soup.find_all("div", class_="courses-content")

def clean_text(text):
    """Remove emojis, excessive whitespace, and special characters."""
    text = re.sub(r'[^\w\s.,!?-]', '', text)  # Remove emojis & special chars
    return text.strip()

for course in course_cards:
    title = clean_text(course.find("h3").text)  # Clean course title
    description = clean_text(course.find("p").text)  # Clean description
    link = course.find("a")["href"]
    full_link = f"{base_url}{link}"

    price_tag = course.find_previous("div", class_="price shadow")
    price = None
    if price_tag:
        price_span = price_tag.find("span", class_="price-per-session")
        if price_span:
            price_text = price_span.get_text(strip=True, separator=" ")
            price = int(price_text.replace("$", "").strip())

    lessons_tag = course.find_next("li")
    lessons = None
    if lessons_tag:
        lessons_span = lessons_tag.find("i", class_="flaticon-agenda")
        if lessons_span:
            lessons_text = lessons_tag.get_text(strip=True, separator=" ")
            lessons = int(lessons_text.split()[0])  

    total_cost = price * lessons if price and lessons else None

    course_response = requests.get(full_link)
    course_soup = BeautifulSoup(course_response.text, "html.parser")

    # Extract and clean course description
    course_description_tag = course_soup.find("div", class_="courses-overvie")
    detailed_description = clean_text(course_description_tag.find("p").get_text("\n", strip=True)) if course_description_tag else None

    courses.append({
        "title": title,
        "description": description,
        "link": full_link,
        "Price Per Session": f"${price}" if price else None,
        "Lessons": lessons,
        "Total Cost": f"${total_cost}" if total_cost else None,
        "Detailed Description": detailed_description,
    })

# Save cleaned data to JSON file
with open("cleaned_courses.json", "w", encoding="utf-8") as f:
    json.dump(courses, f, indent=4)

print("Cleaned data saved to cleaned_courses.json")