from __future__ import annotations

import os
import time
import json
import asyncio
from typing import Optional
from urllib.parse import urlparse

import bs4
from bs4 import BeautifulSoup

import selenium.webdriver as webdriver
from selenium.webdriver.common.by import By

from fastapi import FastAPI

if not os.path.exists("./.__db/"):
    os.mkdir("./.__db/")

def __load_cookies():
    cookies = {}
    if not os.path.exists(os.path.join("./", ".__db/cookie.instagram.json")):
        return []

    with open("./.__db/cookie.instagram.json", "r") as f:
        cookies = json.load(f)
    
    for i in range(len(cookies)):
        try:
            if "expiry" in cookies[i]:
                cookies[i]["expires"] = cookie["expiry"]
        except:
            pass
        try:
            if "expires" in cookies[i]:
                cookies[i]["expiry"] = cookie["expires"]
        except:
            pass
    
    t = time.time()
    for cookie in cookies:
        if "expiry" in cookie or "expires" in cookie:
            if int(t) >= (int(cookie["expiry"]) - 120):
                return []
        
        
    return cookies

def __get_new_login_cookies():
    try: os.rmdir("./.__cache")
    except: pass

    IS_FIRST_RUN = True
    if os.path.exists("./.__cache"):
        IS_FIRST_RUN = False

    options = webdriver.ChromeOptions()
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("user-data-dir=./.__cache")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--headless')
    options.page_load_strategy = 'normal'
    options.unhandled_prompt_behavior = "dismiss"
    driver = webdriver.Chrome(options)
    driver.get("https://www.instagram.com/accounts/login")
    print( "[Instagram Driver] ┌ Getting Instagram Credentials")
    time.sleep(5)
    print( "[Instagram Driver] ├┬ Login Page Landed !")
    print(f"[Instagram Driver] │├ Inputting Username : ", os.environ['INSTAGRAM_USERNAME'])
    driver.find_element(By.NAME, "username").send_keys(os.environ['INSTAGRAM_USERNAME'])
    print(f"[Instagram Driver] │├ Inputting Password : ", "".join(["*" for i in range(len(os.environ['INSTAGRAM_PASSWORD']))]))
    driver.find_element(By.NAME, "password").send_keys(os.environ['INSTAGRAM_PASSWORD'])
    buttons = driver.find_elements(By.TAG_NAME, "button")
    for button in buttons:
        if button.get_attribute("type") == "submit":
            print("[Instagram Driver] │├ Logging In")
            button.click()
            break

    time.sleep(8)
    print("[Instagram Driver] │└ Done ! Logged In !")
    print("[Instagram Driver] ├┬ Gathering Cookies")

    cookies = driver.get_cookies()

    print("[Instagram Driver] ├┬ Saving Cookies")
    with open("./.__db/cookie.instagram.json", "w") as f:
        json.dump(cookies, f, indent=2)
    print("[Instagram Driver] │└ Done !")
    print("[Instagram Driver] └ Done !")
    return cookies

__DRIVER = None
def get_driver():
    global __DRIVER
    cookies = __load_cookies()
    if len(cookies) <= 0:
        cookies = __get_new_login_cookies()
    
    if __DRIVER:
        return __DRIVER

    options = webdriver.ChromeOptions()
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("user-data-dir=./.__cache")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--headless')
    options.page_load_strategy = 'normal'
    options.unhandled_prompt_behavior = "dismiss"

    __DRIVER = webdriver.Chrome(options)
    __DRIVER.execute_cdp_cmd("Network.enable", {})
    for cookie in cookies:
        __DRIVER.execute_cdp_cmd("Network.setCookie", cookie)
    __DRIVER.execute_cdp_cmd("Network.disable", {})
    return __DRIVER

class InstagramPostComment:
    def __init__(self, username: str, comment: str):
        self.__username = username
        self.__comment = comment
    
    @staticmethod
    def from_json(json: dict):
        return InstagramPostComment(
            json["username"],
            json["comment"]
        )
    
    @property
    def username(self):
        return self.__username

    @property
    def comment(self):
        return self.__comment
    
    @property
    def json(self):
        return {
            "username": self.__username,
            "comment": self.comment
        }

    def __repr__(self) -> str:
        return (self.username + ": " + self.comment).replace("\n.\n", ".").replace("\n.\n", ".").replace("\n.", ".").replace("\n\n", "\n").replace("\n\n", "\n").replace("\n\n", "\n").replace("\n", "  ")[0:64]

    def __str__(self) -> str:
        return self.__repr__()
    
