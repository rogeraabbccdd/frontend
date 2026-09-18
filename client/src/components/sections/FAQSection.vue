<template>
  <section id="faq" class="py-12 bg-slate-950 relative overflow-hidden">
    <!-- 頂部環境發光微暈 -->
    <div class="absolute -top-32 left-1/3 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl pointer-events-none"></div>

    <div class="max-w-[1536px] mx-auto px-4 sm:px-6 lg:px-8 2xl:px-12 relative z-10 w-full">
      <!-- FAQ 手風琴清單 (大螢幕置中限寬，最佳閱讀行長，避免文字橫向過寬) -->
      <div class="space-y-4 max-w-4xl mx-auto">
        <div
          v-for="faq in store.faqs"
          :key="faq.id"
          class="rounded-2xl bg-slate-900/80 border border-slate-800 hover:border-slate-700/80 overflow-hidden transition-[border-color,background-color,box-shadow] duration-300 shadow-md"
          :class="activeId === faq.id ? 'border-cyan-500/40 bg-slate-900' : ''"
        >
          <button
            type="button"
            :id="'faq-btn-' + faq.id"
            :aria-controls="'faq-panel-' + faq.id"
            @click="toggleFaq(faq.id)"
            class="w-full p-5 sm:p-6 text-left flex items-center justify-between space-x-4 transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-cyan-400"
            :aria-expanded="activeId === faq.id"
          >
            <div class="flex items-center gap-3.5 sm:gap-4 min-w-0">
              <span
                class="w-12 h-12 sm:w-14 sm:h-14 shrink-0 rounded-2xl bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center transition-colors duration-300"
                :class="activeId === faq.id ? 'bg-cyan-500/20 border-cyan-500/40' : ''"
                role="img"
                :aria-label="faq.category"
              >
                <component :is="categoryIcon(faq.category)" class="w-6 h-6 sm:w-7 sm:h-7 text-cyan-400" :stroke-width="1.75" />
              </span>
              <span class="font-bold text-white text-base sm:text-lg text-pretty">
                {{ faq.question }}
              </span>
            </div>
            <span
              aria-hidden="true"
              class="shrink-0 w-8 h-8 rounded-full bg-slate-800/80 border border-slate-700/80 flex items-center justify-center transition-[transform,color,border-color] duration-300"
              :class="activeId === faq.id ? 'rotate-180 text-cyan-400 border-cyan-500/40' : 'text-slate-300'"
            >
              <svg class="w-4 h-4" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2.5">
                <path d="M5 8l5 5 5-5" stroke-linecap="round" stroke-linejoin="round" />
              </svg>
            </span>
          </button>

          <!-- 絲滑 Grid 展開動效 (WAI-ARIA 合規 region) -->
          <div
            :id="'faq-panel-' + faq.id"
            role="region"
            :aria-labelledby="'faq-btn-' + faq.id"
            class="grid transition-[grid-template-rows] duration-300 ease-out"
            :class="activeId === faq.id ? 'grid-rows-[1fr]' : 'grid-rows-[0fr]'"
          >
            <div class="overflow-hidden">
              <div class="px-5 sm:px-6 pb-6 pt-2 text-slate-300 text-base leading-relaxed border-t border-slate-800/60 whitespace-pre-line">
                {{ faq.answer }}
              </div>
            </div>
          </div>
        </div>
      </div>

            <!-- 官方規範指引與免責聲明卡片 (加大字級更清晰易讀，寬度與手風琴一致置中) -->
      <div class="mt-10 max-w-4xl mx-auto p-6 sm:p-8 rounded-3xl bg-slate-900/80 border border-cyan-500/30 shadow-xl shadow-slate-950/50 text-left flex items-start gap-4">
        <span class="w-12 h-12 shrink-0 rounded-2xl bg-cyan-500/15 border border-cyan-500/30 flex items-center justify-center" aria-hidden="true">
          <Info class="w-6 h-6 text-cyan-300" />
        </span>
        <div class="space-y-2.5 flex-1">
          <span class="block text-base sm:text-lg font-black text-white tracking-tight">權益提醒</span>
          <p class="text-base text-slate-300 leading-relaxed">
            參訓資格、免費受訓審查、生活津貼與招生期程，<strong class="text-white font-bold">一律以台灣就業通的最新公告與簡章為準</strong>。
          </p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick, watch, type Component } from 'vue'
import {
  Info,
  UserCheck,
  Wallet,
  HandCoins,
  Clock,
  Briefcase,
  BedDouble,
  CircleHelp,
} from 'lucide-vue-next'
import { gsap } from '@/utils/motion'
import { useCmsStore } from '@/stores/useCmsStore'

const store = useCmsStore()
const activeId = ref<number | null>(null)

// 分類名來自 CMS，可能新增未預期的值，因此保留泛用問號圖示作為預設
const CATEGORY_ICONS: Record<string, Component> = {
  參訓資格: UserCheck,
  參訓費用: Wallet,
  生活津貼: HandCoins,
  上課時間: Clock,
  就業輔導: Briefcase,
  住宿申請: BedDouble,
}

function categoryIcon(category: string): Component {
  return CATEGORY_ICONS[(category || '').trim()] || CircleHelp
}

function toggleFaq(id: number) {
  activeId.value = activeId.value === id ? null : id
}

// FAQ 頁面頂部直接平滑進場
const playDirectEnter = () => {
  nextTick(() => {
    gsap.fromTo(
      '#faq .rounded-2xl',
      { y: 20, opacity: 0 },
      { y: 0, opacity: 1, duration: 0.7, stagger: 0.05, ease: 'power1.out', clearProps: 'transform,opacity' }
    )
  })
}
onMounted(playDirectEnter)
watch(() => store.faqs.length, playDirectEnter)
</script>
