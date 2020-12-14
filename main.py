from utils import authorizer, fix_bads, get_problem

USERNAME = "YOUR_USERNAME"
PASSWORD = "YOUR_PASSWORD"
COURSE_URL = "https://courses.openedu.ru/courses/course-v1:spbstu+MATHPH+fall_2020/courseware/9c203a328aa346eb89da102cbb8813fe/a19be83529304950b32a8d21c1f51af6/1?activate_block_id=block-v1%3Aspbstu%2BMATHPH%2Bfall_2020%2Btype%40vertical%2Bblock%401705783cbc894ddebeb0bb8edc844d7f"

if __name__ == "__main__":
    client = authorizer(USERNAME, PASSWORD)
    page = fix_bads(client.get(COURSE_URL).text)
    out = get_problem(page)