class InstagramPost:
    def __init__(self, id: str, media: str, caption: str, date_post: str, comments: list[InstagramPostComment]):
        self.__id = id
        self.__media = media
        self.__caption = caption
        self.__date_post = date_post
        self.__comments = comments
    
    @staticmethod
    def from_json(json: dict):
        return InstagramPost(
            json["id"],
            json["media"],
            json["caption"],
            json["date_post"],
            [InstagramPostComment.from_json(c) for c in json["comments"]],
        )

    @property
    def id(self): return self.__id
    @property
    def media(self): return self.__media
    @property
    def caption(self): return self.__caption
    @property
    def date_post(self): return self.__date_post
    @property
    def comments(self): return self.__comments

    @property
    def title(self):
        separator = ["\n", "|", ".", ",", ";", ":", "-", "=", "!"]
        possible_titles = [(i, self.__caption.split(i)[0]) for i in separator]

        lowest_title = possible_titles[0][1]
        lowest_sep = possible_titles[0][0]
        for sep, title in possible_titles:
            if len(title) < len(lowest_title):
                lowest_title = title
                lowest_sep = sep

        if len(lowest_title) <= 48:
            return lowest_title + lowest_sep
        
        space_separated_title = self.__caption.split(" ")
        new_title = []
        for i in space_separated_title:
            if len(" ".join(new_title) + " " + i) >= 48:
                break

            new_title.append(i)
        
        return " ".join(new_title)

    @property
    def json(self):
        comments = [c.json for c in self.comments]
        return {
            "id": self.id,
            "media": self.media,
            "caption": self.caption,
            "date_post": self.date_post,
            "comments": comments
        }


    def __repr__(self) -> str:
        p = [
             "[Instagram Driver] ├┬ Instagram Post: " + self.id,
            ("[Instagram Driver] │├ Media: " + urlparse(self.media).path.split("/")[-2])[0:64] + "...",
            ("[Instagram Driver] │├ Caption: " + self.caption).replace("\n.\n", ".").replace("\n.\n", ".").replace("\n.", ".").replace("\n\n", "\n").replace("\n\n", "\n").replace("\n\n", "\n").replace("\n", "  ")[0:64] + "...",
             "[Instagram Driver] │├ Post Date: " + self.date_post,
             "[Instagram Driver] │├┬ Comments: ",
        ]
        cs = self.comments if len(self.comments) <= 5 else self.comments[0:5]
        for comment in cs:
            p.append(("[Instagram Driver] ││├ " + comment.__str__())[0:64] + "...")

        if len(self.comments) > 5:
            p.append("[Instagram Driver] ││└ ... ")    
        else:
            p[-1] = p[-1].replace("[Instagram Driver] ││├ ", "[Instagram Driver] ││└ ")
        p.append("[Instagram Driver] │└ Done ! ")

        return "\n".join(p)
    
    def __str__(self) -> str:
        return self.__repr__()

class InstagramProfile:
    def __init__(self, id: str, profile_icon: str, name: str, description: str, posts: list[InstagramPost] = []):
        self.__id = id
        self.__profile_icon = profile_icon
        self.__name = name
        self.__description = description
        self.__posts = posts

    @staticmethod
    def from_json(json: dict):
        return InstagramProfile(
            json["id"],
            json["profile_icon"],
            json["name"],
            json["description"],
            [InstagramPost.from_json(post) for post in json["posts"]],
        )
    
    @property
    def id(self): return self.__id
    @property
    def profile_icon(self): return self.__profile_icon
    @property
    def name(self): return self.__name
    @property
    def description(self): return self.__description
    @property
    def posts(self): return self.__posts

    @property
    def json(self):
        posts = [p.json for p in self.posts]
        return {
            "id": self.id,
            "profile_icon": self.profile_icon,
            "name": self.name,
            "description": self.description,
            "posts": posts
        }

    def __repr__(self) -> str:
        p = [
            "\n",
            "\n[Instagram Driver] ┌ Instagram Profile: @" + self.id,
            "\n[Instagram Driver] ├ Name: " + self.name,
            "\n" + ("[Instagram Driver] ├ Description: " + self.description).replace("\n.\n", ".").replace("\n.\n", ".").replace("\n.", ".").replace("\n\n", "\n").replace("\n\n", "\n").replace("\n\n", "\n").replace("\n", "  ")[0:64] + "...\n",
            *[i.__str__() for i in self.__posts]
        ]

        return "".join(p)

