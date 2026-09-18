<template>
	<section
		id="outcomes"
		class="section-shell bg-transparent relative overflow-hidden"
	>

		<div class="max-w-[1536px] mx-auto px-4 sm:px-6 lg:px-8 2xl:px-12 relative z-10 w-full">
			<!-- 區塊前導標題 -->
			<div class="section-head text-center max-w-4xl mx-auto">
				<h2
					class="text-3xl sm:text-4xl lg:text-5xl xl:text-6xl font-black text-white tracking-tight leading-tight text-balance"
				>
					<span class="block lg:inline">你帶走的<span class="hidden lg:inline">，</span></span><span
						class="block mt-1 lg:mt-0 lg:inline text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 via-blue-400 to-emerald-400"
						>不只是一張結訓證明</span
					>
				</h2>
			</div>

			<!-- 6 大真實收穫圖示磚 -->
			<div class="max-w-5xl mx-auto">
				<SpotlightTiles
					v-model="active"
					:items="takeaways"
					id-prefix="outcomes"
					aria-label="四大結訓收穫"
					columns="grid-cols-2 lg:grid-cols-4"
				/>
			</div>
		</div>
	</section>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Globe, ScanSearch, Users, Compass } from 'lucide-vue-next'
import SpotlightTiles, { type SpotlightItem } from '@/components/common/SpotlightTiles.vue'

const takeaways: SpotlightItem[] = [
	{
		key: 'portfolio',
		icon: Globe,
		iconActiveClass: 'text-cyan-300',
		navLabel: '專案作品',
		title: '真正做出屬於自己的作品',
		titleClass: 'text-cyan-300',
		body: '獨立完成可向面試官展示、說得出架構細節與選型理由的專案代表作。',
		activeTile: 'bg-cyan-500/15 border-cyan-400/60 shadow-cyan-950/50',
		panelBorder: 'border-cyan-500/50',
	},
	{
		key: 'debug',
		icon: ScanSearch,
		iconActiveClass: 'text-blue-300',
		navLabel: '除錯能力',
		title: '建立拆解與解決問題的能力',
		titleClass: 'text-blue-300',
		body: '面對 Bug 不盲猜答案，學會從 Console 定位根因，具備獨立除錯思維。',
		activeTile: 'bg-blue-500/15 border-blue-400/60 shadow-blue-950/50',
		panelBorder: 'border-blue-500/50',
	},
	{
		key: 'peers',
		icon: Users,
		iconActiveClass: 'text-amber-300',
		navLabel: '同行夥伴',
		title: '認識一起學習成長的夥伴',
		titleClass: 'text-amber-300',
		body: '半年一起上課的同學，畢業後還在同一個圈子裡。',
		activeTile: 'bg-amber-500/15 border-amber-400/60 shadow-amber-950/50',
		panelBorder: 'border-amber-500/50',
	},
	{
		key: 'clarity',
		icon: Compass,
		iconActiveClass: 'text-cyan-300',
		navLabel: '職涯方向',
		title: '更清楚自己是否適合走這條路',
		titleClass: 'text-cyan-300',
		body: '六個月後，你會更知道自己適不適合這行。',
		activeTile: 'bg-cyan-500/15 border-cyan-400/60 shadow-cyan-950/50',
		panelBorder: 'border-cyan-500/50',
	},
]

const active = ref(0)
</script>
