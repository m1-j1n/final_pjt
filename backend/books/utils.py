import os
import requests
import openai
from pathlib import Path
from django.conf import settings
import uuid
import random
from django.core.files.base import ContentFile

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
        model="gpt-4o",
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
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "당신은 글을 요약하고 핵심 키워드를 잘 뽑는 도우미입니다."},
            {"role": "user", "content": prompt}
        ]
    )

    result = response.choices[0].message.content.strip()
    return [kw.strip() for kw in result.split(",")]

def generate_image_with_openai(thread_title, thread_content, book_title, book_author):

    keyword_extractor_prompt = (
        f"""
        {book_author}의 책 {book_title}을 읽고 쓴 독서 다이어리의 감정을 분석해 키워드 5개를 추출하시오.
        키워드 추출이 완료됐다면 키워드를 기반으로 이미지 생성 AI에 제공할 프롬프트를 작성하시오.
        해당 프롬프트를 통해 해당 독서 다이어리 페이지의 썸네일 이미지를 생성 예정.
        생성할 최종 이미지는 추상적이고 모호한 형태의 초현실주의적인 그림이어야 함. 

        <독서 다이어리>
            <제목>{thread_title}</제목>
            <본문>{thread_content}</본문>
        </독서 다이어리>

        <답변 예시>
            불안, 격정, 찬란함, 노스텔지아, 희망이 담긴 Abstract expressionism 스타일의 추상화
        </답변 예시>

        답변 : 
        """
    )
    client = openai.OpenAI()
    keyword_extractor_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "당신은 이미지 생성 AI를 위한 프롬프트 작성 비서입니다."},
            {"role": "user", "content": keyword_extractor_prompt},
        ],
        max_tokens=2040,
        temperature=0.5
    )
    keyword_extractor_response = keyword_extractor_response.choices[0].message.content
    
    img_generator_prompt = keyword_extractor_response + " 어떠한 텍스트, 글자, 숫자, 심볼도 포함하지 않을 것"
    print(img_generator_prompt)

    response = client.images.generate(
        model="dall-e-3",
        prompt=img_generator_prompt,
        size="1792x1024",
        quality="standard",
        n=1,
    )

    image_url = response.data[0].url
    
    response_img = requests.get(image_url)
    if response_img.status_code == 200:
        output_dir = Path(settings.MEDIA_ROOT) / "post_cover_img"
        output_dir.mkdir(parents=True, exist_ok=True)
        file_name = f"{uuid.uuid4()}.png"
        file_path = output_dir / file_name
        file_path.write_bytes(response_img.content)
        return str(Path("post_cover_img") / file_name)

    return None