__WATCHING_IS_DONE = True
async def parse_instagram_post(page_source: str):
    global __WATCHING_IS_DONE
    __WATCHING_IS_DONE = False
    soup = BeautifulSoup(page_source, "html.parser")

    caption = soup.find("h1", { "class": "_aacl" })
    if not caption: caption = ""
    else:
        d = ""
        for c in caption.contents:
            t = c.text
            if t == "":
                d += "\n"
            else:
                d += t
        
        caption = d

    post_time = soup.find("time", { "class": "_aaqe" })
    if not post_time: post_time = ""
    else:
        try: post_time = post_time.text
        except: post_time = ""

    ul_comments: list[bs4.element.Tag | bs4.element.NavigableString] = soup.find_all("ul", { "class": "_a9ym" })
    comments: list[InstagramPostComment] = []
    for ul in ul_comments:
        username = "@" + ul.find("a", { "class": "x1i10hfl" })["href"].replace("/", "")
        comment = ul.find("span", { "class": "_aacl" })
        if not comment:
            continue
        else:
            try: comment = comment.text
            except: continue
        comments.append(InstagramPostComment(username, comment))

    
    img_url = soup.find("div", { "role": "button" })
    if not img_url: img_url = ""
    else:
        img = img_url.find("div", { "class": "_aagv" })
        if img:
            img_url = img_url.img["src"]
        else:
            img_url = img_url.find("video", { "class": "x1lliihq" })["src"]
    
    return {
        "img_url": img_url,
        "caption": caption,
        "post_time": post_time,
        "comments": comments
    }

async def get_page_source(driver: webdriver.Chrome, link: str):
    driver.get(link)
    await asyncio.sleep(4)
    return driver.page_source

async def get_instagram_user(ig_id: str, ignored_post_ids: list[str]):
    global __WATCHING_IS_DONE
    __WATCHING_IS_DONE = False
    print("[Instagram Driver] ┌ Getting Instagram Profile:", ig_id)

    driver = get_driver()
    driver.get("https://instagram.com/" + ig_id)
    time.sleep(3)
    source = driver.page_source

    soup = BeautifulSoup(source, "html.parser")
    print("[Instagram Driver] ├ Getting Profile Name")
    profile_name = soup.find("div", { "class": "_aa_c" })
    if not profile_name:
        profile_name = ""
    else:
        profile_name = profile_name.find("span", { "class": "x1lliihq" }).contents[0]
        if not profile_name:
            profile_name = ""

    print("[Instagram Driver] ├ Getting Profile Description")
    profile_desc = soup.find("div", { "class": "_aa_c" })
    if not profile_desc:
        profile_desc = ""
    else:
        profile_desc = profile_desc.find("h1", { "class": "_aacl" })
        if not profile_desc:
            profile_desc = ""
        else:
            profile_desc = profile_desc.contents[0]
    
    print("[Instagram Driver] ├ Getting Profile Image")
    try: profile_image = soup.findAll("img", { "class": "xpdipgo" })[1]
    except: profile_image = soup.findAll("img", { "class": "xpdipgo" })[0]
    if not profile_image:
        profile_image = ""
    else:
        profile_image = profile_image["src"]

    print("[Instagram Driver] ├ Getting Post List")
    article = soup.find("article", { "class": "x1iyjqo2" })
    post_url = []
    for a in article.findAll("a", { "class": "x1i10hfl" }):
        try: post_url.append(a["href"].split("/")[-2])
        except: pass
    
    post_url = [url for url in post_url if url not in ignored_post_ids]
    print("[Instagram Driver] ├┬ Gathering Post Info and Resource")

    post_sources = []
    for url in post_url:
        print("[Instagram Driver] │├ Scraping post_id:", url)
        driver.get("https://instagram.com/p/" + url)
        await asyncio.sleep(3)
        post_sources.append((url, driver.page_source))
    print("[Instagram Driver] │└ Done !")
    print("[Instagram Driver] ├ Parsing scraped post sources")

    posts = []
    for url, source in post_sources:
        try:
            post = await parse_instagram_post(source)
            posts.append(InstagramPost(
                url,
                post["img_url"],
                post["caption"],
                post["post_time"],
                post["comments"]
            ))
        except Exception as e:
            print(f"[Instagram Driver] ├ post {url} skipped cause:", str(e)[0:80] + "...")
    print("[Instagram Driver] └ Done !")

    return InstagramProfile(ig_id, profile_image, profile_name, profile_desc, posts)


