import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useThreadStore = defineStore('counter', () => {
  let id = 0

  // threads 기본 데이터
  const threads = ref([
    {
      id: id++,
      bookId: 6,
      title: '이 책 정말 감명 깊었어요',
      content: '마지막 장면에서 눈물이 났습니다. 비슷한 책 추천도 부탁드려요!',
      datetime: '2025-05-16T10:30:00',
      comments: [] // 댓글 기본값은 빈 배열
    },
  ])


  // thread 생성 함수
  const createThread = function (bookId, title, content, datetime) {
    const newThread = {
      id: id++,
      bookId,
      title,
      content,
      datetime,
      comments: []
    }

    threads.value.push(newThread)
  }



  return { threads, createThread, }
})
