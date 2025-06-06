import os
import requests
import openai
from pathlib import Path
from django.conf import settings
import uuid
import random
from django.core.files.base import ContentFile
from random import sample

# get_random_image_file : 포스트 생성 시 디폴트 이미지 저장
PICSUM_SEEDS = list(range(100, 200))

def get_random_image_file():
    seed = random.choice(range(100, 200))  # 고정된 seed 사용
    url = f"https://picsum.photos/seed/{seed}/400/300"
    response = requests.get(url)
    
    if response.status_code == 200:
        file_name = f"random_{seed}.jpg"
        return ContentFile(response.content, name=file_name)
    return None

# generate_reason : 추천 이유를 생성해주는 함수
from openai import OpenAI
client = OpenAI(api_key=settings.OPENAI_API_KEY)
def generate_recommendation_summary(user_books, recommended_books):
    """
    user_books: 사용자가 읽은 책 제목 리스트
    recommended_books: 추천된 책들의 제목 리스트
    """
    user_list = ", ".join(user_books)
    rec_list = ", ".join([book.title for book in recommended_books])

    prompt = (
    f"{user_list}를 읽은 독자에게 잘 어울리는 책들입니다: {rec_list}.\n"
    f"이 추천 리스트의 공통된 매력이나 연결점을 2문장 이내로 설명해주세요. 너무 과장되거나 뻔한 표현은 피하고, 자연스럽게 독서 큐레이터처럼 안내해주세요."
)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "당신은 책 추천 전문가입니다."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content.strip()

# extract_keywords_from_content : 키워드 추출 함수
def extract_keywords_from_content(content):
    prompt = (
        f"다음 글에서 핵심 키워드 3개를 뽑아주세요. 각 키워드는 1~2단어로 짧고 명확하게.\n\n"
        f"글:\n{content}\n\n"
        f"출력 형식: 키워드1, 키워드2, 키워드3"
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "당신은 글을 요약하고 핵심 키워드를 잘 뽑는 도우미입니다."},
            {"role": "user", "content": prompt}
        ]
    )

    result = response.choices[0].message.content.strip()
    return [kw.strip() for kw in result.split(",")]


def build_prompt(answers, books):
    # 🔥 길이 자르고 \n 제거
    def short_text(txt, length):
        return txt.replace('\n', ' ').strip()[:length]

    # 🔥 무작위로 20~30권만 추출
    sampled_books = sample(books, min(30, len(books)))

    book_lines = []
    for b in sampled_books:
        book_lines.append(
            f"- 제목: {b['title']}, 소개: {short_text(b['description'], 80)}..., 작가: {b['author']} ({short_text(b['author_info'], 40)}...)"
        )

    book_list = '\n'.join(book_lines)

    return f"""
        당신은 책 추천 전문가입니다.

        사용자의 설문 응답은 다음과 같습니다:
        - 상태: {answers['mood']}
        - 관심 분야: {answers['interest']}
        - 선호 스타일: {answers['style']}
        - 독서 이유: {answers['reason']}

        다음 책 목록 중 사용자에게 가장 잘 맞는 책 3~5권을 추천해 주세요.
        책 정보는 간단하게 소개만 보고 판단하세요. 설명이 짧은 편이며 일부 생략되어 있습니다.
        각 책의 제목과 간단한 추천 이유를 함께 작성해 주세요.
        각 항목은 다음 형식으로 출력해주세요:
        1. 제목 - 추천 이유

        책 목록:
        {book_list}
        """

def parse_response(content, answers, books):
    lines = content.strip().split('\n')
    result = []

    # 설문에서 가져온 키워드 3개
    keywords = [answers.get('mood'), answers.get('interest'), answers.get('style')]

    for line in lines:
        if '-' in line:
            parts = line.split('-', 1)
            title = parts[0].strip("1234567890. ").strip('"“” ')
            reason = parts[1].strip()
        else:
            title = line.strip("1234567890. ").strip('"“” ')
            reason = "추천 이유 없음"

        # 🔍 books 리스트에서 해당 title을 가진 book 찾기
        matched_book = next((b for b in books if b['title'] == title), None)

        if title and matched_book:
            result.append({
                'title': title,
                'reason': reason,
                'id': matched_book.get('id'),  # ✅ id 추가!
                'cover': matched_book.get('cover'),
                'author': matched_book.get('author'),
                'description': matched_book.get('description')[:100],
                'keywords': keywords
            })

    return result



def get_gpt_recommendation(answers, books):
    prompt = build_prompt(answers, books)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "당신은 책 추천 전문가입니다."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
    )

    content = response.choices[0].message.content.strip()

    # books 전달 추가
    return parse_response(content, answers, books)
