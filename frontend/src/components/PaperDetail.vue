<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { GetPaperDetail } from '@/request/api'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()

const paper = ref<any>(null)
const loading = ref(true)

onMounted(async () => {
  const paperId = Number(route.params.paperId)
  if (!paperId) {
    ElMessage.error('无效的论文ID')
    router.push('/index/paperSearch')
    return
  }
  try {
    paper.value = await GetPaperDetail(paperId)
  } catch (e: any) {
    ElMessage.error('获取论文详情失败')
    router.push('/index/paperSearch')
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="paper-detail" v-loading="loading">
    <el-page-header @back="router.push('/index/paperSearch')" title="返回搜索" />

    <div v-if="paper" class="detail-content">
      <h2 class="paper-title">{{ paper.title }}</h2>

      <el-descriptions :column="2" border style="margin-top: 20px">
        <el-descriptions-item label="作者" :span="2">
          {{ paper.authors }}
        </el-descriptions-item>
        <el-descriptions-item label="会议/期刊">
          {{ paper.venue }}
        </el-descriptions-item>
        <el-descriptions-item label="年份">
          {{ paper.year }}
        </el-descriptions-item>
        <el-descriptions-item label="关键词" :span="2">
          <el-tag
            v-for="kw in (paper.keywords || '').split(',')"
            :key="kw"
            type="primary"
            effect="plain"
            style="margin-right: 6px; margin-bottom: 4px"
          >
            {{ kw.trim() }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="链接" :span="2" v-if="paper.url">
          <a :href="paper.url" target="_blank" rel="noopener">{{ paper.url }}</a>
        </el-descriptions-item>
      </el-descriptions>

      <div class="abstract-section">
        <h3>摘要</h3>
        <p class="abstract-text">{{ paper.abstract }}</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.paper-detail {
  padding: 20px;
}

.detail-content {
  margin-top: 20px;
}

.paper-title {
  font-size: 22px;
  line-height: 1.4;
  color: #303133;
}

.abstract-section {
  margin-top: 24px;
}

.abstract-section h3 {
  font-size: 16px;
  color: #606266;
  margin-bottom: 12px;
}

.abstract-text {
  font-size: 15px;
  line-height: 1.8;
  color: #303133;
  text-align: justify;
}
</style>