if not os.path.exists(os.path.join("./", ".__db/news.instagram_watch.json")):
    with open("./.__db/news.instagram_watch.json", "w") as f:
        json.dump([], f, indent=2)

if not os.path.exists(os.path.join("./", ".__db/ignored_post.instagram_watch.json")):
    with open("./.__db/ignored_post.instagram_watch.json", "w") as f:
        json.dump([], f, indent=2)

if not os.path.exists("./.__db/posts.instagram_watch.json"):
    with open("./.__db/posts.instagram_watch.json", "w") as f:
        json.dump([], f, indent=2)

async def add_to_pooled_post(new_post: InstagramPost):
    while True:
        try:
            with open("./.__db/posts.instagram_watch.json", "r") as f:
                posts: list[InstagramPost] = [InstagramPost.from_json(i) for i in json.load(f)]
            break
        except Exception as e:
            print(e)
            continue
    
    posts.append(new_post)

    while True:
        try:
            with open("./.__db/posts.instagram_watch.json", "w") as f:
                json.dump([i.json for i in posts], f, indent=2)
            break
        except Exception as e:
            print(e)
            continue

async def get_all_pooled():
    while True:
        try:
            with open("./.__db/posts.instagram_watch.json", "r") as f:
                posts: list[InstagramPost] = [InstagramPost.from_json(i) for i in json.load(f)]
            break
        except Exception as e:
            print(e)
            continue
    
    return posts

async def get_one_from_pooled():
    posts = await get_all_pooled()
    if len(posts) <= 0: return None
    popped = posts.pop(0)

    while True:
        try:
            with open("./.__db/posts.instagram_watch.json", "w") as f:
                json.dump(posts, f, indent=2)
            break
        except Exception as e:
            print(e)
            continue
    
    return popped

async def get_all_watch_list():
    while True:
        try:
            with open("./.__db/news.instagram_watch.json", "r") as f:
                saved_watch_list: list[str] = json.load(f)
            break
        except Exception as e:
            print(e)
            continue
    
    return saved_watch_list

async def add_to_watch_list(ig_id: str):
    saved_watch_list = await get_all_watch_list()
    saved_watch_list.append(ig_id)

    while True:
        try:
            with open("./.__db/news.instagram_watch.json", "w") as f:
                json.dump(saved_watch_list, f, indent=2)
            break
        except Exception as e:
            print(e)
            continue

async def get_all_ignored_post():
    while True:
        try:
            with open("./.__db/ignored_post.instagram_watch.json", "r") as f:
                ignored_post_list: list[str] = json.load(f)
            break
        except Exception as e:
            print(e)
            continue

    return ignored_post_list

async def watch():
    global __WATCHING_IS_DONE
    saved_watch_list = await get_all_watch_list()
    ignored_post_list = await get_all_ignored_post()
    
    if len(saved_watch_list) <= 0:
        __WATCHING_IS_DONE = True
        return
    

    print("[Instagram Driver: watch] Scraping Started!")
    for user_id in saved_watch_list:
        __WATCHING_IS_DONE = False
        user: InstagramProfile = None
        for _ in range(3):
            try:
                user = await get_instagram_user(user_id, ignored_post_list + [i.id for i in await get_all_pooled()])
                break
            except Exception as e:
                print(e)
                print("Retrying...")
                continue

        for post in user.posts:
            await add_to_pooled_post(post)

    __WATCHING_IS_DONE = True

async def watch_timer():
    print("[Instagram Driver: watch_timer] Timer Started!")
    while True:
        await asyncio.sleep(1)
        if not __WATCHING_IS_DONE:
            continue
        
        print("[Instagram Driver: watch_timer] Watching Instagram")
        asyncio.ensure_future(watch())

############ API ------
app = FastAPI(debug=True, title="Instagram Watcher")

@app.on_event("startup")
async def app_startup():
    asyncio.create_task(watch_timer(), name="watch_timer")

@app.post("/{instagram_id}")
async def add_to_watch_list(instagram_id: str):
    asyncio.ensure_future(add_to_watch_list(instagram_id))
    return True

@app.post("/")
async def get_one_post():
    p = await get_one_from_pooled()
    if not p: return False
    return p.json