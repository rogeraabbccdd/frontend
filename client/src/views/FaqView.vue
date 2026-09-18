<template>
  <div class="flex-grow">
    <!-- 標準化頂部 Header -->
    <PageHeader
      title="常見問題 FAQ"
      subtitle="零基礎、費用、津貼、上課時間，報名前最常被問到的都在這裡。"
      theme="cyan"
    />

    <!-- FAQ 手風琴列表 (支援絲滑展開，由 PageHeader 統一引導) -->
    <FAQSection />

    <!-- 底部導引前往 Discord 社群 -->
    <section class="py-20 sm:py-24 bg-slate-900/30 border-t border-slate-800/60 text-center relative overflow-hidden">
      <div class="max-w-[1536px] mx-auto px-4 sm:px-6 lg:px-8 2xl:px-12 space-y-4">
        <div class="max-w-3xl mx-auto space-y-4">
          <h3 class="text-2xl sm:text-3xl font-black text-white tracking-tight">還有其他問題？</h3>
          <p class="text-slate-300 text-base">授課老師、在訓學員與結訓學長姐都在 Discord 社群裡，可以直接發問。</p>
          <div class="pt-2">
            <router-link
              to="/community"
              class="inline-flex items-center justify-center px-8 py-4 rounded-2xl font-bold text-base text-white bg-[#5865F2] hover:bg-[#4752C4] shadow-xl shadow-indigo-500/25 hover:shadow-indigo-500/40 hover:-translate-y-0.5 active:scale-95 transition-all"
            >
              前往 Discord 線上諮詢社群
            </router-link>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { useCmsStore } from '@/stores/useCmsStore'
import { useSeoMeta } from '@/composables/useSeoMeta'
import PageHeader from '@/components/layout/PageHeader.vue'
import FAQSection from '@/components/sections/FAQSection.vue'

const store = useCmsStore()

useSeoMeta(() => {
  const faqEntities = (store.faqs || []).map(faq => ({
    '@type': 'Question',
    'name': faq.question,
    'acceptedAnswer': {
      '@type': 'Answer',
      'text': faq.answer
    }
  }))

  return {
    title: '常見問題與解答 ｜ 待業者生活津貼與報名資格 FAQ',
    description: '整理報名泰山職訓「前端網頁技術與AI應用」專班的常見問題：包含零基礎參訓可行性、每月職訓生活津貼申請成數、報名與甄試流程、一人一機培訓設施與就業輔導。',
    canonicalPath: '/faq',
    robots: 'index, follow',
    jsonLd: [
      {
        '@type': 'BreadcrumbList',
        'itemListElement': [
          {
            '@type': 'ListItem',
            'position': 1,
            'name': '首頁',
            'item': 'https://wdaweb.github.io/frontend/'
          },
          {
            '@type': 'ListItem',
            'position': 2,
            'name': '常見問題 FAQ',
            'item': 'https://wdaweb.github.io/frontend/faq'
          }
        ]
      },
      {
        '@type': 'FAQPage',
        'mainEntity': faqEntities
      }
    ]
  }
})
</script>
