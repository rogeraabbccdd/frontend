<template>
  <section
    id="facilities"
    :class="[
      hideHeader
        ? 'py-6 sm:py-10 bg-transparent relative'
        : 'section-shell bg-transparent relative overflow-hidden'
    ]"
  >
    <!-- 頂部與底部環境發光微暈 -->

    <div class="max-w-[1536px] mx-auto px-4 sm:px-6 lg:px-8 2xl:px-12 relative z-10 w-full">
      <!-- 區塊標題 -->
      <div v-if="!hideHeader" class="section-head text-center max-w-5xl mx-auto">
        <h2 class="text-3xl sm:text-4xl lg:text-5xl xl:text-6xl font-black text-white tracking-tight leading-tight text-balance">
          <span class="block lg:inline">接下來半年<span class="hidden lg:inline">，</span></span><span
						class="block mt-1 lg:mt-0 lg:inline text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 via-blue-400 to-emerald-400">你會在這裡學習</span>
        </h2>
      </div>


      <!-- 教室環境實景 (手機單張＋左右箭頭，sm 以上並排 2 欄) -->
      <div id="facilities-cards-grid" class="relative grid sm:grid-cols-2 gap-4 sm:gap-6 max-w-5xl mx-auto">
        <StepperArrows v-model="active" :total="displayFacilities.length" unit-label="場地" />

        <div
          v-for="(fac, index) in visibleFacilities"
          :key="fac.id || index"
          class="facility-card card-subsurface-glow relative rounded-3xl overflow-hidden bg-slate-900/80 backdrop-blur-xl border border-slate-800/90 shadow-xl shadow-slate-950/60 flex flex-col justify-between transform-gpu cursor-default"
        >

          <!-- 圖片展示相框 (固定 16:10 比例) -->
          <div class="facility-frame aspect-[16/10] lg:aspect-[16/9] bg-slate-800/80 relative overflow-hidden flex items-center justify-center">
            <img
              :src="fac.displayImage"
              :alt="fac.image_alt || fac.displayTitle"
              @error="handleFacilityImgError(fac.id)"
              class="w-full h-full object-cover"
            />

            <!-- 底部微光漸層遮罩 -->
            <div class="absolute inset-0 bg-gradient-to-t from-slate-900 via-transparent to-transparent opacity-60"></div>
          </div>

          <!-- 說明區塊 (僅保留標題與設備說明兩層) -->
          <div class="p-5 pb-9 sm:pb-5 flex-1 flex flex-col relative z-10">
            <h3 class="mb-2 text-xl sm:text-2xl font-black text-white tracking-tight leading-snug text-balance">
              {{ fac.displayTitle }}
            </h3>
            <p class="text-slate-200 leading-relaxed text-base sm:text-lg text-pretty">
              {{ fac.displayDescription }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useMediaQuery } from '@vueuse/core'
import StepperArrows from '@/components/common/StepperArrows.vue'
import { useCmsStore } from '@/stores/useCmsStore'
import facility1Img from '@/assets/facilities/learning_ijciKln_09KM7k0_ddXbwFz.webp'
import facility2Img from '@/assets/facilities/lunch_g71Ci6n_NsJ8XsZ_mJ12g5T.webp'

const defaultFacilityImages = [facility1Img, facility2Img]
const brokenFacilityIds = ref<Set<number>>(new Set())

function getFacilityImage(fac: { id?: number; image_url?: string }, index: number) {
  // 若該設施圖片已被標記載入失敗，或後端未提供有效圖片路徑，100% 穩定回傳本地高畫質實景資產
  if ((fac.id && brokenFacilityIds.value.has(fac.id)) || !fac.image_url) {
    return defaultFacilityImages[index % defaultFacilityImages.length]
  }
  return fac.image_url
}

// 雙重防禦：遠端圖片 404 或載入失敗時，立即觸發響應式降級，切換至本地實景照片
function handleFacilityImgError(facId?: number) {
  if (facId !== undefined) {
    brokenFacilityIds.value.add(facId)
  }
}

// 智慧解析主標與副標：優先使用 subtitle，若無則依頓號自動拆分（雙重防禦相容）
function getFacilityTitle(fac?: { facility_name?: string }) {
  // 設施名稱若以「、」串接多個詞，僅取第一段作為卡片標題
  return (fac?.facility_name || '').split('、')[0]
}

withDefaults(
  defineProps<{
    hideHeader?: boolean
  }>(),
  {
    hideHeader: false
  }
)

const store = useCmsStore()

function getConciseFacilityDesc(desc?: string) {
  if (!desc) return ''
  const sentences = desc.split('。').filter(Boolean)
  // 僅取首句重點，避免實景卡片出現大段說明文字
  const text = sentences[0] ?? desc
  // 截斷處若已自帶終止標點（！？…），不再補句號，避免出現「！。」雙標點
  return /[。！？!?…]$/.test(text) ? text : text + '。'
}

// 防禦性預處理設施清單，兼顧主副標智慧解析與安全圖片綁定，杜絕 template 重複呼叫
const displayFacilities = computed(() => {
  return (store.facilities || []).map((fac, index) => {
    return {
      ...fac,
      displayTitle: getFacilityTitle(fac),
      displayDescription: getConciseFacilityDesc(fac.description),
      displayImage: getFacilityImage(fac, index)
    }
  })
})

// 手機一次只顯示一張場地照，sm 以上並排顯示全部
const active = ref(0)
const isWide = useMediaQuery('(min-width: 640px)')
const visibleFacilities = computed(() =>
	isWide.value ? displayFacilities.value : displayFacilities.value.slice(active.value, active.value + 1),
)
</script>
