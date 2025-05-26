<template>
  <div class="container py-5">
    <h2 class="fw-bold text-center mb-5">✨ 다른 사람들의 인생 책이 궁금하다면?</h2>

    <div class="row row-cols-1 row-cols-md-3 g-4">
      <div v-for="post in uniquePosts" :key="post.id" class="col">
        <RouterLink :to="{ name: 'posts-detail', params: { postId: post.id } }" class="text-decoration-none text-dark">
          <div class="card h-100">
            <div class="post-img-container">
              <p>{{ post.cover_img }}</p> 
              <img
                v-if="post.cover_img"
                :src="getCoverImgUrl(post.cover_img)"
                class="card-img-top"
                style="width: 100%; height: 100%; object-fit: cover;"
                :alt="post.title"
              />







            </div>
            <div class="card-body d-flex flex-column justify-content-between">
              <div>
                <span class="badge bg-primary mb-2">카테고리 {{ post.category_id }}</span>
                <h5 class="card-title">{{ post.title }}</h5>
                <p class="card-text text-muted mb-3">
                  {{ post.content.slice(0, 100) }}<span v-if="post.content.length > 100">...</span>
                </p>
              </div>
              <div class="d-flex align-items-center">
                <img :src="post.user_profile || 'https://placehold.co/40x40'" class="rounded-circle me-2"
                  style="width: 40px; height: 40px; object-fit: cover;">
                <div>
                  <strong class="d-block">{{ post.user_name }}</strong>
                  <small class="text-muted">{{ post.created_at.slice(0, 10) }}</small>
                </div>
              </div>
            </div>
          </div>
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'

const posts = ref([])

const uniquePosts = computed(() => posts.value.slice(0, 1))

function getCoverImgUrl(coverImg) {
  console.log('📸 coverImg:', coverImg)
  if (!coverImg) return ''
  return coverImg.startsWith('http') ? coverImg : `http://127.0.0.1:8000/media/${coverImg}`
}


// const uniquePosts = computed(() => {
//   const seenBooks = new Set()
//   return posts.value.filter(post => {
//     const bookId = post.book || post.book_id
//     if (!bookId || seenBooks.has(bookId)) return false
//     seenBooks.add(bookId)
//     return true
//   }).slice(0, 9)
// })

onMounted(async () => {
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/v1/post/recommend/')
    posts.value = res.data
    console.log("📸 uniquePosts", uniquePosts.value)
    console.log('📦 받은 포스트:', res.data)  // ✅ 여기가 정확한 위치야!
    console.log(uniquePosts.value.map(p => p.id))
    console.log(posts.value[0]?.cover_img)

  } catch (err) {
    console.error('추천 포스트 로딩 실패:', err)
  }
})


</script>


<style scoped>
.card {
  transition: transform 0.2s ease-in-out;
  border-radius: 16px;
  overflow: hidden;
  height: 100%;
}

.card:hover {
  transform: scale(1.02);
}

.post-img-container {
  height: 200px;
  overflow: hidden;
}

.card-img-top {
  object-fit: cover;
  width: 100%;
  height: 100%;
}

</style>