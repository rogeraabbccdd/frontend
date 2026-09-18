<template>
  <section id="showcase" :class="hideHeader ? 'pt-8 pb-20 sm:pb-24 bg-transparent relative' : 'py-24 bg-slate-900/40 border-t border-slate-800/60 relative'">
    <div class="max-w-[1536px] mx-auto px-4 sm:px-6 lg:px-8 2xl:px-12">

      <!-- 期別篩選頁籤 (期別由 CMS 資料動態推導，由新到舊排列) -->
      <div v-if="!props.limit && batchTabs.length > 2" class="mb-8">
        <SegmentedNav
          v-model="activeBatch"
          :items="batchTabs"
          variant="tab"
          accent="cyan"
          id-prefix="showcase-batch"
          aria-label="依期別篩選專題作品"
        />
      </div>

      <!-- 作品網格清單 (以頁碼 key 驅動平滑淡入淡出轉場) -->
      <Transition name="page-fade" mode="out-in">
        <div id="showcase-cards-grid" :key="`${activeBatch}-${currentPage}`" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          <div
            v-for="project in displayedProjects"
            :key="project.id"
            class="showcase-card h-84 perspective-1000 group cursor-pointer rounded-3xl focus-visible:ring-2 focus-visible:ring-cyan-400 focus:outline-none transform-gpu"
            tabindex="0"
            role="button"
            :aria-expanded="flippedIds.has(project.id)"
            :aria-label="`${project.project_name} 專案卡片，作者 ${project.student_name}，按 Enter 或 Space 鍵翻轉查看詳情`"
            @click="toggleFlip(project.id)"
            @keydown.enter.prevent="toggleFlip(project.id)"
            @keydown.space.prevent="toggleFlip(project.id)"
          >
            <!-- 翻轉內層容器 -->
            <div
              class="relative w-full h-full duration-500 transform-style-3d transition-transform rounded-3xl shadow-xl"
              :class="flippedIds.has(project.id) ? 'rotate-y-180' : ''"
            >
              <!-- 1. 卡片正面 (對齊全站深色科技主題與極光流光線) -->
              <div class="card-subsurface-glow absolute inset-0 w-full h-full backface-hidden rounded-3xl overflow-hidden bg-slate-900/70 hover:bg-slate-900/90 backdrop-blur-xl border border-slate-800/90 flex flex-col justify-between shadow-xl shadow-slate-950/60">
                <!-- 頂部流光光暈線 (Hover 時優雅顯現) -->
                <div class="absolute top-0 left-0 right-0 h-[2px] bg-gradient-to-r from-transparent via-cyan-400 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none z-20"></div>

                <!-- 封面圖片相框 -->
                <div class="relative h-44 bg-slate-800 overflow-hidden">
                  <img
                    v-if="project.cover_image_url && !brokenProjectImages.has(project.id)"
                    :src="getProjectImageUrl(project)"
                    :alt="project.image_alt || project.project_name || '學員專題作品成果縮圖'"
                    loading="lazy"
                    decoding="async"
                    @error="handleImgError(project)"
                    class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                  />
                  <div v-else class="w-full h-full flex items-center justify-center bg-gradient-to-br from-slate-800 to-slate-900 text-cyan-400">
                    <Code2 class="w-10 h-10" :stroke-width="1.75" aria-hidden="true" />
                  </div>

                  <div class="absolute bottom-2 right-2 px-2.5 py-1 rounded-md bg-black/75 backdrop-blur-md text-sm text-slate-200 flex items-center gap-1.5">
                    <Eye class="w-4 h-4" :stroke-width="1.75" aria-hidden="true" />
                    <span>{{ project.view_count }} 次瀏覽</span>
                  </div>
                </div>

                <!-- 正面資訊區塊 -->
                <div class="p-5 flex-1 flex flex-col justify-between relative z-10">
                  <div>
                    <h3 class="font-extrabold text-white text-base truncate mb-1 group-hover:text-cyan-300 transition-colors">
                      {{ project.project_name }}
                    </h3>
                    <div class="text-sm text-slate-300 font-medium">
                      開發者：{{ project.student_name }}
                    </div>
                  </div>

                  <div class="flex items-center justify-between pt-3 border-t border-slate-800/80">
                    <span class="text-sm text-slate-300 font-semibold">
                      {{ project.batch_tag || '' }}
                    </span>
                    <span class="text-sm text-cyan-400 font-bold flex items-center gap-1">
                      <span>查看詳情</span>
                    </span>
                  </div>
                </div>
              </div>

              <!-- 2. 卡片背面 (展示詳細資訊與 Demo 連結，加入滾動防呆保護) -->
              <div class="card-subsurface-glow absolute inset-0 w-full h-full backface-hidden rotate-y-180 rounded-3xl p-5 sm:p-6 bg-slate-900/95 backdrop-blur-xl border border-cyan-500/40 flex flex-col justify-between shadow-2xl shadow-cyan-950/60 overflow-y-auto no-scrollbar">
                <!-- 頂部流光光暈線 -->
                <div class="absolute top-0 left-0 right-0 h-[2px] bg-gradient-to-r from-transparent via-cyan-400 to-transparent"></div>


                <div class="relative z-10">
                  <span class="px-2.5 py-1 rounded-full bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 text-sm font-bold">
                    專案詳情
                  </span>
                  <h3 class="text-lg font-extrabold text-white mt-3 mb-1">
                    {{ project.project_name }}
                  </h3>
                  <div class="text-sm text-slate-300 mb-2">
                    作者：<strong class="text-white">{{ project.student_name }}</strong>
                  </div>
                </div>

                <div class="space-y-2 pt-2 relative z-10">
                  <a
                    :href="project.demo_url"
                    target="_blank"
                    rel="noopener noreferrer"
                    :tabindex="flippedIds.has(project.id) ? 0 : -1"
                    :aria-label="`${project.project_name} 線上即時展示 Demo（另開新分頁）`"
                    @click.stop="handleView(project.id)"
                    class="w-full min-h-[44px] rounded-xl text-center font-bold text-sm text-white bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 shadow-md shadow-cyan-500/20 transition-all flex items-center justify-center space-x-1.5 focus-visible:ring-2 focus-visible:ring-white focus:outline-none cursor-pointer"
                  >
                    <Globe class="w-4 h-4 shrink-0" :stroke-width="1.75" aria-hidden="true" />
                    <span>線上即時展示 (Demo)</span>
                    <ExternalLink class="w-3.5 h-3.5 shrink-0" :stroke-width="1.75" aria-hidden="true" />
                  </a>
                  <button
                    type="button"
                    :tabindex="flippedIds.has(project.id) ? 0 : -1"
                    aria-label="返回正面卡片"
                    @click.stop="toggleFlip(project.id)"
                    class="w-full min-h-[44px] rounded-xl text-center font-medium text-sm text-slate-300 hover:text-white bg-slate-800/40 hover:bg-slate-800 transition-colors focus-visible:ring-2 focus-visible:ring-cyan-400 focus:outline-none"
                  >
                    返回正面
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </Transition>

      <!-- 8 個為一頁之極致科技感分頁控制器 (當非首頁 limit 模式且總頁數 > 1 時顯示) -->
      <div
        v-if="!props.limit && totalPages > 1"
        class="mt-14 pt-8 border-t border-slate-800/80 flex flex-col sm:flex-row items-center justify-between gap-6"
      >
        <!-- 頁面資訊摘要標籤 -->
        <div class="text-xs sm:text-sm text-slate-400 font-medium order-2 sm:order-1 flex items-center space-x-2">
          <span class="inline-block w-2 h-2 rounded-full bg-cyan-400 animate-pulse"></span>
          <span>共 <strong class="text-white font-bold">{{ filteredProjects.length }}</strong> 件專題作品 ｜ 每頁 8 件 ｜ 第 <strong class="text-cyan-400">{{ currentPage }}</strong> / {{ totalPages }} 頁</span>
        </div>

        <!-- 分頁切換按鈕群 (WAI-ARIA 導航規範) -->
        <nav class="flex items-center space-x-2 order-1 sm:order-2" aria-label="專案成果分頁導航">
          <!-- 上一頁按鈕 -->
          <button
            type="button"
            @click="goToPage(currentPage - 1)"
            :disabled="currentPage === 1"
            class="min-h-[44px] px-4 rounded-xl text-sm font-semibold transition-all border flex items-center gap-1.5"
            :class="[
              currentPage === 1
                ? 'bg-slate-900/50 border-slate-800 text-slate-600 cursor-not-allowed'
                : 'bg-slate-900 hover:bg-slate-850 border-slate-800 hover:border-cyan-500/40 text-slate-200 hover:text-cyan-300 shadow-md'
            ]"
            aria-label="前往上一頁專案列表"
          >
            <ChevronLeft class="w-4 h-4" :stroke-width="2" aria-hidden="true" />
            <span>上一頁</span>
          </button>

          <!-- 數字頁碼按鈕組 -->
          <div class="flex items-center space-x-1.5">
            <button
              v-for="page in totalPages"
              :key="page"
              type="button"
              @click="goToPage(page)"
              :aria-current="currentPage === page ? 'page' : undefined"
              :aria-label="`前往第 ${page} 頁`"
              class="w-11 h-11 rounded-xl text-sm font-bold transition-all flex items-center justify-center"
              :class="[
                currentPage === page
                  ? 'bg-gradient-to-r from-cyan-500 to-blue-600 text-white shadow-lg shadow-cyan-500/30 ring-2 ring-cyan-400 scale-105'
                  : 'bg-slate-900 hover:bg-slate-800 border border-slate-800 hover:border-cyan-500/40 text-slate-300 hover:text-cyan-300'
              ]"
            >
              {{ page }}
            </button>
          </div>

          <!-- 下一頁按鈕 -->
          <button
            type="button"
            @click="goToPage(currentPage + 1)"
            :disabled="currentPage === totalPages"
            class="min-h-[44px] px-4 rounded-xl text-sm font-semibold transition-all border flex items-center gap-1.5"
            :class="[
              currentPage === totalPages
                ? 'bg-slate-900/50 border-slate-800 text-slate-600 cursor-not-allowed'
                : 'bg-slate-900 hover:bg-slate-850 border-slate-800 hover:border-cyan-500/40 text-slate-200 hover:text-cyan-300 shadow-md'
            ]"
            aria-label="前往下一頁專案列表"
          >
            <span>下一頁</span>
            <ChevronRight class="w-4 h-4" :stroke-width="2" aria-hidden="true" />
          </button>
        </nav>
      </div>

      <!-- 若有設定 limit 且總作品數超過 limit，顯示查看全部按鈕 (供首頁使用) -->
      <div v-if="props.limit && store.projects.length > props.limit" class="mt-12 text-center">
        <router-link
          to="/showcase"
          class="inline-flex items-center justify-center px-8 py-4 rounded-2xl font-bold text-white bg-slate-800 hover:bg-slate-700 border border-slate-700/80 shadow-lg hover:border-cyan-500/50 hover:text-cyan-300 transition-all focus-visible:ring-2 focus-visible:ring-cyan-400 focus:outline-none"
        >
          查看全部學員專題成果
        </router-link>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, nextTick, watch } from 'vue'
