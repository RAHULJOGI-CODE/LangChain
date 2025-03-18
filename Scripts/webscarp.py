import requests
from bs4 import BeautifulSoup

base_url = "https://brainlox.com"
category_url = f"{base_url}/courses/category/technical"

response = requests.get(category_url)
soup = BeautifulSoup(response.text, "html.parser")

# Course details
courses = []
course_cards = soup.find_all("div", class_="courses-content")  

for course in course_cards:
    title = course.find("h3").text.strip()  # Course title
    short_description = course.find("p").text.strip()  # Short description
    link = course.find("a")["href"]  # Relative course link
    full_link = base_url + link  # Absolute course URL

    # Extract price per session
    price_tag = course.find_previous("div", class_="price shadow")
    price = None
    if price_tag:
        price_span = price_tag.find("span", class_="price-per-session")
        if price_span:
            price_text = price_span.get_text(strip=True, separator=" ")
            price = int(price_text.replace("$", "").strip())

    # Extract number of lessons
    lessons_tag = course.find_next("li")
    lessons = None
    if lessons_tag:
        lessons_span = lessons_tag.find("i", class_="flaticon-agenda")
        if lessons_span:
            lessons_text = lessons_tag.get_text(strip=True, separator=" ")
            lessons = int(lessons_text.split()[0])  # Extract first number (lesson count)

    # Calculate total cost
    total_cost = price * lessons if price and lessons else "Not available"

#     # Visit course page to extract more details
    course_response = requests.get(full_link)
    course_soup = BeautifulSoup(course_response.text, "html.parser")

#     # Extract detailed course description
#     course_description_tag = course_soup.find("div", class_="courses-overview")
#     detailed_description = course_description_tag.find("p").get_text("\n", strip=True) if course_description_tag else "Not available"

    # circullam
    
    # Extract curriculum (if available)
    curriculum_tag = course_soup.find("div", class_="courses-curriculum")
    print(curriculum_tag)
    curriculum = []

#     if curriculum_tag:
#      session_tags = curriculum_tag.find_all("li")
#      for session in session_tags:
#           session_info = session.find_all("span", class_="courses-name")
#           if len(session_info) == 2:
#                     session_title = session_info[0].get_text(strip=True)  # e.g., "Session 1"
#                     session_content = session_info[1].get_text(strip=True)  # e.g., "Introduction to Scratch Programming"
#                     curriculum.append(f"{session_title}: {session_content}")

#     curriculum_text = "\n".join(curriculum) if curriculum else "Not available"

    courses.append({
        "title": title,
        "short_description": short_description,
        "link": full_link,
        "Price Per Session": f"${price}" if price else "Price not available",
        "Lessons": lessons if lessons else "Lessons not available",
        "Total Cost": f"${total_cost}" if total_cost != "Not available" else "Total Cost not available",
     #    "Detailed Description": detailed_description,
     #    "Curriculum": curriculum
    })

# Print extracted course details
i=1
for course in courses:
     if i == 5:
          break
     else:
          i += 1
          print(course)