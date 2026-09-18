<template>
	<section id="tracks-starting-points" class="section-shell bg-transparent relative overflow-hidden">

		<div class="max-w-[1536px] mx-auto px-4 sm:px-6 lg:px-8 2xl:px-12 relative z-10 w-full">
			<!-- 區塊標題 (大器單行標題，中高齡友善閱讀) -->
			<div class="section-head text-center max-w-5xl mx-auto">
				<h2 class="text-3xl sm:text-4xl lg:text-5xl xl:text-6xl font-black text-white tracking-tight leading-tight text-balance">
					<span class="block lg:inline">起點不同<span class="hidden lg:inline">，</span></span><span
						class="block mt-1 lg:mt-0 lg:inline text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 via-teal-400 to-cyan-400"
						>不代表從零開始</span
					>
				</h2>
				<!-- 輔助論述：手機收起，桌機保留 -->
				<p
					class="hidden sm:block text-slate-400 mt-4 text-base sm:text-lg mx-auto leading-relaxed text-pretty text-center"
				>
					過去的工作經驗，在做作品時都用得上。
				</p>
			</div>

			<!-- 4 大起點軌道圖示磚 -->
			<div class="max-w-4xl mx-auto">
				<SpotlightTiles
					v-model="active"
					:items="tracks"
					id-prefix="tracks-starting-points"
					ariaLabel="四大起點軌道"
					columns="grid-cols-2 lg:grid-cols-4"
				/>
			</div>
		</div>
	</section>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Sprout, Route, Palette, Laptop } from 'lucide-vue-next'
import SpotlightTiles, { type SpotlightItem } from '@/components/common/SpotlightTiles.vue'

const tracks: SpotlightItem[] = [
	{
		key: 'beginner',
		icon: Sprout,
		iconActiveClass: 'text-cyan-300',
		navLabel: '零基礎',
		eyebrow: '完全沒有程式背景',
		title: '從零出發的轉職者',
		body: '從最基礎的網頁排版開始，每日實作演練打底。',
		eyebrowClass: 'text-cyan-400',
		activeTile: 'bg-cyan-500/15 border-cyan-400/60 shadow-cyan-950/50',
		panelBorder: 'border-cyan-500/50',
	},
	{
		key: 'career',
		icon: Route,
		iconActiveClass: 'text-blue-300',
		navLabel: '轉換跑道',
		eyebrow: '想建立新專業',
		title: '探索職涯可能性',
		body: '半年換一項帶得走的技能，工作幾年後還在用。',
		eyebrowClass: 'text-blue-400',
		activeTile: 'bg-blue-500/15 border-blue-400/60 shadow-blue-950/50',
		panelBorder: 'border-blue-500/50',
	},
	{
		key: 'designer',
		icon: Palette,
		iconActiveClass: 'text-purple-300',
		navLabel: '設計背景',
		eyebrow: '設計與視覺背景',
		title: '設計、UI/UX 創作者',
		body: '發揮美感優勢，親手把設計稿變成真實產品。',
		eyebrowClass: 'text-purple-400',
		activeTile: 'bg-purple-500/15 border-purple-400/60 shadow-purple-950/50',
		panelBorder: 'border-purple-500/50',
	},
	{
		key: 'self-taught',
		icon: Laptop,
		iconActiveClass: 'text-emerald-300',
		navLabel: '自學卡關',
		eyebrow: '曾接觸過程式',
		title: '自學瓶頸或資訊相關',
		body: '920 小時系統化訓練，把破碎知識整合成專案能力。',
		eyebrowClass: 'text-emerald-400',
		activeTile: 'bg-emerald-500/15 border-emerald-400/60 shadow-emerald-950/50',
		panelBorder: 'border-emerald-500/50',
	},
]

const active = ref(0)
</script>