import { Eye, Globe, ExternalLink, Code2, ChevronLeft, ChevronRight } from 'lucide-vue-next'
import SegmentedNav, { type SegmentedNavItem } from '@/components/common/SegmentedNav.vue'
import { createScrollStagger, gsap } from '@/utils/motion'
import { useCmsStore } from '@/stores/useCmsStore'
import type { StudentProject } from '@/types'

const PAGE_SIZE = 8 // 每頁固定 8 個學員專案

const props = withDefaults(
  defineProps<{
    limit?: number
    hideHeader?: boolean
  }>(),
  {
    hideHeader: false
  }
)

const store = useCmsStore()
const currentPage = ref(1)
const activeBatch = ref(0)
const flippedIds = ref(new Set<number>())
const brokenProjectImages = ref(new Set<number>())
const fallbackMap = ref<Record<number, string>>({})

// 統一靜態資產與遠端 CDN 縮圖網址解析 (支援本地降級)
function getProjectImageUrl(project: StudentProject): string {
  const customUrl = fallbackMap.value[project.id] || project.cover_image_url
  if (!customUrl) return ''
  if (customUrl.startsWith('http://') || customUrl.startsWith('https://') || customUrl.startsWith('data:')) {
    return customUrl
  }
  const cleanPath = customUrl.replace(/^\.?\//, '')
  return `${import.meta.env.BASE_URL}${cleanPath}`
}

// 多階智慧防禦：遠端 CDN 載入失敗時優先自動切換至打包之本地 WebP，若皆失敗才降級為占位卡片
function handleImgError(project: StudentProject) {
  const localFallback = `./projects/project_${project.id}.webp`
  if (fallbackMap.value[project.id] !== localFallback) {
    fallbackMap.value[project.id] = localFallback
  } else {
    brokenProjectImages.value.add(project.id)
  }
}
let scrollTriggerCtx: ReturnType<typeof createScrollStagger> | null = null

// 總頁數計算 (每 8 個為一頁)
const totalPages = computed(() => {
  return Math.ceil(filteredProjects.value.length / PAGE_SIZE) || 1
})

// 當前頁面展示之專案清單 (8 個為一頁)
// 依 CMS 的 batch_tag 分組，並以年份由新到舊排列（最近一屆的作品先呈現）
const batchGroups = computed(() => {
  const grouped = new Map<string, StudentProject[]>()
  for (const project of store.projects) {
    const tag = (project.batch_tag || '').trim()
    // 後台未填期別者不建立分類頁籤，仍會出現在「全部」
    if (!tag) continue
    if (!grouped.has(tag)) grouped.set(tag, [])
    grouped.get(tag)!.push(project)
  }
  return Array.from(grouped, ([tag, items]) => ({ tag, items, year: Number.parseInt(tag, 10) || 0 })).sort(
    (a, b) => b.year - a.year,
  )
})

const sortedProjects = computed(() => [
  ...batchGroups.value.flatMap((group) => group.items),
  ...store.projects.filter((project) => !(project.batch_tag || '').trim()),
])

const batchTabs = computed<SegmentedNavItem[]>(() => [
  { key: 'all', label: '全部', badge: String(store.projects.length) },
  ...batchGroups.value.map((group) => ({
    key: group.tag,
    label: group.tag,
    badge: String(group.items.length),
  })),
])

const filteredProjects = computed(() =>
  activeBatch.value === 0 ? sortedProjects.value : batchGroups.value[activeBatch.value - 1]?.items || [],
)

const displayedProjects = computed(() => {
  if (props.limit && props.limit > 0) {
    return sortedProjects.value.slice(0, props.limit)
  }
  const startIndex = (currentPage.value - 1) * PAGE_SIZE
  return filteredProjects.value.slice(startIndex, startIndex + PAGE_SIZE)
})

// 切換期別後回到第一頁，避免停在不存在的頁碼
watch(activeBatch, () => {
  currentPage.value = 1
  animatePageChange()
})

function initStaggerAnimation() {
  if (scrollTriggerCtx) {
    scrollTriggerCtx.revert()
    scrollTriggerCtx = null
  }
  nextTick(() => {
    // 專題成果卡片統一由全域工廠函式調度 (滾動到達時 100% 依序 stagger 微升)
    scrollTriggerCtx = createScrollStagger(
      '#showcase-cards-grid .showcase-card',
      '#showcase-cards-grid',
      { stagger: 0.08 }
    )
  })
}

function animatePageChange() {
  nextTick(() => {
    // 分頁切換時，新一頁的 8 張卡片依序溫潤微升
    gsap.fromTo(
      '#showcase-cards-grid .showcase-card',
      { y: 28, opacity: 0 },
      { y: 0, opacity: 1, duration: 0.8, stagger: 0.06, ease: 'power1.out', clearProps: 'transform,opacity' }
    )
  })
}

onMounted(() => {
  initStaggerAnimation()
})

// 當非同步取得後端作品資料時，重新精準綁定滾動動畫
watch(
  () => store.projects.length,
  () => {
    initStaggerAnimation()
  }
)

// 當切換分頁時，觸發新一頁的微升動態
watch(currentPage, () => {
  animatePageChange()
})

onUnmounted(() => {
  if (scrollTriggerCtx) scrollTriggerCtx.revert()
})

function toggleFlip(id: number) {
  if (flippedIds.value.has(id)) {
    flippedIds.value.delete(id)
  } else {
    flippedIds.value.add(id)
  }
}

function handleView(id: number) {
  store.trackProjectView(id)
}

function goToPage(page: number) {
  if (page < 1 || page > totalPages.value) return
  currentPage.value = page
  flippedIds.value.clear() // 切換分頁時重置翻轉狀態
  // 平滑滾動至作品牆頂部
  const el = document.getElementById('showcase')
  if (el) {
    el.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }
}
</script>

<style scoped>
.page-fade-enter-active,
.page-fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.page-fade-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

.page-fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>