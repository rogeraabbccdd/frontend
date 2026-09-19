<template>
	<section
		id="audience-resonance"
		class="section-shell bg-transparent relative overflow-hidden"
	>

		<div class="max-w-[1536px] mx-auto px-4 sm:px-6 lg:px-8 2xl:px-12 relative z-10 w-full">
			<!-- 受眾心聲共鳴標頭 -->
			<div class="section-head text-center max-w-5xl xl:max-w-6xl mx-auto">
				<h2
					class="text-3xl sm:text-4xl lg:text-5xl xl:text-6xl font-black text-white tracking-tight leading-tight text-balance"
				>
					<span class="block lg:inline">你面對的<span class="hidden lg:inline">，</span></span><span
						class="block mt-1 lg:mt-0 lg:inline"
						>不只是要不要學程式</span
					>
				</h2>
				<p class="hidden sm:block text-slate-400 mt-4 text-base sm:text-lg mx-auto leading-relaxed text-pretty text-center">
					害怕跟不上、害怕選錯方向，其實很正常。
				</p>
			</div>

			<!-- 3 大轉職困惑問答手風琴 (一次只展開一則，避免長文同屏堆疊) -->
			<div class="max-w-4xl mx-auto">
				<AccordionList v-model="active" :items="doubts" id-prefix="audience-resonance" />
			</div>
		</div>
	</section>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { CircleHelp, Bot, School } from 'lucide-vue-next'
import AccordionList, { type AccordionItem } from '@/components/common/AccordionList.vue'

const doubts: AccordionItem[] = [
	{
		key: 'doubt-01',
		icon: CircleHelp,
		title: '完全沒寫過程式，我真的學得會嗎？',
		quote: '「看著滿螢幕的英文程式碼，總覺得是離自己非常遙遠的世界……」',
		body: '課程從最基礎的排版教起，每天動手實作。真正的門檻是能不能花滿半年。',
		iconClass: 'bg-cyan-500/15 border-cyan-500/40',
		activeBorder: 'border-cyan-500/50',
	},
	{
		key: 'doubt-02',
		icon: Bot,
		title: '現在才學寫程式，會不會馬上被 AI 取代？',
		quote: '「新聞天天都在報 AI 能一秒寫出網頁，現在投入還有競爭力嗎……」',
		body: 'AI 讓寫程式變容易，卻讓架構思維、獨立除錯與判斷力更加關鍵。課程教的是理解自己正在做什麼。',
		iconClass: 'bg-emerald-500/15 border-emerald-500/40',
		activeBorder: 'border-emerald-500/50',
	},
	{
		key: 'doubt-03',
		icon: School,
		title: '自學資源這麼多，為什麼需要來職訓？',
		quote: '「看線上教學好像都懂，自己開編輯器卻一行都寫不出來……」',
		body: '免費教材到處都有。難的是排除干擾、卡關有人能問，還能撐你走完半年。',
		iconClass: 'bg-purple-500/15 border-purple-500/40',
		activeBorder: 'border-purple-500/50',
	},
]

// 預設展開第一則，讓訪客一眼看見問答形式
const active = ref(0)
</script>
